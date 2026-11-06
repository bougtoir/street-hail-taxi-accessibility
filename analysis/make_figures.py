#!/usr/bin/env python3
"""Phase 17: figures 1-6 (vector PDF + PNG)."""
import os, json, math, numpy as np, pandas as pd, geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import matplotlib.patheffects as pe

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC, FIG, RAW = f"{ROOT}/data/processed", f"{ROOT}/figures", f"{ROOT}/data/raw"
os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.size": 9, "figure.dpi": 150, "savefig.bbox": "tight"})

df = pd.read_parquet(f"{PROC}/relocation_results.parquet")
seg = pd.read_parquet(f"{PROC}/segments.parquet")

def save(fig, name):
    fig.savefig(f"{FIG}/{name}.pdf"); fig.savefig(f"{FIG}/{name}.png")
    plt.close(fig); print(name)

# ---- Figure 1: conceptual framework ---------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 2.2))
labels = ["Public data\n(OSM, NLNI,\nTokyo taxi stats)",
          "Taxi-flow prior +\naccessibility specs\n(A/B/C)",
          "Walking\nneighborhood\n(100-500 m)",
          "Optimal road\nsegment &\nrelocation gain"]
xs = np.linspace(0.05, 0.95, 4)
for x, lab in zip(xs, labels):
    ax.add_patch(mpatches.FancyBboxPatch((x - 0.10, 0.3), 0.19, 0.4,
                boxstyle="round,pad=0.02", fc="#e8f0fe", ec="#3367d6"))
    ax.text(x - 0.005, 0.5, lab, ha="center", va="center", fontsize=8)
for x0, x1 in zip(xs[:-1], xs[1:]):
    ax.annotate("", xy=(x1 - 0.105, 0.5), xytext=(x0 + 0.095, 0.5),
                arrowprops=dict(arrowstyle="->", lw=1.4, color="#333"))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
save(fig, "fig1_framework")

# ---- Figure 2: accessibility map ------------------------------------------
geo = gpd.read_file(f"{PROC}/segments.geojson")
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6))
for ax, per in zip(axes, ["weekday_17", "weekend_23"]):
    geo["av"] = geo[f"A_C_{per}"]
    geo.plot(ax=ax, column="av", cmap="viridis", lw=0.4, legend=False,
             vmin=np.nanpercentile(geo.av, 2), vmax=np.nanpercentile(geo.av, 98))
    ax.set_title({"weekday_17": "Weekday 17:00", "weekend_23": "Weekend 23:00"}[per])
    ax.axis("off")
sm = plt.cm.ScalarMappable(cmap="viridis",
    norm=plt.Normalize(np.nanpercentile(geo.av, 2), np.nanpercentile(geo.av, 98)))
fig.colorbar(sm, ax=axes, shrink=0.7, label="Street-hail accessibility A (SD units)")
save(fig, "fig2_map")

# ---- Figure 3: worked example ---------------------------------------------
rng = np.random.default_rng(42)
base = seg
cand = base[base.hail_ok].reset_index(drop=True)
orig_idx = rng.choice(len(cand), 2000, replace=False)
reach = [{int(k): v for k, v in r.items()} for r in
         json.load(open(f"{PROC}/reach.json"))]
# pick an origin where optimizer beats nearest-major clearly
d3 = df[(df.model == "A_C") & (df.radius == 200) & (df.period == "weekday_17")]
pick = d3[(d3.G_A > 0.5) & (d3.G_A - d3.gain_nearmajor > 0.4)].iloc[0]
i = int(pick.origin)
orow = cand.iloc[orig_idx[i]]
items = [(k, v) for k, v in reach[i].items() if v <= 200]
ei = np.array([k for k, _ in items]); di = np.array([v for _, v in items])
cc = cand.iloc[ei]
col = "A_C_weekday_17"
v = cc[col].to_numpy(); ok = np.isfinite(v)
cc, di, v = cc[ok], di[ok], v[ok]
best = int(np.argmax(v))
maj = cc.w_road.to_numpy() >= 0.99
nearmaj_i = np.argmin(di[maj]) if maj.any() else 0
fig, ax = plt.subplots(figsize=(5.2, 5.2))
geo2 = geo[(geo.mx > orow.mx - 0.003) & (geo.mx < orow.mx + 0.003) &
           (geo.my > orow.my - 0.0025) & (geo.my < orow.my + 0.0025)]
geo2.plot(ax=ax, color="#cccccc", lw=0.6)
ax.scatter(cc.mx, cc.my, s=6, c=v, cmap="viridis", zorder=3, label="Reachable segments")
ax.scatter([orow.mx], [orow.my], marker="*", s=200, c="red", zorder=5, label="Origin")
ax.scatter([cc.mx.iloc[best]], [cc.my.iloc[best]], marker="o", s=90,
           facecolor="none", edgecolor="red", lw=2, zorder=6, label="Optimum")
ax.scatter([cc.mx.iloc[maj.nonzero()[0][nearmaj_i]]],
           [cc.my.iloc[maj.nonzero()[0][nearmaj_i]]], marker="s", s=70,
           facecolor="none", edgecolor="blue", lw=2, zorder=6, label="Nearest major road")
ax.legend(fontsize=7, loc="best"); ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
save(fig, "fig3_worked_example")

# ---- Figure 4: gain distribution by radius ---------------------------------
d4 = df[df.model == "A_C"]
fig, ax = plt.subplots(figsize=(5.5, 3.4))
data = [d4[d4.radius == r].G_A.dropna() for r in [100, 200, 300, 500]]
parts = ax.violinplot(data, showmedians=True)
ax.set_xticks(range(1, 5), [100, 200, 300, 500])
ax.set_xlabel("Walking radius (m)"); ax.set_ylabel("Accessibility gain G_A (SD units)")
save(fig, "fig4_gain_by_radius")

# ---- Figure 5: strategy comparison -----------------------------------------
d5 = df[(df.model == "A_C")]
strategies = [("Stay (A0)", d5.A0), ("Random", d5.A_random),
              ("Nearest major", d5.A_nearmajor), ("Flow-only optimum", d5.A_flow),
              ("Full optimizer", d5.Astar)]
fig, ax = plt.subplots(figsize=(5.8, 3.4))
means = [s.mean() for _, s in strategies]
sem = [s.std() / np.sqrt(s.notna().sum()) for _, s in strategies]
ax.bar([n for n, _ in strategies], means, yerr=sem, capsize=3,
       color=["#999", "#ccc", "#88a", "#6a8", "#3367d6"])
ax.set_ylabel("Mean accessibility (SD units)"); ax.tick_params(axis="x", rotation=20)
save(fig, "fig5_strategies")

# ---- Figure 6: temporal + ward heterogeneity -------------------------------
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2))
t = d5.groupby("period").G_A.mean().reset_index()
t["day"] = t.period.str[:7]; t["hour"] = t.period.str[-2:].astype(int)
for dy, g in t.groupby("day"):
    g = g.sort_values("hour")
    axes[0].plot(g.hour, g.G_A, "o-", label=dy)
axes[0].set_xlabel("Hour"); axes[0].set_ylabel("Mean G_A"); axes[0].legend()
w = d5.groupby(["ward", "radius"]).G_A.mean().unstack()
w.loc[[x for x in ["Chiyoda", "Chuo", "Minato", "Shinjuku", "Shibuya"] if x in w.index]].T.plot(ax=axes[1], marker="o")
axes[1].set_xlabel("Radius (m)"); axes[1].set_ylabel("Mean G_A")
axes[1].legend(fontsize=7)
save(fig, "fig6_heterogeneity")
print("figures done")
