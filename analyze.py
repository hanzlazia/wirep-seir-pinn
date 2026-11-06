"""Builds every table, figure and statistic of the revised manuscript from results/.

Statistics: for each comparison, paired over matched seeds:
  * exact two-sided Wilcoxon signed-rank test,
  * paired t-test on log10(metric) (errors are log-normally spread),
  * Holm-Bonferroni correction over each table's family of tests.
"""
import glob
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import least_squares

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wirep import core
from wirep.data import REAL_DATASETS
from wirep.experiments import ALL_ACTS, CORE, DISEASES, SEEDS, SEEDS_ORIG

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
TAB = os.path.join(ROOT, "tables")
FIG = os.path.join(ROOT, "figs")
os.makedirs(TAB, exist_ok=True)
os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.family": "serif", "font.size": 10, "savefig.dpi": 300, "axes.grid": True,
                     "grid.alpha": 0.3})
REPORT = []


def say(s=""):
    print(s)
    REPORT.append(s)


def load():
    rows = []
    for f in glob.glob(os.path.join(ROOT, "E*", "*.json")):
        r = json.load(open(f))
        j = r["job"]
        row = dict(exp=j["exp"], disease=j["disease"], act=j["act"], seed=j["seed"],
                   noise=j.get("noise", 0.0) or 0.0, id=r["id"], time=r["train_time"],
                   lbfgs=r["lbfgs_evals"], final_loss=r["final_loss"])
        for k in ("mean_rel", "peak_err", "peak_day_err", "phys_res", "beta_err", "gamma_err", "R0", "R0_err",
                  "rmse_train", "rmse_test", "ode_rmse_train", "ode_rmse_test", "pinn_vs_ode_rel"):
            if k in r:
                row[k] = r[k]
        for nm in "SEIR":
            if nm in r:
                row["rel_" + nm] = r[nm]["rel"]
                row["r2_" + nm] = r[nm]["r2"]
        for k, v in r.get("rates", {}).items():
            row["hat_" + k] = v
        rows.append(row)
    return pd.DataFrame(rows)


def holm(p):
    p = np.asarray(p, float)
    out = np.full_like(p, np.nan)
    ok = ~np.isnan(p)
    idx = np.argsort(p[ok])
    m = ok.sum()
    adj = np.minimum(1.0, np.maximum.accumulate((m - np.arange(m)) * p[ok][idx]))
    tmp = np.empty(m)
    tmp[idx] = adj
    out[ok] = tmp
    return out


def holm_by(R, cols, col="p_w"):
    """Holm adjustment within each family defined by `cols` (one family per disease x metric [x noise])."""
    return R.groupby(list(cols), group_keys=False)[col].transform(lambda p: pd.Series(holm(p.values), index=p.index))


def paired(df, ref, other, metric, keys):
    """Paired test of `ref` vs `other` on `metric`, matched on `keys` (seed[, noise])."""
    a = df[df.act == ref].set_index(keys)[metric]
    b = df[df.act == other].set_index(keys)[metric]
    common = a.index.intersection(b.index)
    a, b = a.loc[common].values, b.loc[common].values
    n = len(a)
    if n < 3:
        return dict(n=n, ratio=np.nan, wins=np.nan, p_w=np.nan, p_t=np.nan)
    la, lb = np.log10(np.maximum(a, 1e-300)), np.log10(np.maximum(b, 1e-300))
    d = la - lb
    p_w = stats.wilcoxon(a, b, alternative="two-sided", method="exact").pvalue if np.any(a != b) else 1.0
    p_t = stats.ttest_rel(la, lb).pvalue
    return dict(n=n, ratio=10 ** d.mean(), wins=int((a < b).sum()), p_w=p_w, p_t=p_t)


def fmt(x, sig=3):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "--"
    if x == 0:
        return "0"
    e = int(np.floor(np.log10(abs(x))))
    if -2 <= e <= 2:
        return f"{x:.{max(0, sig - 1 - e)}f}"
    m = x / 10 ** e
    return f"${m:.{sig - 1}f}\\times10^{{{e}}}$"


def fmt_p(p):
    if np.isnan(p):
        return "--"
    s = "<0.001" if p < 0.001 else f"{p:.3f}"
    return s + ("$^{*}$" if p < 0.05 else "")


