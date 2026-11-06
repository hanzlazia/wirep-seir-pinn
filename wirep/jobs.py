"""One training job = one (experiment, disease, activation, seed, setting).
Results are written to results/<exp>/<job_id>.json (+ .npz trajectories),
so the whole study is resumable and every number in the paper is traceable
to a file."""
import json
import math
import os
import time

import numpy as np
import torch

from . import core
from .core import DTYPE
from .data import REAL_DATASETS


def job_id(j):
    parts = [j["exp"], j["disease"], j["act"], f"s{j['seed']}"]
    if j.get("noise"):
        parts.append(f"n{j['noise']}")
    if j.get("layers"):
        parts.append("L" + "x".join(map(str, j["layers"][1:-1])))
    if j.get("legacy"):
        parts.append("legacy")
    return "_".join(p.replace("/", "-").replace("(", "").replace(")", "").replace("=", "")
                    for p in parts)


def out_paths(root, j):
    d = os.path.join(root, j["exp"])
    os.makedirs(d, exist_ok=True)
    jid = job_id(j)
    return os.path.join(d, jid + ".json"), os.path.join(d, jid + ".npz")


def _bw_hint(T):
    t_pilot = np.linspace(0.0, T, core.PILOT_N_PTS)
    return float(np.mean(np.diff(t_pilot)) / T / 2.0)


def _u0(dis, device):
    N = dis["N"]
    return torch.tensor([core.y0_of(dis)], dtype=DTYPE, device=device) / N


def setup_forward(j, device):
    """Forward problem exactly as in the original study: known parameters,
    24 anchors of all four compartments from the reference solution
    (optionally corrupted with multiplicative noise), CWAC collocation."""
    dis = core.DISEASES[j["disease"]]
    N, T = dis["N"], dis["T"]
    t_ref = np.linspace(0.0, T, 10001)
    sol_ref = core.solve(dis, t_ref)
    tune = core.auto_tune(dis, t_ref, sol_ref)
    anc_idx = np.clip(np.searchsorted(t_ref, tune["anchor_days"]), 0, len(sol_ref) - 1)
    u_anc = sol_ref[anc_idx] / N
    if j.get("noise"):
        nrng = np.random.default_rng(10_000 + j["seed"])
        u_anc = np.clip(u_anc * (1.0 + nrng.normal(0.0, j["noise"], u_anc.shape)), 0.0, None)
    rng = np.random.default_rng(j["seed"])
    t_pilot, sol_pilot = core.pilot_solve(dis)
    tau_c, w_c = core.build_cwac_collocation(t_pilot, sol_pilot, dis, core.N_COLLOC, core.EPS_FLOOR,
                                             rng, device)
    prob = core.Problem(dis, tau_c, w_c,
                        torch.tensor((tune["anchor_days"] / T).reshape(-1, 1), dtype=DTYPE, device=device),
                        torch.tensor(u_anc, dtype=DTYPE, device=device), [0, 1, 2, 3],
                        tune["comp_scales"], core.Rates(dis).to(device), device)
    return dis, prob, tune["comp_scales"], tune["tau_ic"]


INV_INIT = {"beta": 0.2, "gamma": 0.1}  # generic prior guess (R0 = 2), same for every disease
INV_OBS_EVERY = 2.0                      # one observation of I every 2 days
REAL_W_PHYS = 1000.0                     # physics weight for real data: with 10 sparse points, weight 1 lets the network fit the data while violating the ODE
N_COLLOC_INV = 2000                      # uniform collocation for inverse / real-data runs


def setup_inverse(j, device):
    """Inverse problem on synthetic data: only I(t) is observed (every 2 days,
    multiplicative noise), beta and gamma are unknown and learned; sigma is
    known. No S, E or R information and no reference-solution anchors are used;
    collocation is uniform because CWAC would require the unknown parameters."""
    dis = core.DISEASES[j["disease"]]
    N, T = dis["N"], dis["T"]
    t_obs = np.arange(INV_OBS_EVERY, T + 1e-9, INV_OBS_EVERY)
    I_true = core.solve(dis, np.concatenate([[0.0], t_obs]))[1:, 2] / N
    nrng = np.random.default_rng(20_000 + j["seed"])
    I_obs = np.clip(I_true * (1.0 + nrng.normal(0.0, j.get("noise", 0.0), I_true.shape)), 0.0, None)
    imax = float(I_obs.max())
    cs = [1.0, imax, imax, 1.0]
    tau_c = torch.tensor(np.linspace(0, 1, N_COLLOC_INV).reshape(-1, 1), dtype=DTYPE, device=device)
    rates = core.Rates(dis, learn=("beta", "gamma"), init=INV_INIT).to(device)
    prob = core.Problem(dis, tau_c, torch.ones_like(tau_c),
                        torch.tensor((t_obs / T).reshape(-1, 1), dtype=DTYPE, device=device),
                        torch.tensor(I_obs.reshape(-1, 1), dtype=DTYPE, device=device), [2], cs, rates, device)
    return dis, prob, cs, 0.05


