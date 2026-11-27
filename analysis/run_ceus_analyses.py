#!/usr/bin/env python3
"""CEUS final pass: cluster-aware inference, cross-specification transfer,
spatial permutation null (unconstrained + within-ward constrained).

Reuses reach.json, ablation_results.parquet, segments.parquet, edge_ward.parquet.
No upstream preprocessing rerun. Seeds fixed.
"""
import os, json, numpy as np, pandas as pd
from scipy.stats import wilcoxon

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC, TAB = f"{ROOT}/data/processed", f"{ROOT}/tables"
rng = np.random.default_rng(42)
B = 5000          # bootstrap replicates (origin-level)
NPERM = 500       # spatial permutations

seg = pd.read_parquet(f"{PROC}/segments.parquet")
ab = pd.read_parquet(f"{PROC}/ablation_results.parquet")
cand = seg[seg.hail_ok].reset_index(drop=True)
PERIODS = [f"{wd}_{h:02d}" for wd in ["weekday", "weekend"] for h in [8, 13, 17, 21, 23]]
STATIC = {"ROAD": "S_ROAD", "ATTR": "S_ATTR"}
VARY = {"PROXY": "A_A_", "COMB": "A_C_"}
seg["S_ROAD"] = ((seg.w_road - seg.w_road.mean()) / (seg.w_road.std() + 1e-12)
                 + 0.5 * ((np.log1p(seg.deg) - np.log1p(seg.deg).mean()) / (np.log1p(seg.deg).std() + 1e-12))
                 + 0.3 * ((np.log1p(seg.lanes_n) - np.log1p(seg.lanes_n).mean()) / (np.log1p(seg.lanes_n).std() + 1e-12)))
seg["S_ROAD"] = (seg.S_ROAD - seg.S_ROAD.mean()) / (seg.S_ROAD.std() + 1e-12)
for c, w in [("k_station", 1.0), ("k_pois_nightlife", 0.6), ("k_pois_hotel_hosp", 0.5), ("k_pois_transit", 0.4)]:
    seg[f"_z{c}"] = (np.log1p(seg[c]) - np.log1p(seg[c]).mean()) / (np.log1p(seg[c]).std() + 1e-12)
seg["S_ATTR"] = seg._zk_station + 0.6 * seg._zk_pois_nightlife + 0.5 * seg._zk_pois_hotel_hosp \
    + 0.4 * seg._zk_pois_transit + 0.8 * seg.stand100
seg["S_ATTR"] = (seg.S_ATTR - seg.S_ATTR.mean()) / (seg.S_ATTR.std() + 1e-12)
cand = seg[seg.hail_ok].reset_index(drop=True)

def score_vec(spec, per):
    if spec in STATIC: return cand[STATIC[spec]].to_numpy()
    return cand[f"{VARY[spec]}{per}"].to_numpy()

orig_scores = {}
for spec in STATIC: orig_scores[spec] = cand[STATIC[spec]].to_numpy()

# ---- cluster-aware ablation summary ----
def _sums_counts(vals_by_origin):
    s = np.array([v.sum() for v in vals_by_origin])
    c = np.array([len(v) for v in vals_by_origin], dtype=float)
    return s, c

def cluster_boot(vals_by_origin, B=B, rng=rng):
    """Origin-clustered bootstrap of the row-level mean (resample origins)."""
    s, c = _sums_counts(vals_by_origin)
    n = len(s)
    idx = rng.integers(0, n, (B, n))
    stats = s[idx].sum(1) / c[idx].sum(1)
    return np.percentile(stats, [2.5, 97.5]), stats.mean()

cluster_boot_frac = cluster_boot