def ms(v):
    return f"{fmt(np.mean(v))} $\\pm$ {fmt(np.std(v, ddof=1))}" if len(v) > 1 else fmt(np.mean(v))


def write(name, text):
    open(os.path.join(TAB, name), "w", encoding="utf-8").write(text)


# ══════════════════════════════════════════════════════════════════════
def e0_legacy(df):
    """Reproduction with the original (detached) L-BFGS gradient vs corrected gradient."""
    leg = df[df.exp == "E0_legacy"]
    cor = df[(df.exp == "E1_main") & df.seed.isin(SEEDS_ORIG)]
    if leg.empty:
        return
    say("\n## E0 — reproduction (original detached L-BFGS gradient) vs corrected gradient, 5 original seeds")
    lines = []
    for d in DISEASES:
        for a in ["MV-Morlet", "WIRE-P", "Tanh"]:
            l = leg[(leg.disease == d) & (leg.act == a)]
            c = cor[(cor.disease == d) & (cor.act == a)]
            if l.empty:
                continue
            s = (f"{d:11s} {a:10s} legacy: relL2={l.mean_rel.mean():.3e} peak={l.peak_err.mean():.4f}% "
                 f"phys={l.phys_res.mean():.3e} lbfgs={l.lbfgs.mean():.0f} (n={len(l)})")
            if not c.empty:
                s += (f" | corrected: relL2={c.mean_rel.mean():.3e} peak={c.peak_err.mean():.4f}% "
                      f"phys={c.phys_res.mean():.3e} lbfgs={c.lbfgs.mean():.0f} (n={len(c)})")
            say(s)
            lines.append((d, a, l, c))
    tex = ["\\begin{tabular}{llcccccc}", "\\toprule",
           " & & \\multicolumn{3}{c}{Original L-BFGS gradient} & \\multicolumn{3}{c}{Corrected gradient} \\\\",
           "\\cmidrule(lr){3-5}\\cmidrule(lr){6-8}",
           "Disease & Activation & Rel.\\ $L_2$ & Peak err.\\ (\\%) & L-BFGS evals & Rel.\\ $L_2$ & Peak err.\\ (\\%) & L-BFGS evals \\\\",
           "\\midrule"]
    for d, a, l, c in lines:
        cc = [fmt(c.mean_rel.mean()), fmt(c.peak_err.mean()), f"{c.lbfgs.mean():.0f}"] if not c.empty else ["--"] * 3
        tex.append(f"{d} & {a} & {fmt(l.mean_rel.mean())} & {fmt(l.peak_err.mean())} & {l.lbfgs.mean():.0f} & "
                   + " & ".join(cc) + " \\\\")
    tex += ["\\bottomrule", "\\end{tabular}"]
    write("tab_legacy.tex", "\n".join(tex))


def main_table(df, exp, acts, name, ref="WIRE-P", metrics=("mean_rel", "peak_err", "phys_res"), keys=("seed",)):
    """mean ± sd per activation and paired tests ref-vs-others. Holm family = one disease x metric
    (all comparisons against `ref`); a Holm adjustment over the whole table is kept as a conservative check."""
    sub = df[df.exp == exp]
    if sub.empty:
        return None
    say(f"\n## {exp}: {ref} vs others  (paired over seeds; Holm over {len(DISEASES)}x{len(metrics)}x{len(acts) - 1} tests)")
    recs = []
    for d in sub.disease.unique():
        dd = sub[sub.disease == d]
        for m in metrics:
            for a in acts:
                if a == ref or dd[dd.act == a].empty:
                    continue
                t = paired(dd, ref, a, m, list(keys))
                recs.append(dict(disease=d, metric=m, act=a, **t))
    R = pd.DataFrame(recs)
    if R.empty:
        return R
    R["p_w_holm"] = holm_by(R, ("disease", "metric"))
    R["p_t_holm"] = holm_by(R, ("disease", "metric"), "p_t")
    R["p_w_holm_all"] = holm(R.p_w)
    for _, r in R.iterrows():
        say(f"  {r.disease:11s} {r.metric:9s} {ref} vs {r.act:13s} n={r.n:2d} ratio(GM)={r.ratio:7.3f} "
            f"wins={r.wins}/{r.n} p_W={r.p_w:.4f} p_W,Holm={r.p_w_holm:.4f} p_t,Holm={r.p_t_holm:.4f} "
            f"p_W,all={r.p_w_holm_all:.4f}")
    R.to_csv(os.path.join(TAB, name + "_tests.csv"), index=False)
    return R


