# FINAL PUBLIC REPRODUCTION

Classification: **PUBLIC PARTIAL REPRODUCTION**.

- Manuscript stage (tables -> canonical registry -> figures -> docx):
  FULLY REPRODUCIBLE from the public repository alone.
- Raw stage (OSM/NLNI download -> network -> ablation tables):
  requires re-running `download_data.py` + `run_ceus_analyses.py`, which
  re-downloads public OSM/NLNI/PDOK inputs (network-bound, hours). Inputs
  are public; no licensed input is required, so this is PARTIAL (not
  "requires external licensed input") — it is re-runnable but heavy.

Clean-room evidence (this audit):
1. `git clone https://github.com/bougtoir/street-hail-taxi-accessibility` to /tmp/sht_repro.
2. `python3 analysis/build_canonical_results.py` -> 17 ablation cells, 36
   transfer cells, byte-identical canonical_results.json to the private
   working copy.
3. `python3 analysis/renumber_figures_qc.py` -> 9 figures renamed per
   first-citation order; FAIL-LOUD on any missing source.
4. `python3 analysis/build_manuscript_final_qc.py` -> manuscript/cover/
   highlights regenerated; extracted prose identical to the private build.
5. Required processed input `data/processed/perm_null_arrays.npz` IS
   committed in the public repo (12 null arrays, verified loadable).

FAIL-LOUD behavior: builders exit non-zero on missing canonical keys,
missing figures, or missing npz — no silent defaults.