summ = []
for (spec, r), s in ab.groupby(["spec", "radius"]):
    if spec in STATIC:
        su = s.drop_duplicates(subset=["origin"])  # period-invariant
        by_o = su.groupby("origin")
        G = [g.G.to_numpy() for _, g in by_o]
        dnm_all = (su.G - su.gain_nearmaj)
        dnm = [g.dropna().to_numpy() for _, g in dnm_all.groupby(su.origin)]
        n_eff = su.origin.nunique(); n_rows = len(s)
        wilc = wilcoxon(su.set_index("origin").G.sub(
            su.set_index("origin").gain_nearmaj).dropna())
    else:
        by_o = s.groupby("origin")
        G = [g.G.to_numpy() for _, g in by_o]
        d = (s.G - s.gain_nearmaj)
        dnm = [g.dropna().to_numpy() for _, g in d.groupby(s.origin)]
        n_eff = s.origin.nunique(); n_rows = len(s)
        # origin-mean paired difference -> Wilcoxon on origins
        dm = d.groupby(s.origin).mean().dropna()
        wilc = wilcoxon(dm) if (dm != 0).any() else None
    frac_mask = [(g.G > 0).to_numpy() for _, g in by_o]
    ci_G, _ = cluster_boot(G)
    summ.append({"spec": spec, "radius": r, "n_origins": n_eff, "n_rows": n_rows,
                 "frac_pos": (s.G > 0).mean(), "frac_pos_ci": cluster_boot_frac(frac_mask)[0].tolist(),
                 "frac_gt_01": (s.G > 0.1).mean(),
                 "mean_G": s.G.mean(), "ci_G": ci_G.tolist(),
                 "gt_rand": (s.G > s.gain_rand).mean(),
                 "gt_nearmaj": ((s.G - s.gain_nearmaj).dropna() > 1e-9).mean(),
                 "diff_nearmaj": (s.G - s.gain_nearmaj).mean(),
                 "diff_nearmaj_ci": cluster_boot(dnm)[0].tolist(),
                 "wilcoxon_p": wilc.pvalue if wilc is not None else np.nan,
                 "best_is_major": s.best_is_major.mean()})
ss = pd.DataFrame(summ)
ss.to_csv(f"{TAB}/ablation_summary_clustered.csv", index=False)
print(ss[ss.radius == 300].round(3).to_string())

# ---- cross-specification transfer ----
reach = [{int(k): v for k, v in r.items()} for r in json.load(open(f"{PROC}/reach.json"))]
orig_idx_map = ab[["origin", "radius", "period", "spec", "eid"]].copy()
orig_cand_idx = {}
rng42 = np.random.default_rng(42)
orig_idx = rng42.choice(len(cand), 2000, replace=False)
origin_row = {i: int(orig_idx[i]) for i in range(2000)}  # cand row of origin segment

TRANSFERS = [("ROAD", "ATTR"), ("ATTR", "ROAD"), ("ROAD", "PROXY"), ("ATTR", "PROXY"),
             ("PROXY", "ROAD"), ("PROXY", "ATTR"), ("ROAD", "COMB"), ("ATTR", "COMB"),
             ("PROXY", "COMB")]
# period handling: selector period p -> evaluate under B at same p (static specs identical)
sel = ab.set_index(["origin", "radius", "period", "spec"])
rows = []
for (i, r, per), grp in ab.groupby(["origin", "radius", "period"]):
    oid = origin_row[i]
    for A, Bs in TRANSFERS:
        try:
            eA = int(sel.loc[(i, r, per, A)].eid)
        except KeyError:
            continue
        colB = STATIC.get(Bs, None)
        sb = (cand[colB].iat[eA] - cand[colB].iat[oid]) if colB else \
             (cand[f"{VARY[Bs]}{per}"].iat[eA] - cand[f"{VARY[Bs]}{per}"].iat[oid])
        rows.append({"origin": i, "radius": r, "period": per,
                     "selector": A, "evaluator": Bs, "TG": sb})
tr = pd.DataFrame(rows)
tr.to_parquet(f"{PROC}/transfer_results.parquet")

tsum = []
for (A, Bs, r), s in tr.groupby(["selector", "evaluator", "radius"]):
    # cluster by origin (dedupe periods for static evaluators)
    if Bs in STATIC:
        su = s.drop_duplicates(subset=["origin"])
        vals = [np.array([v]) for v in su.TG]
    else:
        vals = [g.TG.to_numpy() for _, g in s.groupby("origin")]
    ci, _ = cluster_boot(vals)
    su_ = s.drop_duplicates(subset=["origin"]) if Bs in STATIC else s.groupby("origin").TG.mean()
    tg = su_.TG if Bs in STATIC else su_
    tsum.append({"selector": A, "evaluator": Bs, "radius": r,
                 "mean_TG": s.TG.mean(), "med_TG": s.TG.median(), "ci_TG": ci.tolist(),
                 "frac_pos": (s.TG > 0).mean(), "frac_gt_01": (s.TG > 0.1).mean()})
ts = pd.DataFrame(tsum)
ts.to_csv(f"{TAB}/transfer_summary.csv", index=False)
print(ts[ts.radius == 300].round(3).to_string())