def summary_table(df, exp, acts, name, metrics=("mean_rel", "peak_err", "phys_res")):
    sub = df[df.exp == exp]
    if sub.empty:
        return
    labels = {"mean_rel": "Rel.\\ $L_2$", "peak_err": "Peak err.\\ (\\%)", "phys_res": "Phys.\\ res.",
              "time": "Time (s)", "lbfgs": "L-BFGS evals"}
    acts = [a for a in acts if a in set(sub.act)]
    say(f"\n## {exp}: mean ± sd (n seeds)")
    tex = ["\\begin{tabular}{ll" + "c" * len(acts) + "}", "\\toprule",
           "Disease & Metric & " + " & ".join(acts) + " \\\\", "\\midrule"]
    for d in DISEASES:
        dd = sub[sub.disease == d]
        if dd.empty:
            continue
        for m in metrics:
            vals = {a: dd[dd.act == a][m].values for a in acts}
            means = {a: np.mean(v) if len(v) else np.inf for a, v in vals.items()}
            best = min(means, key=means.get)
            cells = []
            for a in acts:
                c = ms(vals[a]) if len(vals[a]) else "--"
                cells.append(f"\\textbf{{{c}}}" if a == best else c)
            say(f"  {d:11s} {m:9s} " + " | ".join(f"{a}={np.mean(v):.3e}±{np.std(v, ddof=1) if len(v) > 1 else 0:.1e}(n={len(v)})"
                                                   for a, v in vals.items() if len(v)))
            tex.append(f"{d} & {labels.get(m, m)} & " + " & ".join(cells) + " \\\\")
        tex.append("\\midrule")
    tex[-1] = "\\bottomrule"
    tex.append("\\end{tabular}")
    write(name + ".tex", "\n".join(tex))


def ranking(df, exp):
    sub = df[df.exp == exp]
    if sub.empty:
        return
    say(f"\n## {exp}: ranking by mean (geometric mean over seeds in brackets)")
    for d in DISEASES:
        dd = sub[sub.disease == d]
        for m in ("mean_rel", "peak_err", "phys_res"):
            g = dd.groupby("act")[m]
            order = g.mean().sort_values()
            gm = g.apply(lambda v: 10 ** np.log10(v).mean())
            say(f"  {d:11s} {m:9s}: " + "  ".join(f"{a}={v:.2e}[{gm[a]:.2e}]" for a, v in order.items()))


# ══════════════════════════════════════════════════════════════════════
def classical_fit_real(name):
    """Reference: least-squares SEIR fit to the same training days (multi-start)."""
    ds = REAL_DATASETS[name]
    t, y = np.asarray(ds["t"], float), np.asarray(ds["I"], float)
    tr = t <= ds["train_days"]
    dis0 = dict(N=ds["N"], E0=ds["E0"], I0=ds["I0"], R_init=0.0)

    def sim(th, tt):
        d = dict(dis0, beta=np.exp(th[0]), sigma=np.exp(th[1]), gamma=np.exp(th[2]))
        return core.solve(d, np.concatenate([[0.0], tt]), 1e-10, 1e-10)[1:, 2]

    best = None
    for b0 in (0.5, 1.0, 2.0, 4.0):
        for s0 in (0.3, 1.0, 3.0):
            for g0 in (0.2, 0.5, 1.0):
                try:
                    r = least_squares(lambda th: sim(th, t[tr]) - y[tr], np.log([b0, s0, g0]))
                except Exception:
                    continue
                if best is None or r.cost < best.cost:
                    best = r
    th = best.x
    p = sim(th, t)
    return dict(beta=np.exp(th[0]), sigma=np.exp(th[1]), gamma=np.exp(th[2]),
                rmse_train=np.sqrt(np.mean((p[tr] - y[tr]) ** 2)), rmse_test=np.sqrt(np.mean((p[~tr] - y[~tr]) ** 2)))


