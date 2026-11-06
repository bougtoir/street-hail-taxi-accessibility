#!/usr/bin/env python3
"""CEUS figures: fig7 ablation (regenerated), fig8 transfer matrix, fig9 permutation null."""
import os, json, numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAB, FIG = f"{ROOT}/tables", f"{ROOT}/figures"

abl = pd.read_csv(f"{TAB}/ablation_summary_clustered.csv")
NAME = {"ROAD": "Road-only", "ATTR": "Attractor-only", "PROXY": "Circulation proxy", "COMB": "Combined"}
COL = {"ROAD": "#1f77b4", "ATTR": "#2ca02c", "PROXY": "#9467bd", "COMB": "#d62728"}

fig, axs = plt.subplots(1, 3, figsize=(13, 4))
for spec in ["ROAD", "ATTR", "PROXY", "COMB"]:
    s = abl[abl.spec == spec]
    axs[0].plot(s.radius, s.frac_pos, "o-", label=NAME[spec], color=COL[spec])
    axs[1].plot(s.radius, s.gt_nearmaj, "o-", label=NAME[spec], color=COL[spec])
agr = pd.read_csv(f"{TAB}/ablation_rank_agreement.csv")
m = agr.groupby("spec").spearman.mean()
axs[2].bar([NAME[s] for s in m.index], m.values, color=[COL[s] for s in m.index])
axs[0].set(ylabel="Fraction of origins improved", xlabel="Walking radius (m)"); axs[0].legend(fontsize=8)
axs[1].set(ylabel="Fraction beating nearest major road", xlabel="Walking radius (m)")
axs[2].set(ylabel="Spearman rho vs combined", ylim=(0, 1)); axs[2].tick_params(axis="x", rotation=20)
fig.tight_layout(); fig.savefig(f"{FIG}/fig7_ablation.pdf"); fig.savefig(f"{FIG}/fig7_ablation.png", dpi=200)
plt.close(fig)

# fig8: selector x evaluator transfer matrix at 300 m
ts = pd.read_csv(f"{TAB}/transfer_summary.csv")
t3 = ts[ts.radius == 300]
specs = ["ROAD", "ATTR", "PROXY", "COMB"]
mat = np.full((4, 4), np.nan)
frac = np.full((4, 4), np.nan)
for _, r in t3.iterrows():
    i, j = specs.index(r.selector), specs.index(r.evaluator)
    mat[i, j] = r.mean_TG; frac[i, j] = r.frac_pos
fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))
im = axs[0].imshow(mat, cmap="viridis")
axs[0].set_xticks(range(4), [NAME[s] for s in specs], rotation=20)
axs[0].set_yticks(range(4), [NAME[s] for s in specs])
axs[0].set(xlabel="Evaluation specification", ylabel="Selection specification",
           title="Mean transfer gain (SD units), 300 m")
for i in range(4):
    for j in range(4):
        if np.isfinite(mat[i, j]):
            axs[0].text(j, i, f"{mat[i,j]:.2f}", ha="center", va="center",
                        color="white" if mat[i, j] < np.nanmax(mat) * 0.6 else "black", fontsize=9)
fig.colorbar(im, ax=axs[0], shrink=0.8)
im2 = axs[1].imshow(frac, cmap="magma", vmin=0, vmax=1)
axs[1].set_xticks(range(4), [NAME[s] for s in specs], rotation=20)
axs[1].set_yticks(range(4), [NAME[s] for s in specs])
axs[1].set(xlabel="Evaluation specification", ylabel="Selection specification",
           title="Fraction of origins with transfer gain > 0")
for i in range(4):
    for j in range(4):
        if np.isfinite(frac[i, j]):
            axs[1].text(j, i, f"{frac[i,j]:.2f}", ha="center", va="center",
                        color="white" if frac[i, j] < 0.6 else "black", fontsize=9)
fig.colorbar(im2, ax=axs[1], shrink=0.8)
fig.suptitle("Cross-specification transfer: off-diagonal entries show transfer between distinct constructions")
fig.tight_layout(); fig.savefig(f"{FIG}/fig8_transfer_matrix.pdf"); fig.savefig(f"{FIG}/fig8_transfer_matrix.png", dpi=200)
plt.close(fig)

# fig9: permutation null vs observed (weekday_17)
nz = np.load(f"{ROOT}/data/processed/perm_null_arrays.npz")
fig, axs = plt.subplots(1, 2, figsize=(11, 4))
obs = json.load(open(f"{TAB}/permutation_null.json"))["weekday_17"]["obs"]
nf = np.array([x[0] for x in nz["weekday_17_300"]]); ng = np.array([x[1] for x in nz["weekday_17_300"]])
axs[0].hist(nf, bins=30, color="gray", alpha=0.7, label="Permutation null (500)")
axs[0].axvline(obs["300"][0], color="red", lw=2, label=f"Observed = {obs['300'][0]:.3f}")
axs[0].set(xlabel="Fraction of origins with positive gain", ylabel="Permutations",
           title="Any-improvement rate, 300 m (weekday 17:00)"); axs[0].legend(fontsize=8)
axs[1].hist(ng, bins=30, color="gray", alpha=0.7, label="Permutation null (500)")
axs[1].axvline(obs["300"][1], color="red", lw=2, label=f"Observed = {obs['300'][1]:.2f}")
axs[1].set(xlabel="Mean absolute gain (SD units)", ylabel="Permutations",
           title="Mean relocation gain, 300 m (weekday 17:00)"); axs[1].legend(fontsize=8)
fig.tight_layout(); fig.savefig(f"{FIG}/fig9_permutation_null.pdf"); fig.savefig(f"{FIG}/fig9_permutation_null.png", dpi=200)
plt.close(fig)
print("ceus figures done")