# ---- spatial permutation null (COMB spec) ----
ward = pd.read_parquet(f"{PROC}/edge_ward.parquet")
cand_key = cand[["u", "v", "key"]].reset_index().merge(ward, on=["u", "v", "key"], how="left")
cand_ward = cand_key.ward.to_numpy()

origins_eid = orig_idx  # cand indices of origins
reach_arr = {}
for i in range(2000):
    for r in [100, 200, 300, 500]:
        ei = np.array([k for k, v in reach[i].items() if v <= r], dtype=int)
        reach_arr[(i, r)] = ei

def perm_stats(scores, order=None):
    """scores: permuted score vector over cand; returns dict of stats at 300m etc."""
    out = {}
    for r in [100, 200, 300, 500]:
        pos, tot, gsum = 0, 0, 0.0
        for i in range(2000):
            ei = reach_arr[(i, r)]
            if len(ei) == 0: continue
            a0 = scores[origins_eid[i]]
            v = scores[ei]
            ok = np.isfinite(v)
            if not ok.any() or not np.isfinite(a0): continue
            g = v[ok].max() - a0
            tot += 1; pos += g > 0; gsum += g
        out[r] = (pos / tot if tot else np.nan, gsum / tot if tot else np.nan)
    return out

period = "weekday_17"  # primary null period; also weekend_23 as secondary check
PERM_PERIODS = ["weekday_17", "weekend_23"]
permres = {}
for per in PERM_PERIODS:
    base = cand[f"A_C_{per}"].to_numpy()
    finite = np.isfinite(base)
    obs = perm_stats(base)
    nulls = {r: [] for r in [100, 200, 300, 500]}
    for p in range(NPERM):
        ps = base.copy()
        idx = np.where(finite)[0]
        ps[idx] = base[idx][rng.permutation(len(idx))]
        st = perm_stats(ps)
        for r in nulls: nulls[r].append(st[r])
        if p % 50 == 0: print("perm", per, p, flush=True)
    permres[per] = {"obs": obs, "null": nulls}
    for r in [100, 200, 300, 500]:
        nf = np.array([x[0] for x in nulls[r]]); ng = np.array([x[1] for x in nulls[r]])
        pf = (1 + (nf >= obs[r][0]).sum()) / (1 + NPERM)
        pg = (1 + (ng >= obs[r][1]).sum()) / (1 + NPERM)
        print(f"{per} r={r}: frac_pos obs={obs[r][0]:.3f} null={nf.mean():.3f} p={pf:.4f} | "
              f"meanG obs={obs[r][1]:.3f} null={ng.mean():.3f} p={pg:.4f}")
json.dump({p: {"obs": permres[p]["obs"], "null_mean": {str(r): [float(np.mean([x[0] for x in permres[p]['null'][r]])), float(np.mean([x[1] for x in permres[p]['null'][r]]))] for r in [100,200,300,500]}} for p in PERM_PERIODS},
          open(f"{TAB}/permutation_null.json", "w"), indent=1)

# constrained null: within-ward permutation
per = "weekday_17"
base = cand[f"A_C_{per}"].to_numpy()
obs = perm_stats(base)
nullw = {r: [] for r in [100, 200, 300, 500]}
ward_groups = {}
for w in pd.unique(cand_ward):
    ward_groups[w] = np.where(cand_ward == w)[0]
for p in range(NPERM):
    ps = base.copy()
    for w, idx in ward_groups.items():
        ps[idx] = base[idx][rng.permutation(len(idx))]
    st = perm_stats(ps)
    for r in nullw: nullw[r].append(st[r])
    if p % 50 == 0: print("wardperm", p, flush=True)
for r in [100, 200, 300, 500]:
    nf = np.array([x[0] for x in nullw[r]]); ng = np.array([x[1] for x in nullw[r]])
    print(f"ward r={r}: frac_pos obs={obs[r][0]:.3f} null={nf.mean():.3f} "
          f"p={(1+(nf>=obs[r][0]).sum())/(1+NPERM):.4f} | "
          f"meanG obs={obs[r][1]:.3f} null={ng.mean():.3f} "
          f"p={(1+(ng>=obs[r][1]).sum())/(1+NPERM):.4f}")
np.savez(f"{PROC}/perm_null_arrays.npz",
         **{f"{per}_{r}": np.array(nulls[r]) for per in PERM_PERIODS for r in [100,200,300,500]
            for nulls in [permres[per]["null"]]},
         **{f"ward_{r}": np.array(nullw[r]) for r in [100,200,300,500]})
print("done")
