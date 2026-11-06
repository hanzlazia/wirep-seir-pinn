"""
WIRE-P SEIR-PINN — single reproducible implementation used for every result
in the revised manuscript.

This module reproduces the original notebook pipeline exactly (network,
softmax output, IC gate, CWAC collocation, 3-phase Adam/Adam/L-BFGS schedule,
EMA, metrics) and adds:
  * an exactly admissible (zero-mean) WIRE-P variant, WIRE-P-A, using an
    analytic mean-correction term (the rational analogue of the classical
    "complete Morlet" correction);
  * the complete (zero-mean) Morlet, MV-Morlet-A;
  * a phase ablation, WIRE-P(phi=0);
  * an inverse-problem mode: unknown epidemic parameters are learned jointly
    with the network from noisy, partial observations (I(t) only).

The physics loss is the explicit differential residual
    r_k(tau) = (1/T) du_k/dtau - f_k(u(tau); theta),
not the right-hand side f_k alone.
"""
import math
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from scipy.integrate import odeint

DTYPE = torch.float64
torch.set_default_dtype(DTYPE)

# ── Defaults identical to the original notebooks ─────────────────────────
BUDGET = {"n_p1": 4000, "n_p2": 4000, "n_lbfgs": 3000}
N_COLLOC = 6000
EPS_FLOOR = 0.08
PILOT_N_PTS = 300
PILOT_RTOL, PILOT_ATOL = 1e-4, 1e-4
LAYERS = (1, 64, 64, 64, 64, 4)
RATE_LR_MULT = 50.0  # Adam lr multiplier for learned epidemic rates (inverse mode)
RATE_FREEZE = 0      # phase-1 epochs during which learned rates are held at their initial guess

DISEASES = {
    "Hantavirus": dict(name="Hantavirus", beta=0.16, sigma=1 / 12.0, gamma=1 / 14.0,
                       N=1_000_000, E0=10.0, I0=2.0, R_init=0.0, T=400.0),
    "SARS-2003": dict(name="SARS-2003", beta=0.27, sigma=1 / 5.0, gamma=1 / 10.0,
                      N=1_000_000, E0=10.0, I0=2.0, R_init=0.0, T=300.0),
    "COVID-19": dict(name="COVID-19", beta=0.35, sigma=1 / 5.1, gamma=1 / 14.0,
                     N=1_000_000, E0=50.0, I0=2.0, R_init=0.0, T=300.0),
}


# ══════════════════════════════════════════════════════════════════════════
#  ACTIVATIONS
# ══════════════════════════════════════════════════════════════════════════

def _omega(raw, lo, hi):
    return lo + (hi - lo) * torch.sigmoid(raw)


class MVMorletActivation(nn.Module):
    """psi(x) = cos(omega z) exp(-z^2/2), z = (x-b)/s.  3 params/neuron."""
    def __init__(self, dim, omega_min=0.5, omega_max=2.0, **kw):
        super().__init__()
        self.omega_min, self.omega_max = omega_min, omega_max
        self.omega_raw = nn.Parameter(torch.zeros(dim))
        self.b = nn.Parameter(torch.zeros(dim))
        self.s_raw = nn.Parameter(torch.full((dim,), 0.5413))

    def forward(self, x):
        omega = _omega(self.omega_raw, self.omega_min, self.omega_max)
        s = F.softplus(self.s_raw) + 1e-3
        z = (x - self.b) / s
        return torch.cos(omega * z) * torch.exp(-0.5 * z * z)


class MVMorletAdmActivation(MVMorletActivation):
    """Complete (exactly zero-mean) Morlet:
    psi(x) = (cos(omega z) - exp(-omega^2/2)) exp(-z^2/2)."""
    def forward(self, x):
        omega = _omega(self.omega_raw, self.omega_min, self.omega_max)
        s = F.softplus(self.s_raw) + 1e-3
        z = (x - self.b) / s
        return (torch.cos(omega * z) - torch.exp(-0.5 * omega * omega)) * torch.exp(-0.5 * z * z)