def setup_real(j, device):
    """Real outbreak data: I(t) observed, beta, sigma, gamma all unknown.
    Days > train_days are held out for forecasting."""
    ds = REAL_DATASETS[j["disease"]]
    N, T = ds["N"], ds["T"]
    t_all, y_all = np.asarray(ds["t"], float), np.asarray(ds["I"], float) / N
    tr = t_all <= ds["train_days"]
    dis = dict(name=ds["name"], N=N, T=T, E0=ds["E0"], I0=ds["I0"], R_init=0.0,
               beta=float("nan"), sigma=float("nan"), gamma=float("nan"))
    imax = float(y_all[tr].max())
    cs = [1.0, imax, imax, 1.0]
    tau_c = torch.tensor(np.linspace(0, 1, N_COLLOC_INV).reshape(-1, 1), dtype=DTYPE, device=device)
    rates = core.Rates(dis, learn=("beta", "sigma", "gamma"), init=ds["init"]).to(device)
    prob = core.Problem(dis, tau_c, torch.ones_like(tau_c),
                        torch.tensor((t_all[tr] / T).reshape(-1, 1), dtype=DTYPE, device=device),
                        torch.tensor(y_all[tr].reshape(-1, 1), dtype=DTYPE, device=device), [2], cs,
                        rates, device)
    prob.w_phys = REAL_W_PHYS
    return dis, prob, cs, ds.get("tau_ic", 0.05), ds


def run_job(j, root, device, budget=None, log_every=0):
    jpath, npath = out_paths(root, j)
    if os.path.exists(jpath):
        return json.load(open(jpath))
    budget = budget or core.BUDGET
    layers = tuple(j.get("layers") or core.LAYERS)
    kind = j.get("kind", "forward")
    ds = None
    if kind == "forward":
        dis, prob, cs, tau_ic = setup_forward(j, device)
    elif kind == "inverse":
        dis, prob, cs, tau_ic = setup_inverse(j, device)
    else:
        dis, prob, cs, tau_ic, ds = setup_real(j, device)

    model = core.build_model(j["act"], layers, _u0(dis, device), tau_ic, _bw_hint(dis["T"]), j["seed"], device)
    t0 = time.time()
    hist, n_lbfgs = core.train(model, prob, budget, log_every=log_every, label=job_id(j),
                               legacy_lbfgs=bool(j.get("legacy")))
    if device.type == "cuda":
        torch.cuda.synchronize()
    elapsed = time.time() - t0
    res = {"job": j, "id": job_id(j), "train_time": elapsed, "lbfgs_evals": n_lbfgs,
           "final_loss": hist["total"][-1], "final_phys": hist["phys"][-1], "final_anchor": hist["anchor"][-1],
           "device": str(device)}
    learned = {k: float(prob.rates.get(k).item()) for k in ("beta", "sigma", "gamma")}
    res["rates"] = learned
    sub = lambda a: np.asarray(a)[:: max(1, len(a) // 2000)]
    arrays = {"hist_total": sub(hist["total"]), "hist_phys": sub(hist["phys"]), "hist_anchor": sub(hist["anchor"])}

    if kind == "real":
        T, N = ds["T"], ds["N"]
        t_d = np.asarray(ds["t"], float)
        y_d = np.asarray(ds["I"], float)
        t_f = np.linspace(0.0, T, 600)
        model.eval()
        with torch.no_grad():
            pf = (model(torch.tensor((t_f / T).reshape(-1, 1), dtype=DTYPE, device=device)) * N).cpu().numpy()
            pd = (model(torch.tensor((t_d / T).reshape(-1, 1), dtype=DTYPE, device=device)) * N).cpu().numpy()[:, 2]
        tr = t_d <= ds["train_days"]
        res["rmse_train"] = float(np.sqrt(np.mean((pd[tr] - y_d[tr]) ** 2)))
        res["rmse_test"] = float(np.sqrt(np.mean((pd[~tr] - y_d[~tr]) ** 2))) if (~tr).any() else float("nan")
        res["R0"] = learned["beta"] / learned["gamma"] if learned["gamma"] > 0 else float("inf")
        # self-consistency: ODE re-integrated with the learned rates vs the network
        dis_l = dict(dis, **learned)
        sol_l = core.solve(dis_l, t_f)
        res["pinn_vs_ode_rel"] = float(np.linalg.norm(pf[:, 2] - sol_l[:, 2]) / np.linalg.norm(sol_l[:, 2]))
        sol_ld = core.solve(dis_l, np.concatenate([[0.0], t_d]))[1:, 2]
        res["ode_rmse_train"] = float(np.sqrt(np.mean((sol_ld[tr] - y_d[tr]) ** 2)))
        res["ode_rmse_test"] = float(np.sqrt(np.mean((sol_ld[~tr] - y_d[~tr]) ** 2))) if (~tr).any() else float("nan")
        arrays.update(t=t_f, pred=pf, ode_learned=sol_l)
    else:
        ev = core.evaluate(model, dis, cs, device)
        res.update(core.summarise(ev))
        arrays.update(t=ev["t"], pred=ev["pred"].astype(np.float64))
        if kind == "inverse":
            res["beta_err"] = abs(learned["beta"] - dis["beta"]) / dis["beta"] * 100
            res["gamma_err"] = abs(learned["gamma"] - dis["gamma"]) / dis["gamma"] * 100
            R0_true = dis["beta"] / dis["gamma"]
            res["R0"] = learned["beta"] / learned["gamma"] if learned["gamma"] > 0 else float("inf")
            res["R0_err"] = abs(res["R0"] - R0_true) / R0_true * 100

    np.savez_compressed(npath, **arrays)
    tmp = jpath + ".tmp"
    with open(tmp, "w") as f:
        json.dump(res, f, indent=1, default=float)
    os.replace(tmp, jpath)
    return res
