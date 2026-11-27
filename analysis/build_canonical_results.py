#!/usr/bin/env python3
"""Generate analysis/canonical_results.json — the single canonical numerical
registry for every analysis-derived value reported in the manuscript, tables,
figures, highlights, cover letter, and audit documents.

Every value is read FROM analysis outputs (tables/*.csv, tables/*.json,
data/processed/perm_null_arrays.npz, committed pipeline logs, DATA_SOURCE_AUDIT.md).
No analysis-derived value is typed manually; each entry carries its provenance.
"""
import json, re, os
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAB, PROC = f"{ROOT}/tables", f"{ROOT}/data/processed"

abl = pd.read_csv(f"{TAB}/ablation_summary_clustered.csv")
ts = pd.read_csv(f"{TAB}/transfer_summary.csv")
perm = json.load(open(f"{TAB}/permutation_null.json"))
sigma = json.load(open(f"{TAB}/sigma_sensitivity.json"))
agr = pd.read_csv(f"{TAB}/ablation_rank_agreement.csv")
nullarr = np.load(f"{PROC}/perm_null_arrays.npz")

def ci(v):
    return [float(x) for x in v] if isinstance(v, (list, tuple)) \
        else [float(x) for x in re.findall(r"-?\d+\.?\d*(?:e-?\d+)?", str(v))]

canon = {"_provenance": {}, "config": {}, "network": {}, "ablation": {},
         "transfer": {}, "permutation": {}, "sigma": {}, "agreement": {}}

# ---- network descriptors (analysis pipeline outputs, committed docs/logs) ----
log = open(f"{PROC}/ceus_rerun.log").read()
m = re.search(r"segments:\s*(\d+)\s*\|\s*hail_ok:\s*(\d+)", log)
canon["network"]["n_segments_total"] = int(m.group(1))
canon["network"]["n_segments_hail_ok"] = int(m.group(2))
canon["_provenance"]["network.n_segments_hail_ok"] = "data/processed/ceus_rerun.log 'hail_ok'"
audit = open(f"{ROOT}/DATA_SOURCE_AUDIT.md").read()
mw = re.search(r"osm_walk_graph\.graphml[^\d]*([\d,]+)\s*/\s*([\d,]+)", audit)
canon["network"]["n_walk_nodes"] = int(mw.group(1).replace(",", ""))
canon["network"]["n_walk_edges"] = int(mw.group(2).replace(",", ""))
canon["_provenance"]["network.n_walk_edges"] = "DATA_SOURCE_AUDIT.md (osm_walk_graph.graphml inventory)"

# ---- design / configuration parameters (allowed literals, not results) ----
canon["config"] = {
    "n_origins_planned": 2000, "seed": 42,
    "radii_m": [100, 200, 300, 500], "n_permutations": 500,
    "bootstrap_replicates": 5000, "kernel_sigma_m": 300, "n_wards": 5,
    "monitor_survey_n": 2662,
}
canon["_provenance"]["config"] = ("design constants set in analysis/"
    "run_relocation.py, run_ceus_analyses.py, download_data.py; "
    "monitor_survey_n from Tokyo Taxi Center monitor report (cited source)")

# ---- ablation summary (full grid) ----
for _, r in abl.iterrows():
    key = f"{r.spec}.{int(r.radius)}"
    canon["ablation"][key] = {
        "n_origins": int(r.n_origins), "n_rows": int(r.n_rows),
        "frac_pos": float(r.frac_pos), "frac_pos_ci": ci(r.frac_pos_ci),
        "frac_gt_01": float(r.frac_gt_01),
        "mean_G": float(r.mean_G), "ci_G": ci(r.ci_G),
        "gt_rand": float(r.gt_rand), "gt_nearmaj": float(r.gt_nearmaj),
        "diff_nearmaj": float(r.diff_nearmaj),
        "diff_nearmaj_ci": ci(r.diff_nearmaj_ci),
        "wilcoxon_p": float(r.wilcoxon_p),
        "best_is_major": float(r.best_is_major),
    }
