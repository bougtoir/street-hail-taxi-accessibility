#!/usr/bin/env python3
"""Regenerate the stress-test framework figure (final terminology).
Output: figures/fig1_framework.{pdf,png} — Figure 8 in first-citation order."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = f"{ROOT}/figures"
os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.size": 9, "figure.dpi": 150, "savefig.bbox": "tight"})

steps = ["Public\nurban data\n(OSM, NLNI,\ntaxi statistics)",
         "Alternative\nproxy\nconstructions",
         "Local\noptimization\n(100-500 m)",
         "Component\nablation",
         "Cross-spec.\ntransfer",
         "Spatial\npermutation\nnull",
         "Heuristic\ncomparison",
         "Calibrated\ninterpretation"]

fig, ax = plt.subplots(figsize=(8.6, 2.1))
xs = np.linspace(0.065, 0.935, len(steps))
for x, lab in zip(xs, steps):
    ax.add_patch(mpatches.FancyBboxPatch((x - 0.055, 0.30), 0.11, 0.48,
                boxstyle="round,pad=0.012", fc="#e8f0fe", ec="#3367d6"))
    ax.text(x, 0.54, lab, ha="center", va="center", fontsize=6.9,
            linespacing=1.25)
for x0, x1 in zip(xs[:-1], xs[1:]):
    ax.annotate("", xy=(x1 - 0.058, 0.54), xytext=(x0 + 0.058, 0.54),
                arrowprops=dict(arrowstyle="->", lw=1.0, color="#333"))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
fig.savefig(f"{FIG}/fig1_framework.pdf"); fig.savefig(f"{FIG}/fig1_framework.png")
plt.close(fig); print("fig1_framework")
