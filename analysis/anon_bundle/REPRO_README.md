# Anonymized reproduction bundle (peer review copy)

Study: internal stress tests for constructed spatial opportunity surfaces (street-hail relocation demonstration, five central Tokyo wards). Python 3.10; osmnx 2.0.7, geopandas, networkx, scipy, pandas, statsmodels, scikit-learn, matplotlib. Fixed seed 42.

## Quick check (minutes): regenerate every reported number

    python analysis/build_canonical_results.py

reads `tables/*.csv|json` and rewrites `analysis/canonical_results.json`; compare its SHA-256 with `MANIFEST.csv`. Every number printed in the manuscript is read from this registry.

## Full pipeline (hours)

1. `python analysis/download_data.py all` — OSM drive/walk networks and POIs via Overpass (archived responses in `cache/` are used by OSMnx, so the networks are rebuilt without new queries), MLIT N02 stations; writes `data/raw/acquisition_ledger.jsonl` with SHA-256.
2. `python analysis/build_segments.py` (SIGMA env: 300 default; 150/500 sensitivity)
3. `python analysis/run_relocation.py`
4. `python analysis/analyze_stats.py`
5. `python analysis/run_ablation.py`
6. `python analysis/run_ceus_analyses.py` — clustered inference, cross-specification transfer, permutation nulls (script name is historical)
7. `python analysis/make_figures.py`, `analysis/make_ceus_figures.py`, `analysis/make_framework_figure.py`
8. `python analysis/build_canonical_results.py`

OSM is a live database: if `cache/` is absent, a re-download reflects the current map and can differ from the archived snapshot.

## Contents

See `MANIFEST.csv` (path, bytes, SHA-256). Licences: `LICENSE`.