def e5_real(df):
    sub = df[df.exp == "E5_real"]
    if sub.empty:
        return
    name = "BoardingSchool-1978"
    cf = classical_fit_real(name)
    say("\n## E5 real data (1978 boarding-school influenza; days 1-10 train, 11-14 forecast)")
    say(f"  classical least-squares SEIR fit: beta={cf['beta']:.3f} sigma={cf['sigma']:.3f} gamma={cf['gamma']:.3f} "
        f"R0={cf['beta'] / cf['gamma']:.2f} RMSE train={cf['rmse_train']:.2f} test={cf['rmse_test']:.2f}")
    acts = [a for a in ALL_ACTS if a in set(sub.act)]
    tex = ["\\begin{tabular}{lcccccc}", "\\toprule",
           "Method & RMSE train & RMSE forecast & $\\hat\\beta$ & $\\hat\\sigma$ & $\\hat\\gamma$ & $\\hat R_0$ \\\\",
           "& (pupils) & (pupils) & \\multicolumn{4}{c}{(median over seeds)} \\\\",
           "\\midrule",
           f"Least-squares ODE fit & {cf['rmse_train']:.1f} & {cf['rmse_test']:.1f} & {cf['beta']:.2f} & "
           f"{cf['sigma']:.2f} & {cf['gamma']:.2f} & {cf['beta'] / cf['gamma']:.2f} \\\\", "\\midrule"]
    for a in acts:
        s = sub[sub.act == a]
        mr = lambda c, f=1: f"{s[c].mean():.{f}f} $\\pm$ {s[c].std(ddof=1):.{f}f}"
        # sigma and R0 are heavy-tailed (sigma is not identifiable from I(t) alone): report medians, cap at >100
        md = lambda c: (f"{s[c].median():.2f}" if s[c].median() <= 100 else "$>$100")
        say(f"  {a:13s} n={len(s)} RMSE train={s.rmse_train.mean():.2f}±{s.rmse_train.std():.2f} "
            f"forecast={s.rmse_test.mean():.2f}±{s.rmse_test.std():.2f} beta={s.hat_beta.mean():.3f} "
            f"sigma={s.hat_sigma.mean():.3f} gamma={s.hat_gamma.mean():.3f} R0={s.R0.mean():.2f}±{s.R0.std():.2f} "
            f"pinn-vs-ODE={s.pinn_vs_ode_rel.mean():.2e}")
        tex.append(f"{a} & {mr('rmse_train')} & {mr('rmse_test')} & {md('hat_beta')} & {md('hat_sigma')} & "
                   f"{md('hat_gamma')} & {md('R0')} \\\\")
    tex += ["\\bottomrule", "\\end{tabular}"]
    write("tab_real.tex", "\n".join(tex))
    R = []
    for m in ("rmse_train", "rmse_test"):
        for a in acts:
            if a != "WIRE-P":
                R.append(dict(metric=m, act=a, **paired(sub, "WIRE-P", a, m, ["seed"])))
    R = pd.DataFrame(R)
    R["p_w_holm"] = holm_by(R, ("metric",))
    for _, r in R.iterrows():
        say(f"  WIRE-P vs {r.act:13s} {r.metric}: ratio={r.ratio:.3f} wins={r.wins}/{r.n} p_W={r.p_w:.4f} "
            f"p_W,Holm={r.p_w_holm:.4f}")
    R.to_csv(os.path.join(TAB, "tab_real_tests.csv"), index=False)

    # figure: data, training window, forecasts (median & range over seeds) for selected activations
    ds = REAL_DATASETS[name]
    fig, ax = plt.subplots(figsize=(6.5, 4))
    cols = {"WIRE-P": "#1a6eb5", "WIRE-P-A": "#2ca02c", "MV-Morlet": "#e07b00", "Tanh": "#7f7f7f"}
    styles = {"WIRE-P": "-", "WIRE-P-A": "--", "MV-Morlet": "-.", "Tanh": ":"}
    for a, c in cols.items():
        files = sorted(glob.glob(os.path.join(ROOT, "E5_real", f"E5_real_{name}_{a.replace('(', '').replace(')', '').replace('=', '')}_s*.npz")))
        if not files:
            continue
        P = np.array([np.load(f)["pred"][:, 2] for f in files])
        tt = np.load(files[0])["t"]
        ax.plot(tt, np.median(P, 0), color=c, lw=1.8, ls=styles[a], label=f"{a} (median, n={len(files)})")
        ax.fill_between(tt, P.min(0), P.max(0), color=c, alpha=0.15)
    t = np.asarray(ds["t"])
    y = np.asarray(ds["I"])
    tr = t <= ds["train_days"]
    ax.scatter(t[tr], y[tr], color="k", zorder=5, s=18, label="Observed (training)")
    ax.scatter(t[~tr], y[~tr], facecolor="white", edgecolor="k", zorder=5, s=22, label="Observed (held out)")
    ax.axvline(ds["train_days"] + 0.5, color="red", ls="--", lw=1)
    ax.set_xlabel("Day")
    ax.set_ylabel("Pupils confined to bed, $I(t)$")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_real_boarding_school.png"))
    plt.close(fig)


