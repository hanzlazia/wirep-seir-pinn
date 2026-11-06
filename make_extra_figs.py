"""Extra figures for the paper: forward solutions and errors, training curves, inverse-problem
reconstruction, and the training schedule. Reads results/*.npz|json, writes results/figs/."""
import glob
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from wirep import core

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
FIG = os.path.join(ROOT, "figs")
DIS = ["Hantavirus", "SARS-2003", "COVID-19"]
SEEDS = [42, 7, 123, 2024, 314, 1, 2, 3, 4, 5]
COL = {"WIRE-P": "#1a6eb5", "MV-Morlet": "#e07b00", "Tanh": "#7f7f7f", "Sigmoid": "#b2182b",
       "SIREN": "#6a3d9a", "Fourier": "#33a02c", "ReLU": "#a6761d"}
plt.rcParams.update({"font.family": "serif", "font.size": 9, "axes.grid": True, "grid.alpha": 0.25,
                     "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False})


def npz(exp, d, a, s, tag=""):
    p = os.path.join(ROOT, exp, f"{exp}_{d}_{a}_s{s}{tag}.npz")
    return np.load(p) if os.path.exists(p) else None


def fig_forward():
    fig, axes = plt.subplots(2, 3, figsize=(12, 5.6), gridspec_kw={"height_ratios": [1, 1.05]})
    for j, d in enumerate(DIS):
        dis = core.DISEASES[d]
        t0 = npz("E1_main", d, "WIRE-P", 42)["t"]
        ref = core.solve(dis, t0) / dis["N"]
        ax = axes[0, j]
        ax.plot(t0, ref[:, 2] * 100, color="k", lw=2.4, label="Reference (ODE solver)")
        p = npz("E1_main", d, "WIRE-P", 42)["pred"] / dis["N"]
        ax.plot(t0, p[:, 2] * 100, color=COL["WIRE-P"], lw=1.4, ls="--", label="WIRE-P (seed 42)")
        ax.set_title(d)
        ax.set_ylabel("Infectious fraction $i(t)$ (%)" if j == 0 else "")
        ax.set_xlabel("Day")
        if j == 0:
            ax.legend(fontsize=8)
        ax = axes[1, j]
        for a in ["WIRE-P", "MV-Morlet", "Tanh", "Sigmoid"]:
            E = []
            for s in SEEDS:
                z = npz("E1_main", d, a, s)
                if z is not None:
                    E.append(np.abs(z["pred"][:, 2] / dis["N"] - ref[:, 2]) / ref[:, 2].max())
            E = np.array(E)
            ax.plot(t0, np.median(E, 0), color=COL[a], lw=1.5, label=a)
            ax.fill_between(t0, np.percentile(E, 25, 0), np.percentile(E, 75, 0), color=COL[a], alpha=0.12, lw=0)
        ax.set_yscale("log")
        ax.set_ylim(1e-7, 3e-2)
        ax.set_xlabel("Day")
        ax.set_ylabel("$|i_\\mathrm{pred}-i_\\mathrm{ref}|\\,/\\,\\max i_\\mathrm{ref}$" if j == 0 else "")
        if j == 0:
            ax.legend(fontsize=8, ncol=2, loc="upper left")
    for ax, l in zip(axes.ravel(), "abcdef"):
        ax.text(-0.02, 1.04, f"({l})", transform=ax.transAxes, fontsize=10, fontweight="bold", va="bottom", ha="right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_forward_solution_error.png"), dpi=300)
    plt.close(fig)


def fig_training():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.4), sharey=False)
    for j, d in enumerate(DIS):
        ax = axes[j]
        for a in ["WIRE-P", "MV-Morlet", "Tanh", "SIREN", "Fourier", "ReLU"]:
            H = [npz("E1_main", d, a, s)["hist_total"] for s in SEEDS if npz("E1_main", d, a, s) is not None]
            n = min(len(h) for h in H)
            H = np.array([h[:n] for h in H])
            ax.plot(np.arange(n), np.median(H, 0), color=COL[a], lw=1.4, label=a)
        ax.set_yscale("log")
        ax.set_title(d)
        ax.set_xlabel("Logged training step (Adam, then L-BFGS)")
        if j == 0:
            ax.set_ylabel("Total loss (median of 10 seeds)")
            ax.legend(fontsize=8, ncol=2)
        ax.text(-0.02, 1.04, f"({'abc'[j]})", transform=ax.transAxes, fontsize=10, fontweight="bold", ha="right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_training_curves.png"), dpi=300)
    plt.close(fig)


