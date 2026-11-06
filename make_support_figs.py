"""Supporting figures/tables built from the existing result files (no new training):
bootstrap forest plot, inverse failure rates, accuracy-vs-cost, phase ablation pairs, per-compartment ratios."""
import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import analyze as A

FIG, TAB = A.FIG, A.TAB
DIS = ["Hantavirus", "SARS-2003", "COVID-19"]
BLUE, GREY, RED = "#1a6eb5", "#8a8a8a", "#b2182b"
plt.rcParams.update({"font.family": "serif", "font.size": 9, "axes.grid": True, "grid.alpha": 0.25,
                     "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False})
rng = np.random.default_rng(0)
df = A.load()
fw = df[df.exp == "E1_main"]


def boot_ratio(a, b, n=10000):
    d = np.log(a) - np.log(b)
    idx = rng.integers(0, len(d), (n, len(d)))
    m = d[idx].mean(1)
    return np.exp(d.mean()), np.exp(np.percentile(m, 2.5)), np.exp(np.percentile(m, 97.5))


def fig_forest():
    others = ["WIRE-P-A", "WIRE-P(phi=0)", "MV-Morlet", "MV-Morlet-A", "MV-Morlet+", "Tanh", "ReLU", "Sigmoid", "SIREN", "Fourier"]
    labels = ["WIRE-P-A", "WIRE-P ($\\phi{=}0$)", "MV-Morlet", "MV-Morlet-A", "MV-Morlet+", "Tanh", "ReLU", "Sigmoid", "SIREN", "Fourier"]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), sharey=True)
    rows = []
    for ax, d in zip(axes, DIS):
        s = fw[fw.disease == d]
        a = s[s.act == "WIRE-P"].set_index("seed").mean_rel
        for k, o in enumerate(others):
            b = s[s.act == o].set_index("seed").mean_rel
            c = a.index.intersection(b.index)
            r, lo, hi = boot_ratio(a.loc[c].values, b.loc[c].values)
            col = BLUE if hi < 1 else (RED if lo > 1 else GREY)
            ax.plot([lo, hi], [k, k], color=col, lw=2)
            ax.plot(r, k, "o", color=col, ms=5)
            rows.append((d, o, r, lo, hi))
        ax.axvline(1, color="k", lw=0.8)
        ax.set_xscale("log")
        ax.set_xlim(0.05, 3)
        ax.set_title(d)
        ax.set_xlabel("Error ratio WIRE-P / other (below 1 favours WIRE-P)")
        ax.set_yticks(range(len(others)))
        ax.set_yticklabels(labels)
        ax.invert_yaxis()
    for ax, l in zip(axes, "abc"):
        ax.text(-0.02, 1.04, f"({l})", transform=ax.transAxes, fontsize=10, fontweight="bold", ha="right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_forest_ratio.png"), dpi=300)
    plt.close(fig)
    pd.DataFrame(rows, columns=["disease", "other", "ratio", "lo", "hi"]).to_csv(os.path.join(TAB, "forest_ratio.csv"), index=False)
    return pd.DataFrame(rows, columns=["disease", "other", "ratio", "lo", "hi"])


def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


def fig_failure():
    inv = df[df.exp == "E4_inverse"].copy()
    inv["fail"] = inv.beta_err > 50
    acts = ["WIRE-P", "WIRE-P-A", "MV-Morlet", "Tanh", "Sigmoid"]
    noises = sorted(inv.noise.unique())
    cols = ["#1a6eb5", "#e07b00", "#b2182b"]
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    w = 0.26
    out = []
    for k, nz in enumerate(noises):
        for i, a in enumerate(acts):
            s = inv[(inv.act == a) & (inv.noise == nz)]
            f, n = int(s.fail.sum()), len(s)
            lo, hi = wilson(f, n)
            x = i + (k - 1) * w
            ax.bar(x, 100 * f / n, w * 0.9, color=cols[k], label=f"{int(round(nz * 100))}% noise" if i == 0 else None)
            ax.plot([x, x], [100 * lo, 100 * hi], color="k", lw=0.9)
            out.append((a, nz, f, n))
    ax.set_xticks(range(len(acts)))
    ax.set_xticklabels(acts)
    ax.set_ylabel("Failed runs (%)")
    ax.set_ylim(0, 105)
    ax.legend(ncol=3, loc="upper left", fontsize=8)
    ax.set_title("Inverse problem, 30 runs per bar (3 diseases $\\times$ 10 seeds); bars show 95% Wilson intervals", fontsize=8.5)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_failure_rate.png"), dpi=300)
    plt.close(fig)
    return out