def compact_main(df, R):
    """Main-text table: mean relative L2 (x1e-3, mean ± sd) per activation and disease, with the
    WIRE-P/other geometric-mean ratio, WIRE-P wins and Holm-adjusted Wilcoxon p."""
    sub = df[df.exp == "E1_main"]
    if sub.empty or R is None or R.empty:
        return
    acts = [a for a in ALL_ACTS if a in set(sub.act)]
    tex = ["\\begin{tabular}{l" + "cc" * len(DISEASES) + "}", "\\toprule",
           " & " + " & ".join(f"\\multicolumn{{2}}{{c}}{{{d}}}" for d in DISEASES) + " \\\\",
           "".join(f"\\cmidrule(lr){{{2 + 2 * i}-{3 + 2 * i}}}" for i in range(len(DISEASES))),
           "Activation" + " & Rel.\\ $L_2$ ($10^{-3}$) & Ratio (wins) $p_\\text{Holm}$" * len(DISEASES) + " \\\\",
           "\\midrule"]
    best = {d: min(acts, key=lambda a: sub[(sub.disease == d) & (sub.act == a)].mean_rel.mean()) for d in DISEASES}
    for a in acts:
        cells = []
        for d in DISEASES:
            v = sub[(sub.disease == d) & (sub.act == a)].mean_rel.values * 1e3
            c = f"{v.mean():.2f} $\\pm$ {v.std(ddof=1):.2f}"
            cells.append(f"\\textbf{{{c}}}" if a == best[d] else c)
            r = R[(R.disease == d) & (R.metric == "mean_rel") & (R.act == a)]
            cells.append("--" if r.empty else f"{r.iloc[0].ratio:.2f} ({r.iloc[0].wins}/{r.iloc[0].n}) {fmt_p(r.iloc[0].p_w_holm)}")
        tex.append(a.replace("phi", "$\\phi$") + " & " + " & ".join(cells) + " \\\\")
    tex += ["\\bottomrule", "\\end{tabular}"]
    write("tab_main_compact.tex", "\n".join(tex))


INV_FAIL_BETA = 50.0


def e4_inverse(df):
    sub = df[df.exp == "E4_inverse"]
    if sub.empty:
        return
    acts = [a for a in CORE + ["Sigmoid"] if a in set(sub.act)]
    say("\n## E4 inverse problem: I(t) observed every 2 days with noise; beta, gamma learned (init 0.2, 0.1)")
    say(f"  failure = beta error > {INV_FAIL_BETA:.0f}% (rates collapse towards the trivial solution beta, gamma -> 0)")
    # medians (means are dominated by collapsed runs with gamma ~ 0) and number of failed seeds
    tex = ["\\begin{tabular}{ll" + "c" * len(acts) + "}", "\\toprule",
           "Disease & Noise & " + " & ".join(acts) + " \\\\", "\\midrule"]
    for d in DISEASES:
        for nz in sorted(sub.noise.unique()):
            dd = sub[(sub.disease == d) & (sub.noise == nz)]
            cells, meds = [], {}
            for a in acts:
                v = dd[dd.act == a]
                if v.empty:
                    cells.append("--")
                    continue
                fail = int((v.beta_err > INV_FAIL_BETA).sum())
                meds[a] = v.R0_err.median()
                cells.append(f"{v.R0_err.median():.1f} / {v.beta_err.median():.1f} [{fail}]")
                say(f"  {d:11s} noise={nz:.2f} {a:10s} median R0_err={v.R0_err.median():9.2f}% beta_err={v.beta_err.median():7.2f}% "
                    f"relL2={v.mean_rel.median():.3e} failed={fail}/{len(v)}")
            best = min(meds, key=meds.get)
            cells = [f"\\textbf{{{c}}}" if a == best else c for a, c in zip(acts, cells)]
            tex.append(f"{d} & {int(round(nz * 100))}\\% & " + " & ".join(cells) + " \\\\")
        tex.append("\\midrule")
    tex[-1] = "\\bottomrule"
    tex.append("\\end{tabular}")
    write("tab_inverse.tex", "\n".join(tex))
    recs = []
    for d in DISEASES:
        for nz in sorted(sub.noise.unique()):
            dd = sub[(sub.disease == d) & (sub.noise == nz)]
            for m in ("mean_rel", "R0_err"):
                for a in acts:
                    if a != "WIRE-P":
                        recs.append(dict(disease=d, noise=nz, metric=m, act=a, **paired(dd, "WIRE-P", a, m, ["seed"])))
    R = pd.DataFrame(recs)
    R["p_w_holm"] = holm_by(R, ("disease", "noise", "metric"))
    R.to_csv(os.path.join(TAB, "tab_inverse_tests.csv"), index=False)
    for _, r in R.iterrows():
        say(f"  {r.disease:11s} noise={r.noise:.2f} {r.metric:8s} WIRE-P vs {r.act:10s} ratio={r.ratio:.3f} "
            f"wins={r.wins}/{r.n} p_W={r.p_w:.4f} p_W,Holm={r.p_w_holm:.4f}")