class MVMorletPlusActivation(nn.Module):
    """Parameter-matched control: a * MV-Morlet + c (5 params/neuron)."""
    def __init__(self, dim, omega_min=0.5, omega_max=2.0, **kw):
        super().__init__()
        self.omega_min, self.omega_max = omega_min, omega_max
        self.omega_raw = nn.Parameter(torch.zeros(dim))
        self.b = nn.Parameter(torch.zeros(dim))
        self.s_raw = nn.Parameter(torch.full((dim,), 0.5413))
        self.a = nn.Parameter(torch.ones(dim))
        self.c = nn.Parameter(torch.zeros(dim))

    def forward(self, x):
        omega = _omega(self.omega_raw, self.omega_min, self.omega_max)
        s = F.softplus(self.s_raw) + 1e-3
        z = (x - self.b) / s
        return self.a * torch.cos(omega * z) * torch.exp(-0.5 * z * z) + self.c


# Gauss-Legendre nodes for the Bessel-K integral representation
#   K_nu(x) = int_0^inf exp(-x cosh t) cosh(nu t) dt
_GL_T, _GL_W = np.polynomial.legendre.leggauss(256)
_T_MAX = 14.0


def rational_cos_ratio(omega, alpha, p):
    """kappa = int cos(omega z)(1+alpha z^2)^-p dz / int (1+alpha z^2)^-p dz
             = 2 (x/2)^nu K_nu(x) / Gamma(nu),  x = omega/sqrt(alpha), nu = p - 1/2.
    Differentiable in (omega, alpha, p); accurate to ~1e-12 for the parameter
    ranges reachable in training (x >= ~0.05, nu <= ~40)."""
    t = torch.as_tensor(0.5 * (_GL_T + 1.0) * _T_MAX, dtype=omega.dtype, device=omega.device)
    w = torch.as_tensor(0.5 * _GL_W * _T_MAX, dtype=omega.dtype, device=omega.device)
    x = (omega / torch.sqrt(alpha)).unsqueeze(-1)
    nu = (p - 0.5).unsqueeze(-1)
    # log of integrand of 2 (x/2)^nu K_nu(x) / Gamma(nu)
    log_cosh = nu * t + torch.log1p(torch.exp(-2.0 * nu * t)) - math.log(2.0)
    log_f = math.log(2.0) + nu * torch.log(x / 2.0) - x * torch.cosh(t) + log_cosh \
        - torch.lgamma(nu)
    return (torch.exp(log_f) * w).sum(-1)


class WIREPActivation(nn.Module):
    """Original WIRE-P (as submitted):
    psi(x) = cos(omega z + phi) (1 + alpha z^2)^-p,  phi = arctan(alpha omega).
    NOTE: this function is NOT zero-mean; its integral equals
    cos(phi) * int cos(omega z)(1+alpha z^2)^-p dz > 0.
    mode: "coupled" (phi=arctan(alpha omega), original), "zero" (phi=0 ablation),
          "admissible" (coupled phase + analytic mean correction => exact zero mean).
    """
    def __init__(self, dim, omega_min=0.5, omega_max=2.0, bandwidth_hint=None,
                 mode="coupled", **kw):
        super().__init__()
        self.omega_min, self.omega_max = omega_min, omega_max
        self.mode = mode
        p_init = 4.0
        p_raw_val = float(np.log(np.exp(min(p_init - 1.0, 20.0)) - 1.0))
        alpha_init = float(np.clip(
            (2.0 ** (1.0 / p_init) - 1.0) / (float(bandwidth_hint) ** 2 + 1e-12), 0.1, 4.0)
        ) if bandwidth_hint else 1.0
        alpha_raw_val = float(np.log(np.exp(min(alpha_init, 20.0)) - 1.0))
        self.omega_raw = nn.Parameter(torch.zeros(dim))
        self.b = nn.Parameter(torch.zeros(dim))
        self.s_raw = nn.Parameter(torch.full((dim,), 0.5413))
        self.p_raw = nn.Parameter(torch.full((dim,), p_raw_val))
        self.alpha_raw = nn.Parameter(torch.full((dim,), alpha_raw_val))

    def params(self):
        omega = _omega(self.omega_raw, self.omega_min, self.omega_max)
        s = F.softplus(self.s_raw) + 1e-3
        p = F.softplus(self.p_raw) + 1.0
        alpha = F.softplus(self.alpha_raw) + 1e-3
        phi = torch.zeros_like(omega) if self.mode == "zero" else torch.atan(alpha * omega)
        return omega, s, p, alpha, phi

    def forward(self, x):
        omega, s, p, alpha, phi = self.params()
        z = (x - self.b) / s
        env = torch.pow(1.0 + alpha * z * z, -p)
        osc = torch.cos(omega * z + phi)
        if self.mode == "admissible":
            osc = osc - torch.cos(phi) * rational_cos_ratio(omega, alpha, p)
        return osc * env


