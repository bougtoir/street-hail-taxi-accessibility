#!/usr/bin/env python3
"""Revision Phase 3-4/10: component-ablation of the opportunity construct.

Specs:
  ROAD   : road/network structure only (w_road, degree, lanes) - no attractors
  ATTR   : urban attractor/context only (station, nightlife, hotel/hosp, transit, taxi stands)
  PROXY  : existing modeled circulation-potential prior (A_A, renamed)
  COMB   : combined model (A_C)
Reuses cached reach.json and the same 2,000 origins (seed 42).
"""
import os, json, math, numpy as np, pandas as pd
from scipy.stats import spearmanr, wilcoxon

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC, TAB = f"{ROOT}/data/processed", f"{ROOT}/tables"
rng = np.random.default_rng(42)

seg = pd.read_parquet(f"{PROC}/segments.parquet")
z = lambda s: (s - s.mean()) / (s.std() + 1e-12)

# ---- build spec scores (segment-level; period-invariant for ROAD/ATTR) ----
seg["S_ROAD"] = z(z(seg.w_road) + 0.5 * z(np.log1p(seg.deg)) + 0.3 * z(np.log1p(seg.lanes_n)))
seg["S_ATTR"] = z(z(np.log1p(seg.k_station)) + 0.6 * z(np.log1p(seg.k_pois_nightlife))
                  + 0.5 * z(np.log1p(seg.k_pois_hotel_hosp))
                  + 0.4 * z(np.log1p(seg.k_pois_transit))
                  + 0.8 * seg.stand100)
# temporal attr variant: nightlife share modulation like combined? Keep ATTR static
# (context is spatial); period effect enters via PROXY/COMB only.
SPECS = ["ROAD", "ATTR", "PROXY", "COMB"]
PERIODS = [f"{wd}_{h:02d}" for wd in ["weekday", "weekend"] for h in [8, 13, 17, 21, 23]]

def spec_col(spec, per):
    if spec == "ROAD": return "S_ROAD"
    if spec == "ATTR": return "S_ATTR"
    if spec == "PROXY": return f"A_A_{per}"
    return f"A_C_{per}"

# ---- segment-level rank agreement vs COMB ----
agree_rows = []
for per in PERIODS:
    comb = seg[f"A_C_{per}"]
    for spec, col in [("ROAD", "S_ROAD"), ("ATTR", "S_ATTR"), ("PROXY", f"A_A_{per}")]:
        m = comb.notna() & seg[col].notna()
        rho = spearmanr(seg.loc[m, col], comb[m]).statistic
        k = int(m.sum() * 0.01)
        top_a = set(seg.loc[m].nlargest(k, col).index)
        top_c = set(seg.loc[m].nlargest(k, f"A_C_{per}").index)
        agree_rows.append({"period": per, "spec": spec, "spearman": rho,
                           "jaccard_top1pct": len(top_a & top_c) / len(top_a | top_c)})
agr = pd.DataFrame(agree_rows)
agr.to_csv(f"{TAB}/ablation_rank_agreement.csv", index=False)
print(agr.groupby("spec").agg({"spearman": "mean", "jaccard_top1pct": "mean"}).round(3))

# ---- relocation evaluation per spec ----
cand = seg[seg.hail_ok].reset_index(drop=True)
orig_idx = rng.choice(len(cand), 2000, replace=False)
origins = cand.iloc[orig_idx].reset_index(drop=True)
reach = [{int(k): v for k, v in r.items()} for r in json.load(open(f"{PROC}/reach.json"))]
RADII = [100, 200, 300, 500]
rand = np.random.default_rng(43)

rows = []
for i, orow in origins.iterrows():
    e = reach[i]
    for r in RADII:
        items = [(k, v) for k, v in e.items() if v <= r]
        if not items:
            continue
        ei = np.array([k for k, _ in items]); di = np.array([v for _, v in items])
        c = cand.iloc[ei]
        maj = c.w_road.to_numpy() >= 0.99
        for per in PERIODS:
            for spec in SPECS:
                col = spec_col(spec, per)
                a0 = orow[col] if spec in ("ROAD", "ATTR") else orow[col]
                v = c[col].to_numpy(); ok = np.isfinite(v)
                if not ok.any() or not np.isfinite(a0):
                    continue
                v2, di2 = v[ok], di[ok]
                b = int(np.argmax(v2))
                rv = rand.choice(v2, size=min(10, len(v2)), replace=False).mean()
                nm = v2[maj[ok]][np.argmin(di2[maj[ok]])] if maj[ok].any() else np.nan
                rows.append({"origin": i, "radius": r, "period": per, "spec": spec,
                             "G": v2[b] - a0, "walk_m": di2[b],
                             "gain_rand": rv - a0,
                             "gain_nearmaj": (nm - a0) if np.isfinite(nm) else np.nan,
                             "eid": int(ei[ok][b]),
                             "best_is_major": bool(maj[ok][b])})
    if i % 400 == 0:
        print("  ", i, len(rows))

ab = pd.DataFrame(rows)
ab.to_parquet(f"{PROC}/ablation_results.parquet")

# ---- summary ----
def boot_ci(x, n=2000):
    x = np.asarray(x)[np.isfinite(x)]
    if len(x) == 0: return [np.nan, np.nan]
    bs = [np.mean(rng.choice(x, len(x), replace=True)) for _ in range(n)]
    return np.percentile(bs, [2.5, 97.5]).round(4).tolist()

summ = []
for (spec, r), s in ab.groupby(["spec", "radius"]):
    dnm = (s.G - s.gain_nearmaj).dropna()
    w = wilcoxon(dnm) if len(dnm) > 10 and (dnm != 0).any() else None
    summ.append({"spec": spec, "radius": r, "n": len(s),
                 "frac_pos": (s.G > 0).mean(), "frac_gt_01": (s.G > 0.1).mean(),
                 "mean_G": s.G.mean(), "med_G": s.G.median(), "ci_G": boot_ci(s.G),
                 "gt_rand": (s.G > s.gain_rand).mean(),
                 "gt_nearmaj": (dnm > 1e-9).mean(), "diff_nearmaj": dnm.mean(),
                 "diff_nearmaj_ci": boot_ci(dnm),
                 "wilcoxon_p": (w.pvalue if w else np.nan),
                 "best_is_major": s.best_is_major.mean()})
ss = pd.DataFrame(summ)
ss.to_csv(f"{TAB}/ablation_summary.csv", index=False)
print(ss[ss.radius == 300].round(3).to_string())
print("done")