def noise_arch(df, exp, title):
    sub = df[df.exp == exp]
    if sub.empty:
        return
    acts = [a for a in CORE if a in set(sub.act)]
    say(f"\n## {title}")
    tex = ["\\begin{tabular}{ll" + "c" * len(acts) + "}", "\\toprule",
           "Disease & Setting & " + " & ".join(acts) + " \\\\", "\\midrule"]
    recs = []
    for d in DISEASES:
        for nz in sorted(sub.noise.unique()):
            dd = sub[(sub.disease == d) & (sub.noise == nz)]
            vals = {a: dd[dd.act == a]["mean_rel"].values for a in acts}
            means = {a: np.mean(v) if len(v) else np.inf for a, v in vals.items()}
            best = min(means, key=means.get)
            cells = [(f"\\textbf{{{ms(v)}}}" if a == best else ms(v)) if len(v) else "--" for a, v in vals.items()]
            setting = f"{int(round(nz * 100))}\\% noise" if exp == "E2_noise" else "$3\\times32$"
            tex.append(f"{d} & {setting} & " + " & ".join(cells) + " \\\\")
            say(f"  {d:11s} noise={nz:.2f} " + " | ".join(f"{a}={np.mean(v):.3e}±{np.std(v, ddof=1) if len(v) > 1 else 0:.1e}(n={len(v)})"
                                                         for a, v in vals.items() if len(v)))
            for a in acts:
                if a != "WIRE-P":
                    recs.append(dict(disease=d, noise=nz, act=a, **paired(dd, "WIRE-P", a, "mean_rel", ["seed"])))
    tex += ["\\bottomrule", "\\end{tabular}"]
    write(f"tab_{exp}.tex", "\n".join(tex))
    R = pd.DataFrame(recs)
    if R.empty:
        return
    R["p_w_holm"] = holm_by(R, ("disease", "noise"))
    R.to_csv(os.path.join(TAB, f"tab_{exp}_tests.csv"), index=False)
    for _, r in R.iterrows():
        say(f"  {r.disease:11s} noise={r.noise:.2f} WIRE-P vs {r.act:10s} ratio={r.ratio:.3f} wins={r.wins}/{r.n} "
            f"p_W={r.p_w:.4f} p_W,Holm={r.p_w_holm:.4f}")


def tests_table(R, name, ref, acts, metrics=("mean_rel", "peak_err", "phys_res")):
    """LaTeX table: geometric-mean ratio ref/other, wins, Holm-adjusted Wilcoxon p."""
    if R is None or R.empty:
        return
    lab = {"mean_rel": "Rel.\\ $L_2$", "peak_err": "Peak err.", "phys_res": "Phys.\\ res."}
    acts = [a for a in acts if a in set(R.act)]
    tex = ["\\begin{tabular}{ll" + "c" * len(acts) + "}", "\\toprule",
           "Disease & Metric & " + " & ".join(acts) + " \\\\", "\\midrule"]
    for d in DISEASES:
        for m in metrics:
            cells = []
            for a in acts:
                r = R[(R.disease == d) & (R.metric == m) & (R.act == a)]
                if r.empty:
                    cells.append("--")
                    continue
                r = r.iloc[0]
                cells.append(f"{r.ratio:.2f} ({r.wins}/{r.n}) {fmt_p(r.p_w_holm)}")
            tex.append(f"{d} & {lab[m]} & " + " & ".join(cells) + " \\\\")
        tex.append("\\midrule")
    tex[-1] = "\\bottomrule"
    tex.append("\\end{tabular}")
    write(name + ".tex", "\n".join(tex))