class WIREP0Activation(WIREPActivation):
    def __init__(self, dim, **kw):
        kw["mode"] = "zero"
        super().__init__(dim, **kw)


class WIREPAdmActivation(WIREPActivation):
    def __init__(self, dim, **kw):
        kw["mode"] = "admissible"
        super().__init__(dim, **kw)


class TanhActivation(nn.Module):
    def __init__(self, dim, **kw):
        super().__init__()

    def forward(self, x):
        return torch.tanh(x)


class ReLUActivation(nn.Module):
    def __init__(self, dim, **kw):
        super().__init__()

    def forward(self, x):
        return F.relu(x)


class SigmoidActivation(nn.Module):
    def __init__(self, dim, **kw):
        super().__init__()

    def forward(self, x):
        return torch.sigmoid(x)


class SineActivation(nn.Module):
    def __init__(self, dim, omega_0=1.0, **kw):
        super().__init__()
        self.omega_0 = omega_0

    def forward(self, x):
        return torch.sin(self.omega_0 * x)


# ══════════════════════════════════════════════════════════════════════════
#  NETWORKS (softmax output => S+E+I+R=1; IC gate => u(0)=u0 exactly)
# ══════════════════════════════════════════════════════════════════════════

class _GatedPINN(nn.Module):
    def forward(self, tau):
        raw = self._raw(tau)
        gate = 1.0 - torch.exp(-tau / self.tau_ic)
        return self.u0 + gate * (raw - self.u0)


class SEIR_PINN(_GatedPINN):
    def __init__(self, layers, u0, activation_cls, tau_ic=0.05, act_kwargs=None):
        super().__init__()
        act_kwargs = act_kwargs or {}
        self.lins = nn.ModuleList()
        self.acts = nn.ModuleList()
        for i in range(len(layers) - 1):
            lin = nn.Linear(layers[i], layers[i + 1])
            nn.init.xavier_normal_(lin.weight)
            nn.init.zeros_(lin.bias)
            self.lins.append(lin)
            if i < len(layers) - 2:
                self.acts.append(activation_cls(layers[i + 1], **act_kwargs))
        self.register_buffer("u0", u0)
        self.tau_ic = tau_ic

    def _raw(self, tau):
        x = tau
        for i, lin in enumerate(self.lins):
            x = lin(x)
            if i < len(self.lins) - 1:
                x = self.acts[i](x)
        return torch.softmax(x, dim=-1)


def siren_init_(linear, is_first, omega_0):
    fan_in = linear.weight.size(1)
    with torch.no_grad():
        bound = 1.0 / fan_in if is_first else np.sqrt(6.0 / fan_in) / omega_0
        linear.weight.uniform_(-bound, bound)
        nn.init.zeros_(linear.bias)


