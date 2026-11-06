#!/usr/bin/env python3
"""Phases 8, 11, 16: utility analysis, sensitivity, statistical reporting."""
import os, json, math, numpy as np, pandas as pd
from scipy.stats import spearmanr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC, TAB = f"{ROOT}/data/processed", f"{ROOT}/tables"
os.makedirs(TAB, exist_ok=True)
rng = np.random.default_rng(42)

df = pd.read_parquet(f"{PROC}/relocation_results.parquet")
seg = pd.read_parquet(f"{PROC}/segments.parquet")
out = {}

# --- 1. headline summaries -------------------------------------------------
def boot_ci(x, fn=np.mean, n=2000):
    x = np.asarray(x)[np.isfinite(x)]
    bs = [fn(rng.choice(x, len(x), replace=True)) for _ in range(n)]
    return np.percentile(bs, [2.5, 97.5]).round(4).tolist()

rows = []
for (model, radius), s in df.groupby(["model", "radius"]):
    diff_nm = (s.G_A - s.gain_nearmajor).dropna()
    rows.append({
        "model": model, "radius": radius, "n": len(s),
        "frac_any_gain": (s.G_A > 0).mean(),
        "frac_gain_gt_0.1sd": (s.G_A > 0.1).mean(),
        "mean_G_A": s.G_A.mean(), "median_G_A": s.G_A.median(),
        "mean_G_A_ci": boot_ci(s.G_A),
        "median_RAG": s.RAG.median(),
        "median_walk_m": s.walk_m.median(),
        "opt_gt_random": (s.G_A > s.gain_random).mean(),
        "opt_gt_nearmajor": (diff_nm > 1e-9).mean(),
        "mean_diff_nearmajor": diff_nm.mean(),
        "diff_nearmajor_ci": boot_ci(diff_nm),
        "opt_gt_bestmajor": ((s.G_A - s.gain_major).dropna() > 1e-9).mean(),
        "best_is_major": s.best_is_major.mean(),
    })
t1 = pd.DataFrame(rows)
t1.to_csv(f"{TAB}/strategy_comparison.csv", index=False)

# --- 2. distance-to-meaningful-improvement ---------------------------------
t2 = df.groupby(["model", "radius"])[[c for c in df if c.startswith("dist_p")]].median()
t2.to_csv(f"{TAB}/distance_to_threshold.csv")

# --- 3. temporal & spatial heterogeneity -----------------------------------
t3 = df[df.model == "A_C"].groupby(["radius", "period"]).G_A.agg(["mean", "median"])
t3.to_csv(f"{TAB}/temporal_heterogeneity.csv")
t4 = df[df.model == "A_C"].groupby(["radius", "ward"]).G_A.agg(["mean", "median"])
t4.to_csv(f"{TAB}/ward_heterogeneity.csv")

# --- 4. segment-level model agreement (Spearman) ----------------------------
rho = {}
per = "weekday_17"
cols = [f"A_{m}_{per}" for m in "ABC"]
sseg = seg[cols].dropna()
for i in range(3):
    for j in range(i + 1, 3):
        rho[f"{cols[i]}~{cols[j]}"] = spearmanr(sseg[cols[i]], sseg[cols[j]]).statistic
# top-1% segment Jaccard between models
k = int(len(sseg) * 0.01)
tops = {c: set(sseg.nlargest(k, c).index) for c in cols}
jac = {f"{a}~{b}": len(tops[a] & tops[b]) / len(tops[a] | tops[b])
       for a in cols for b in cols if a < b}
json.dump({"spearman": rho, "jaccard_top1pct": jac}, open(f"{TAB}/model_agreement.json", "w"), indent=1)

# --- 5. optimum agreement across models (same chosen segment rate) ----------
grp = df[(df.radius == 300)].pivot_table(index=["origin", "period"], columns="model",
                                         values=["Astar", "walk_m"], aggfunc="first")
same_ac = np.nan
try:
    astar = df[df.radius == 300].pivot_table(index=["origin", "period"], columns="model", values="walk_m")
    # proxy for 'same place': compare walk_m & Astar is hard; use gain correlation instead
    gains = df[df.radius == 300].pivot_table(index=["origin", "period"], columns="model", values="G_A")
    same_ac = gains.corr(method="spearman")
except Exception as e:
    print(e)
if isinstance(same_ac, pd.DataFrame):
    same_ac.to_csv(f"{TAB}/gain_corr_across_models.csv")

# --- 6. utility / gain-per-meter & walking penalty --------------------------
d = df[(df.model == "A_C") & (df.radius >= 200)].copy()
d["gpm"] = d.G_A / (d.walk_m / 100)  # gain per 100 m walked
t6 = d.groupby("radius").agg(gpm_med=("gpm", "median"),
                             gpm_p25=("gpm", lambda s: s.quantile(.25)),
                             gpm_p75=("gpm", lambda s: s.quantile(.75)))
t6.to_csv(f"{TAB}/gain_per_meter.csv")

# lambda sweep on stored results: utility-maximizing choice isn't stored per
# candidate, approximate with optimizer result: report walk_m and G_A trade-off
# quantiles + fraction where dstar <= radius*0.5
t7 = d.groupby("radius").apply(lambda s: pd.Series({
    "frac_opt_within_half_radius": (s.walk_m <= s.radius * 0.5).mean(),
    "gain_per_min80mpm_med": (s.G_A / (s.walk_m / 80)).median(),
}))
t7.to_csv(f"{TAB}/utility_summary.csv")

# --- 7. rank stability across specifications (transition of gain class) -----
g = df.pivot_table(index=["origin", "radius", "period"], columns="model", values="G_A")
def cls(x):
    return pd.cut(x, [-1e9, 0, 0.5, 1.5, 1e9], labels=["none", "low", "mid", "high"])
ct = pd.crosstab(cls(g.A_A), cls(g.A_C), normalize="index")
ct.to_csv(f"{TAB}/gainclass_transition_AtoC.csv")

print(t1.round(3).to_string())
print("agreement:", json.dumps({"spearman": rho, "jaccard": jac}, indent=1))
print("done")