def figures_main(df):
    sub = df[df.exp == "E1_main"]
    if sub.empty:
        return
    acts = [a for a in ALL_ACTS if a in set(sub.act)]
    fig, axes = plt.subplots(3, 3, figsize=(13, 10), sharex=True)
    for i, d in enumerate(DISEASES):
        for k, (m, lab) in enumerate((("mean_rel", "Mean rel. $L_2$"), ("peak_err", "Peak error (%)"),
                                      ("phys_res", "Physics residual"))):
            ax = axes[i, k]
            data = [sub[(sub.disease == d) & (sub.act == a)][m].values for a in acts]
            ax.boxplot(data, showfliers=False, widths=0.6)
            for x, v in enumerate(data):
                ax.scatter(np.full(len(v), x + 1) + np.random.uniform(-0.15, 0.15, len(v)), v, s=8,
                           color="#1a6eb5" if acts[x].startswith("WIRE") else "#555555", zorder=3)
            ax.set_yscale("log")
            ax.set_title(f"{d}: {lab}", fontsize=9)
            ax.set_xticks(range(1, len(acts) + 1))
            ax.set_xticklabels(acts, rotation=60, fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_main_boxplots.png"))
    plt.close(fig)



def fig_inverse(df):
    """Relative beta error of every inverse run (per seed), by activation and noise level."""
    sub = df[df.exp == "E4_inverse"]
    if sub.empty:
        return
    acts = [a for a in CORE + ["Sigmoid"] if a in set(sub.act)]
    noises = sorted(sub.noise.unique())
    cols = ["#1a6eb5", "#e07b00", "#b2182b"]
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8), sharey=True)
    for i, d in enumerate(DISEASES):
        ax = axes[i]
        for k, nz in enumerate(noises):
            for x, a in enumerate(acts):
                v = sub[(sub.disease == d) & (sub.act == a) & (sub.noise == nz)].beta_err.values
                v = np.clip(v, 1e-2, 100.0)
                xx = x + (k - 1) * 0.25 + np.random.uniform(-0.06, 0.06, len(v))
                ax.scatter(xx, v, s=12, color=cols[k], alpha=0.8,
                           label=f"{int(round(nz * 100))}% noise" if (i == 0 and x == 0) else None)
        ax.axhline(INV_FAIL_BETA, color="k", ls="--", lw=0.8)
        ax.set_yscale("log")
        ax.set_xticks(range(len(acts)))
        ax.set_xticklabels(acts, fontsize=8)
        ax.set_title(d)
        ax.grid(alpha=0.3)
    axes[0].set_ylabel(r"Relative error of $\hat\beta$ (%)")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.legend(loc="lower center", ncol=3, fontsize=8, frameon=False)
    fig.savefig(os.path.join(FIG, "fig_inverse_beta.png"))
    plt.close(fig)