class SIREN_PINN(_GatedPINN):
    def __init__(self, layers, u0, tau_ic=0.05, omega_0_first=30.0, omega_0_hidden=1.0):
        super().__init__()
        self.lins = nn.ModuleList()
        self.acts = nn.ModuleList()
        for i in range(len(layers) - 1):
            lin = nn.Linear(layers[i], layers[i + 1])
            omega_0 = omega_0_first if i == 0 else omega_0_hidden
            siren_init_(lin, i == 0, omega_0)
            self.lins.append(lin)
            if i < len(layers) - 2:
                self.acts.append(SineActivation(layers[i + 1], omega_0=omega_0))
        self.register_buffer("u0", u0)
        self.tau_ic = tau_ic

    _raw = SEIR_PINN._raw


class Fourier_PINN(_GatedPINN):
    def __init__(self, layers, u0, tau_ic=0.05, n_fourier=32, sigma=4.0, seed=0):
        super().__init__()
        g = torch.Generator().manual_seed(seed)
        self.register_buffer("B", torch.randn(layers[0], n_fourier, generator=g, dtype=DTYPE) * sigma)
        mlp = (2 * n_fourier,) + tuple(layers[1:])
        self.lins = nn.ModuleList()
        for i in range(len(mlp) - 1):
            lin = nn.Linear(mlp[i], mlp[i + 1])
            nn.init.xavier_normal_(lin.weight)
            nn.init.zeros_(lin.bias)
            self.lins.append(lin)
        self.register_buffer("u0", u0)
        self.tau_ic = tau_ic

    def _raw(self, tau):
        proj = 2.0 * np.pi * (tau @ self.B)
        x = torch.cat([torch.cos(proj), torch.sin(proj)], dim=-1)
        for i, lin in enumerate(self.lins):
            x = lin(x)
            if i < len(self.lins) - 1:
                x = torch.tanh(x)
        return torch.softmax(x, dim=-1)


ACTIVATIONS = {
    "MV-Morlet": MVMorletActivation,
    "MV-Morlet-A": MVMorletAdmActivation,
    "MV-Morlet+": MVMorletPlusActivation,
    "WIRE-P": WIREPActivation,
    "WIRE-P(phi=0)": WIREP0Activation,
    "WIRE-P-A": WIREPAdmActivation,
    "Tanh": TanhActivation,
    "ReLU": ReLUActivation,
    "Sigmoid": SigmoidActivation,
}


def build_model(act, layers, u0, tau_ic, bw_hint, seed, device):
    torch.manual_seed(seed)
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if act == "SIREN":
        m = SIREN_PINN(layers, u0, tau_ic)
    elif act == "Fourier":
        m = Fourier_PINN(layers, u0, tau_ic, n_fourier=32, sigma=4.0, seed=seed)
    else:
        kw = {"bandwidth_hint": bw_hint} if act.startswith("WIRE-P") else {}
        m = SEIR_PINN(layers, u0, ACTIVATIONS[act], tau_ic, act_kwargs=kw)
    return m.to(device)


class EMA:
    def __init__(self, model, decay=0.999):
        self.decay = decay
        self.shadow = {n: p.detach().clone() for n, p in model.named_parameters() if p.requires_grad}

    def update(self, model):
        for n, p in model.named_parameters():
            if p.requires_grad:
                self.shadow[n].mul_(self.decay).add_(p.detach(), alpha=1 - self.decay)

    def apply_to(self, model):
        for n, p in model.named_parameters():
            if p.requires_grad and n in self.shadow:
                p.data.copy_(self.shadow[n])


# ══════════════════════════════════════════════════════════════════════════
#  ODE, reference solution, collocation
# ══════════════════════════════════════════════════════════════════════════

def seir_rhs(y, t, beta, sigma, gamma, N):
    S, E, I, R = y
    bSI = beta * S * I / N
    return [-bSI, bSI - sigma * E, sigma * E - gamma * I, gamma * I]


def y0_of(dis):
    N = dis["N"]
    return [N - dis["E0"] - dis["I0"] - dis["R_init"], dis["E0"], dis["I0"], dis["R_init"]]


