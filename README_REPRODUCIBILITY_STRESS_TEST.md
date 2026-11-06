# REPRODUCIBILITY — STRESS TEST

Same pipeline as README_REPRODUCIBILITY_FINAL (steps 1-8 unchanged);
manuscript now built by analysis/build_manuscript_stress_test.py ->
output/CEUS_STRESS_TEST_*.{docx,pdf} and CEUS_STRESS_TEST_submission_FINAL.zip.
No new analyses or datasets were added during the reframing pass; all
numbers in the manuscript derive from tables/ablation_summary_clustered.csv,
tables/transfer_summary.csv, tables/permutation_null.json,
data/processed/perm_null_arrays.npz.

## FINAL_QC layer (2026-10-17)

- Canonical numerical registry: `analysis/canonical_results.json`, generated
  by `analysis/build_canonical_results.py` from the committed tables and
  `data/processed/perm_null_arrays.npz`. It is the single source for every
  analysis-derived number printed in the FINAL_QC manuscript.
- `analysis/build_manuscript_final_qc.py` loads values via `canon()` only;
  it exits non-zero on any missing key (fail-loud, no defaults).
- Figure files follow first-citation order
  (`analysis/renumber_figures_qc.py`): fig1_framework ... fig9_heterogeneity.
- Clean reproduction verified: a fresh clone regenerates byte-identical
  `canonical_results.json` and identical manuscript prose
  (see output/FINAL_PUBLIC_REPRODUCTION.md). Classification:
  PUBLIC PARTIAL REPRODUCTION (raw stage re-downloads public inputs).
- QC audit files: output/FINAL_QC_REPORT.md (20/20 PASS) and the
  FINAL_*_AUDIT / *_MATRIX artifacts.