def fig_inverse_fit(d="COVID-19", noise_tag="_n0.05"):
    dis = core.DISEASES[d]
    # first seed on which tanh collapsed but WIRE-P did not
    seed = None
    for s in SEEDS:
        jt = os.path.join(ROOT, "E4_inverse", f"E4_inverse_{d}_Tanh_s{s}{noise_tag}.json")
        jw = os.path.join(ROOT, "E4_inverse", f"E4_inverse_{d}_WIRE-P_s{s}{noise_tag}.json")
        if os.path.exists(jt) and os.path.exists(jw):
            if json.load(open(jt))["beta_err"] > 50 and json.load(open(jw))["beta_err"] < 50:
                seed = s
                break
    if seed is None:
        return
    t = npz("E4_inverse", d, "WIRE-P", seed, noise_tag)["t"]
    ref = core.solve(dis, t) / dis["N"]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    names = ["Susceptible $s(t)$", "Infectious $i(t)$ (observed)", "Recovered $r(t)$"]
    idx = [0, 2, 3]
    info = {}
    for a in ["WIRE-P", "Tanh"]:
        z = npz("E4_inverse", d, a, seed, noise_tag)
        r = json.load(open(os.path.join(ROOT, "E4_inverse", f"E4_inverse_{d}_{a}_s{seed}{noise_tag}.json")))
        info[a] = (z["pred"] / dis["N"], r)
    for ax, k, nm in zip(axes, idx, names):
        ax.plot(t, ref[:, k], color="k", lw=2.4, label="Reference")
        ax.plot(t, info["WIRE-P"][0][:, k], color=COL["WIRE-P"], lw=1.5, ls="--",
                label=f"WIRE-P ($\\hat\\beta$ error {info['WIRE-P'][1]['beta_err']:.1f}%)")
        ax.plot(t, info["Tanh"][0][:, k], color=COL["Tanh"], lw=1.5, ls=":",
                label=f"Tanh, collapsed ($\\hat\\beta$ error {info['Tanh'][1]['beta_err']:.0f}%)")
        ax.set_title(nm)
        ax.set_xlabel("Day")
    axes[0].set_ylabel("Fraction of population")
    axes[1].legend(fontsize=7.5, loc="upper right")
    for ax, l in zip(axes, "abc"):
        ax.text(-0.02, 1.04, f"({l})", transform=ax.transAxes, fontsize=10, fontweight="bold", ha="right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_inverse_reconstruction.png"), dpi=300)
    plt.close(fig)
    print("inverse reconstruction seed", seed)


def fig_schedule():
    e1, e2 = 4000, 4000
    ep = np.arange(e1 + e2)
    lr = np.empty(e1 + e2)
    q = e1 // 4
    for i in range(e1):
        lr[i] = 1e-6 + (2e-4 - 1e-6) * i / q if i < q else 8e-6 + (2e-4 - 8e-6) * 0.5 * (1 + np.cos(np.pi * (i - q) / (e1 - q)))
    for i in range(e2):
        lr[e1 + i] = 3e-7 + (8e-6 - 3e-7) * 0.5 * (1 + np.cos(np.pi * i / e2))
    lam = np.concatenate([np.full(e1, 10.0), 10.0 * (1.0 / 10.0) ** (np.arange(e2) / (e2 - 1))])
    fig, ax = plt.subplots(1, 1, figsize=(6.6, 3.0))
    ax.semilogy(ep, lr, color="#1a6eb5", lw=1.8, label="Adam learning rate")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Learning rate", color="#1a6eb5")
    ax2 = ax.twinx()
    ax2.plot(ep, lam, color="#b2182b", lw=1.8, label="Data weight $\\lambda$")
    ax2.set_ylabel("Data weight $\\lambda$", color="#b2182b")
    ax2.set_ylim(0, 17)
    ax2.grid(False)
    ax2.spines["right"].set_visible(True)
    ax.axvline(e1, color="k", lw=0.8, ls="--")
    ax.axvspan(e1 + e2, e1 + e2 + 1500, color="#dddddd", alpha=0.6)
    ax.set_xlim(0, e1 + e2 + 1500)
    for x, s in ((e1 / 2, "Phase 1\nAdam, EMA"), (e1 + e2 / 2, "Phase 2\nAdam, $\\lambda$ decays"),
                 (e1 + e2 + 750, "Phase 3\nL-BFGS,\n$\\lambda=1$")):
        ax.text(x, 4.5e-4, s, ha="center", va="bottom", fontsize=8)
    ax.set_ylim(1e-7, 4e-3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_schedule.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    fig_forward()
    fig_training()
    fig_inverse_fit()
    fig_schedule()
    print("done")
