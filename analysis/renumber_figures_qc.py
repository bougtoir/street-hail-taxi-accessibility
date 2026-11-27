#!/usr/bin/env python3
"""Renumber figure files into first-body-citation order for the FINAL_QC
manuscript. Writes figN_<desc>.{pdf,png} alongside the originals; the
originals are left in place for provenance (zip uses only the new set).

First-citation order in the FINAL_QC body:
  §1      -> Figure 1 framework        (regenerated, final terminology)
  §3.1    -> Figure 2 surface map
  §3.2    -> Figure 3 gain-by-radius   + Figure 4 worked example
  §3.3    -> Figure 5 strategies
  §3.4    -> Figure 6 ablation
  §3.5    -> Figure 7 transfer matrix
  §3.6    -> Figure 8 permutation null
  §3.8    -> Figure 9 heterogeneity
"""
import os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = f"{ROOT}/figures"

MAP = [
    ("fig1_framework", "fig1_framework"),          # regenerated upstream
    ("fig2_map", "fig2_map"),
    ("fig4_gain_by_radius", "fig3_gain_by_radius"),
    ("fig3_worked_example", "fig4_worked_example"),
    ("fig5_strategies", "fig5_strategies"),
    ("fig7_ablation", "fig6_ablation"),
    ("fig8_transfer_matrix", "fig7_transfer_matrix"),
    ("fig9_permutation_null", "fig8_permutation_null"),
    ("fig6_heterogeneity", "fig9_heterogeneity"),
]

for old, new in MAP:
    for ext in ["pdf", "png"]:
        src = f"{FIG}/{old}.{ext}"
        dst = f"{FIG}/{new}.{ext}"
        if not os.path.exists(src):
            raise SystemExit(f"FAIL-LOUD: missing figure source {src}")
        if src != dst:
            shutil.copyfile(src, dst)
    print(f"{old} -> {new}")
print("done")