def fig_cost():
    acts = ["WIRE-P", "WIRE-P-A", "WIRE-P(phi=0)", "MV-Morlet", "MV-Morlet-A", "MV-Morlet+", "Tanh", "ReLU", "Sigmoid", "SIREN", "Fourier"]
    pts = {}
    for a in acts:
        s = fw[fw.act == a]
        err = np.exp(np.mean([np.log(s[s.disease == d].mean_rel).mean() for d in DIS]))
        tm = np.mean([s[s.disease == d].time.mean() for d in DIS]) / 60
        pts[a] = (tm, err)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for a, (x, y) in pts.items():
        c = BLUE if a.startswith("WIRE") else GREY
        ax.plot(x, y, "o", color=c, ms=6)
        lab = {"MV-Morlet-A": "-A", "MV-Morlet+": "+", "WIRE-P(phi=0)": "WIRE-P ($\\phi{=}0$)"}.get(a, a)
        off = (-14, -12) if a == "MV-Morlet" else (5, 4)
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=off, fontsize=7.5)
    ax.set_yscale("log")
    ax.set_xlabel("Mean training time per run (minutes)")
    ax.set_ylabel("Error (geometric mean over\n3 diseases and 10 seeds)")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_cost_accuracy.png"), dpi=300)
    plt.close(fig)
    return pts


def fig_phase():
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 3.2), sharey=False)
    for ax, d in zip(axes, DIS):
        s = fw[fw.disease == d]
        a = s[s.act == "WIRE-P(phi=0)"].set_index("seed").mean_rel
        b = s[s.act == "WIRE-P"].set_index("seed").mean_rel
        c = a.index.intersection(b.index)
        for sd in c:
            ax.plot([0, 1], [a[sd], b[sd]], color=BLUE if b[sd] < a[sd] else RED, lw=1, alpha=0.8, marker="o", ms=3)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["without\nphase", "with\nphase"])
        ax.set_yscale("log")
        ax.set_title(f"{d}: lower in {int((b.loc[c] < a.loc[c]).sum())} of {len(c)}", fontsize=9)
        ax.set_xlim(-0.3, 1.3)
    axes[0].set_ylabel("Mean relative $L_2$ error")
    for ax, l in zip(axes, "abc"):
        ax.text(-0.02, 1.04, f"({l})", transform=ax.transAxes, fontsize=10, fontweight="bold", ha="right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_phase_pairs.png"), dpi=300)
    plt.close(fig)


def tab_compartments():
    lines = ["\\begin{tabular}{lcccccccc}", "\\toprule",
             " & \\multicolumn{4}{c}{WIRE-P / MV-Morlet} & \\multicolumn{4}{c}{WIRE-P / Tanh} \\\\",
             "\\cmidrule(lr){2-5}\\cmidrule(lr){6-9}",
             "Disease & $s$ & $e$ & $i$ & $r$ & $s$ & $e$ & $i$ & $r$ \\\\", "\\midrule"]
    res = []
    for d in DIS:
        s = fw[fw.disease == d]
        cells = []
        for o in ("MV-Morlet", "Tanh"):
            for nm in "SEIR":
                a = s[s.act == "WIRE-P"].set_index("seed")["rel_" + nm]
                b = s[s.act == o].set_index("seed")["rel_" + nm]
                c = a.index.intersection(b.index)
                r = np.exp(np.mean(np.log(a.loc[c].values) - np.log(b.loc[c].values)))
                w = int((a.loc[c] < b.loc[c]).sum())
                cells.append(f"\\textbf{{{r:.2f}}}" if r < 1 else f"{r:.2f}")
                res.append((d, o, nm, r, w))
        lines.append(d + " & " + " & ".join(cells) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    A.write("tab_compartments.tex", "\n".join(lines))
    return res


if __name__ == "__main__":
    f = fig_forest()
    print(f.round(3).to_string())
    print(fig_failure())
    print({k: (round(v[0], 1), float('%.3g' % v[1])) for k, v in fig_cost().items()})
    fig_phase()
    for r in tab_compartments():
        print(r)