def solve(dis, t, rtol=1e-13, atol=1e-13):
    return odeint(seir_rhs, y0_of(dis), t, args=(dis["beta"], dis["sigma"], dis["gamma"], dis["N"]),
                  rtol=rtol, atol=atol)


def pilot_solve(dis):
    t = np.linspace(0.0, dis["T"], PILOT_N_PTS)
    return t, solve(dis, t, PILOT_RTOL, PILOT_ATOL)


def auto_tune(dis, t_ref, sol_ref):
    """Anchor days and per-compartment scales (unchanged from the original)."""
    N, T = dis["N"], dis["T"]
    sol_fr = sol_ref / N
    pk_idx = np.argmax(sol_ref[:, 2])
    pk_day = float(t_ref[pk_idx])
    comp_scales = [max(float(sol_fr[:, k].max()), 0.005) for k in range(4)]
    pre = pk_day * 0.55
    pk_end = min(pk_day * 1.30, T * 0.96)
    anc_t = np.unique(np.concatenate([
        np.linspace(0.0, pre, 7),
        np.linspace(pre + (pk_end - pre) * 0.05, pk_end, 15),
        np.array([min(pk_end + (T - pk_end) * 0.4, T - 1.0), T]),
    ]))
    anc_t = anc_t[(anc_t >= 0.0) & (anc_t <= T)]
    return {"comp_scales": comp_scales, "anchor_days": anc_t, "peak_day": pk_day, "tau_ic": 0.05}


def build_cwac_collocation(t_pilot, sol_pilot, dis, n_pts, eps, rng, device):
    N, T = dis["N"], dis["T"]
    curv = np.zeros(len(t_pilot))
    for k in range(4):
        d1 = np.gradient(sol_pilot[:, k] / N, t_pilot)
        curv += np.abs(np.gradient(d1, t_pilot))
    curv /= (curv.max() + 1e-30)
    pdf = curv + eps
    pdf /= pdf.sum()
    idx = rng.choice(len(t_pilot), size=n_pts, replace=True, p=pdf)
    cell_w = np.empty(len(t_pilot))
    cell_w[:-1] = np.diff(t_pilot)
    cell_w[-1] = cell_w[-2]
    tc = np.sort(np.clip(t_pilot[idx] + (rng.random(n_pts) - 0.5) * cell_w[idx], 0.0, T))
    wc = np.interp(tc, t_pilot, curv) + eps
    wc /= wc.mean()
    return (torch.tensor(tc.reshape(-1, 1) / T, dtype=DTYPE, device=device),
            torch.tensor(wc.reshape(-1, 1), dtype=DTYPE, device=device))


# ══════════════════════════════════════════════════════════════════════════
#  LOSSES — explicit differential residual r = (1/T) du/dtau - f(u; theta)
# ══════════════════════════════════════════════════════════════════════════

class Rates(nn.Module):
    """Epidemic rates. Known rates are fixed buffers; unknown ones are learned
    through a log parametrisation, initialised at `init` (never at the truth)."""
    def __init__(self, dis, learn=(), init=None):
        super().__init__()
        init = init or {}
        self.learn = tuple(learn)
        for k in ("beta", "sigma", "gamma"):
            if k in self.learn:
                setattr(self, "log_" + k, nn.Parameter(torch.tensor(math.log(init[k]))))
            else:
                self.register_buffer("c_" + k, torch.tensor(float(dis[k])))

    def get(self, k):
        return torch.exp(getattr(self, "log_" + k)) if k in self.learn else getattr(self, "c_" + k)