def fig_activation():
    """Activation shapes and their integrals (admissibility)."""
    import torch
    z = np.linspace(-8, 8, 2001)
    w, a, p = 1.25, 4.0, 4.0
    phi = np.arctan(a * w)
    env = (1 + a * z * z) ** (-p)
    kappa = core.rational_cos_ratio(torch.tensor([w]), torch.tensor([a]), torch.tensor([p])).item()
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.4))
    axes[0].plot(z, np.cos(w * z) * np.exp(-z * z / 2), color="#e07b00", label="MV-Morlet")
    axes[0].plot(z, (np.cos(w * z) - np.exp(-w * w / 2)) * np.exp(-z * z / 2), color="#e07b00", ls=":",
                 label="MV-Morlet-A (zero mean)")
    axes[0].plot(z, np.cos(w * z + phi) * env, color="#1a6eb5", label="WIRE-P")
    axes[0].plot(z, (np.cos(w * z + phi) - np.cos(phi) * kappa) * env, color="#2ca02c", ls="--",
                 label="WIRE-P-A (zero mean)")
    axes[0].set_xlim(-4, 4)
    axes[0].set_title(f"(a) shapes, $\\omega$={w}, $\\alpha$={a}, $p$={p}")
    axes[0].legend(fontsize=7)
    ws = np.linspace(0.5, 2.0, 61)
    from scipy.integrate import quad
    for aa, pp, ls in ((4.0, 4.0, "-"), (1.0, 2.0, "--"), (0.25, 1.5, ":")):
        vals = []
        for ww in ws:
            ph = np.arctan(aa * ww)
            k = core.rational_cos_ratio(torch.tensor([ww]), torch.tensor([aa]), torch.tensor([pp])).item()
            E = np.sqrt(np.pi / aa) * np.exp(__import__("math").lgamma(pp - 0.5) - __import__("math").lgamma(pp))
            vals.append(np.cos(ph) * k * E)
        axes[1].plot(ws, vals, color="#1a6eb5", ls=ls, label=f"WIRE-P, $\\alpha$={aa}, $p$={pp}")
    axes[1].plot(ws, np.sqrt(2 * np.pi) * np.exp(-ws ** 2 / 2), color="#e07b00", label="MV-Morlet")
    axes[1].axhline(0, color="#2ca02c", ls="--", label="WIRE-P-A / MV-Morlet-A")
    axes[1].set_xlabel("$\\omega$")
    axes[1].set_title("(b) $\\int\\psi(z)\\,dz$ (zero = admissible)")
    axes[1].legend(fontsize=7)
    axes[2].semilogy(z[z > 0], env[z > 0], color="#1a6eb5", label="rational $(1+\\alpha z^2)^{-p}$")
    axes[2].semilogy(z[z > 0], np.exp(-z[z > 0] ** 2 / 2), color="#e07b00", label="Gaussian $e^{-z^2/2}$")
    axes[2].set_ylim(1e-12, 2)
    axes[2].set_title("(c) envelope tails")
    axes[2].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_activation_admissibility.png"))
    plt.close(fig)


def progress(df):
    from wirep.experiments import all_jobs
    from collections import Counter
    tot = Counter(j["exp"] for j in all_jobs())
    done = Counter(df.exp) if not df.empty else Counter()
    say("# Progress: " + ", ".join(f"{e} {done.get(e, 0)}/{n}" for e, n in sorted(tot.items())))
    if not df.empty:
        say("# mean train time (s) by activation: " + ", ".join(
            f"{a}={t:.0f}" for a, t in df[df.exp == "E1_main"].groupby("act").time.mean().items()))


if __name__ == "__main__":
    df = load()
    progress(df)
    if not df.empty:
        df.to_csv(os.path.join(ROOT, "all_results.csv"), index=False)
        e0_legacy(df)
        summary_table(df, "E1_main", ALL_ACTS, "tab_main")
        summary_table(df, "E1_main", ALL_ACTS, "tab_cost", metrics=("time", "lbfgs"))
        ranking(df, "E1_main")
        R1 = main_table(df, "E1_main", ALL_ACTS, "tab_main", ref="WIRE-P")
        tests_table(R1, "tab_main_tests", "WIRE-P", [a for a in ALL_ACTS if a != "WIRE-P"])
        compact_main(df, R1)
        RA = main_table(df, "E1_main", ["WIRE-P-A"] + [a for a in ALL_ACTS if a != "WIRE-P-A"], "tab_main_A",
                        ref="WIRE-P-A")
        tests_table(RA, "tab_mainA_tests", "WIRE-P-A", [a for a in ALL_ACTS if a != "WIRE-P-A"])
        RM = main_table(df, "E1_main", ["MV-Morlet", "MV-Morlet-A"], "tab_morletA", ref="MV-Morlet")
        e5_real(df)
        e4_inverse(df)
        noise_arch(df, "E2_noise", "E2 noisy anchors (forward problem)")
        noise_arch(df, "E3_arch", "E3 smaller network 3x32")
        figures_main(df)
        fig_inverse(df)
    fig_activation()
    open(os.path.join(ROOT, "REPORT.md"), "w", encoding="utf-8").write("\n".join(REPORT))