canon["_provenance"]["ablation"] = "tables/ablation_summary_clustered.csv (run_ceus_analyses.py, clustered)"
n_eff = abl.n_origins
canon["ablation"]["n_origins_range"] = [int(n_eff.min()), int(n_eff.max())]

# ---- cross-specification transfer (full grid) ----
for _, r in ts.iterrows():
    key = f"{r.selector}_to_{r.evaluator}.{int(r.radius)}"
    canon["transfer"][key] = {
        "n_origins": int(r.n_origins),
        "mean_TG": float(r.mean_TG), "med_TG": float(r.med_TG),
        "ci_TG": ci(r.ci_TG),
        "frac_pos": float(r.frac_pos), "frac_gt_01": float(r.frac_gt_01),
    }
canon["_provenance"]["transfer"] = "tables/transfer_summary.csv (run_ceus_analyses.py)"

# ---- spatial permutation nulls ----
perm_periods = ["weekday_17", "weekend_23"]
for p in perm_periods:
    canon["permutation"][p] = {}
    for r in canon["config"]["radii_m"]:
        k = f"{p}_{r}"
        nf = np.array([x[0] for x in nullarr[k]])
        ng = np.array([x[1] for x in nullarr[k]])
        obs = perm[p]["obs"][str(r)]
        canon["permutation"][p][str(r)] = {
            "obs_frac": float(obs[0]), "obs_gain": float(obs[1]),
            "null_frac": float(nf.mean()), "null_gain": float(ng.mean()),
            "null_frac_sd": float(nf.std(ddof=1)), "null_gain_sd": float(ng.std(ddof=1)),
            "emp_p_frac": float((1 + (nf >= obs[0]).sum()) / (1 + len(nf))),
            "emp_p_gain": float((1 + (ng >= obs[1]).sum()) / (1 + len(ng))),
            "null_frac_over_obs": float(nf.mean() / obs[0]),
        }
canon["_provenance"]["permutation"] = ("tables/permutation_null.json + "
    "data/processed/perm_null_arrays.npz (run_ceus_analyses.py); empirical p "
    "= (1 + #{null >= obs})/(1 + N)")
# headline range: radii where observed exceeds null fraction is examined (>=200 m);
# 100 m p=1.0 is reported separately in text
pr = [canon["permutation"][p][str(r)]["emp_p_frac"]
      for p in perm_periods for r in [200, 300, 500]]
canon["permutation"]["emp_p_frac_range_200_500"] = [min(pr), max(pr)]
for p in perm_periods:
    pp = [canon["permutation"][p][str(r)]["emp_p_frac"] for r in [200, 300, 500]]
    canon["permutation"][p]["emp_p_frac_range_200_500"] = [min(pp), max(pp)]
ratios = [canon["permutation"][p][str(r)]["null_frac_over_obs"]
          for p in perm_periods for r in canon["config"]["radii_m"]]
canon["permutation"]["null_reproduces_frac_mean"] = float(np.mean(ratios))
canon["permutation"]["null_reproduces_frac_range"] = [min(ratios), max(ratios)]

# ---- rank agreement between constructions ----
canon["agreement"]["spearman_min"] = float(agr.spearman.min())
canon["agreement"]["spearman_max"] = float(agr.spearman.max())
canon["_provenance"]["agreement"] = "tables/ablation_rank_agreement.csv (spec vs COMB segment-rank Spearman)"

# ---- kernel-bandwidth sensitivity ----
canon["sigma"] = {k: float(v) if isinstance(v, (int, float)) else v
                  for k, v in sigma.items()}
canon["_provenance"]["sigma"] = "tables/sigma_sensitivity.json (SIGMA=150/500 reruns)"

with open(f"{ROOT}/analysis/canonical_results.json", "w") as f:
    json.dump(canon, f, indent=1)
print("canonical_results.json:", len(canon["ablation"]), "ablation cells,",
      len(canon["transfer"]), "transfer cells")