def residual(model, rates, tau, T, create_graph=True):
    tau = tau.detach().requires_grad_(True)
    u = model(tau)
    S, E, I, R = u[:, 0:1], u[:, 1:2], u[:, 2:3], u[:, 3:4]

    def ddt(f):
        return torch.autograd.grad(f, tau, grad_outputs=torch.ones_like(f),
                                   create_graph=create_graph, retain_graph=True)[0] / T

    beta, sigma, gamma = rates.get("beta"), rates.get("sigma"), rates.get("gamma")
    return torch.cat([ddt(S) - (-beta * S * I),
                      ddt(E) - (beta * S * I - sigma * E),
                      ddt(I) - (sigma * E - gamma * I),
                      ddt(R) - (gamma * I)], dim=1)


class Problem:
    """Everything a training run needs: collocation, data term, scales."""
    def __init__(self, dis, tau_c, w_c, tau_obs, y_obs, obs_cols, comp_scales, rates, device):
        self.dis, self.T = dis, dis["T"]
        self.tau_c, self.w_c = tau_c, w_c
        self.tau_obs, self.y_obs = tau_obs, y_obs
        self.obs_cols = obs_cols
        self.cs = torch.tensor([comp_scales], dtype=DTYPE, device=device)
        self.cs_obs = self.cs[:, obs_cols]
        self.rates = rates
        self.w_phys = 1.0  # physics-term weight (raised for the sparse real-data problem)

    def loss(self, model, w_anchor, w_c=None, create_graph=True):
        w_c = self.w_c if w_c is None else w_c
        r = residual(model, self.rates, self.tau_c, self.T, create_graph) / self.cs
        loss_ph = (w_c * (r ** 2).sum(dim=1, keepdim=True)).mean()
        pred = model(self.tau_obs)[:, self.obs_cols]
        loss_an = (((pred - self.y_obs) / self.cs_obs) ** 2).mean()
        return self.w_phys * loss_ph + w_anchor * loss_an, loss_ph, loss_an


# ══════════════════════════════════════════════════════════════════════════
#  TRAINING (identical schedule to the original notebooks)
# ══════════════════════════════════════════════════════════════════════════

def train(model, prob, budget, log_every=0, label="", legacy_lbfgs=False):
    """legacy_lbfgs=True reproduces the original notebooks, whose L-BFGS closure
    called autograd.grad(create_graph=False): du/dtau is then detached, so the
    L-BFGS gradient ignores the derivative part of the physics residual."""
    hist = {"total": [], "phys": [], "anchor": []}
    params = list(model.parameters()) + list(prob.rates.parameters())
    n1, n2, n3 = budget["n_p1"], budget["n_p2"], budget["n_lbfgs"]
    WARMUP, LR_SEED, LR_PEAK, LR_P1_END, LR_P2_END = max(1, n1 // 4), 1e-6, 2e-4, 8e-6, 3e-7
    # rates (inverse mode) share the EMA so phase 3 starts from a consistent state
    ema_target = nn.ModuleList([model, prob.rates])
    ema = EMA(ema_target, 0.999)

    def lr1(s):
        if s < WARMUP:
            return LR_SEED + (LR_PEAK - LR_SEED) * s / WARMUP
        q = (s - WARMUP) / max(1, n1 - WARMUP)
        return LR_P1_END + (LR_PEAK - LR_P1_END) * 0.5 * (1 + np.cos(np.pi * q))

    def lr2(s):
        q = s / max(1, n2 - 1)
        return LR_P2_END + (LR_P1_END - LR_P2_END) * 0.5 * (1 + np.cos(np.pi * q))

    def rec(tot, ph, an):
        hist["total"].append(tot.item())
        hist["phys"].append(ph.item())
        hist["anchor"].append(an.item())

    # unknown epidemic rates (inverse mode) use a larger Adam step; LambdaLR
    # scales each group's base lr, so the schedule shape is shared
    groups = [{"params": list(model.parameters()), "lr": 1.0}]
    if len(list(prob.rates.parameters())):
        groups.append({"params": list(prob.rates.parameters()), "lr": RATE_LR_MULT})
    for phase, n, lrf, clip in ((1, n1, lr1, 1.0), (2, n2, lr2, 0.5)):
        opt = torch.optim.Adam(groups, lr=1.0)
        lrfs = [lrf] * len(groups)
        if phase == 1 and len(groups) > 1:
            # rates stay at their initial guess until the network has fitted the data
            lrfs[1] = lambda s, f=lrf: 0.0 if s < RATE_FREEZE else f(s)
        sch = torch.optim.lr_scheduler.LambdaLR(opt, lrfs)
        for ep in range(n):
            wa = 10.0 if phase == 1 else 10.0 * (0.1 ** (ep / max(1, n2 - 1)))
            opt.zero_grad()
            tot, ph, an = prob.loss(model, wa)
            tot.backward()
            torch.nn.utils.clip_grad_norm_(params, clip)
            opt.step(); sch.step(); ema.update(ema_target)
            rec(tot, ph, an)
            if log_every and ep % log_every == 0:
                print(f"  [{label} P{phase} {ep:5d}] tot={tot.item():.3e} ph={ph.item():.3e} an={an.item():.3e}",
                      flush=True)
    ema.apply_to(ema_target)

    opt3 = torch.optim.LBFGS(params, max_iter=n3, tolerance_grad=1e-12, tolerance_change=1e-14,
                             history_size=150, line_search_fn="strong_wolfe")
    cnt = [0]
    ones = torch.ones_like(prob.w_c)

    def closure():
        opt3.zero_grad()
        tot, ph, an = prob.loss(model, 1.0, w_c=ones, create_graph=not legacy_lbfgs)
        tot.backward()
        rec(tot, ph, an)
        cnt[0] += 1
        return tot

    if n3 > 0:
        opt3.step(closure)
    return hist, cnt[0]


# ══════════════════════════════════════════════════════════════════════════
#  EVALUATION
# ══════════════════════════════════════════════════════════════════════════

def r2(ref, pred):
    return float(1.0 - np.sum((ref - pred) ** 2) / np.sum((ref - ref.mean()) ** 2))


def evaluate(model, dis, comp_scales, device, n_eval=1000, n_grid=6000):
    """Metrics against the true trajectory (true parameters)."""
    N, T = dis["N"], dis["T"]
    t_e = np.linspace(0.0, T, n_eval)
    tau_e = torch.tensor((t_e / T).reshape(-1, 1), dtype=DTYPE, device=device)
    model.eval()
    with torch.no_grad():
        up = (model(tau_e) * N).cpu().numpy()
    sol = solve(dis, t_e)
    out = {"t": t_e, "pred": up, "ref": sol}
    for k, nm in enumerate("SEIR"):
        p, r = up[:, k], sol[:, k]
        out[nm] = {"mse": float(np.mean((p - r) ** 2)), "r2": r2(r, p),
                   "rel": float(np.linalg.norm(p - r) / (np.linalg.norm(r) + 1e-12))}
    out["mean_rel"] = float(np.mean([out[nm]["rel"] for nm in "SEIR"]))
    out["peak_err"] = abs(up[:, 2].max() - sol[:, 2].max()) / sol[:, 2].max() * 100.0
    out["peak_day_err"] = abs(t_e[np.argmax(up[:, 2])] - t_e[np.argmax(sol[:, 2])])
    # physics residual on a dense uniform grid with the TRUE parameters
    true_rates = Rates(dis).to(device)
    tau_g = torch.tensor(np.linspace(0, 1, n_grid).reshape(-1, 1), dtype=DTYPE, device=device)
    cs = torch.tensor([comp_scales], dtype=DTYPE, device=device)
    r = residual(model, true_rates, tau_g, T, create_graph=False) / cs
    out["phys_res"] = float((r ** 2).sum(dim=1).mean().item())
    return out


def summarise(ev):
    """Scalar subset of an evaluation (JSON-friendly)."""
    d = {nm: ev[nm] for nm in "SEIR"}
    for k in ("mean_rel", "peak_err", "peak_day_err", "phys_res"):
        d[k] = float(ev[k])
    return d
