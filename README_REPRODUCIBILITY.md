# REPRODUCIBILITY — street-hail-taxi

Public-data-only feasibility study: street-hail taxi accessibility + pedestrian relocation optimization, 5 central wards of Tokyo (Paper 1 of 2).

## Pipeline (run in order)

```bash
pip install osmnx geopandas scikit-learn statsmodels python-docx lxml
python3 analysis/download_data.py all        # OSM drive/walk graphs, POIs, NLNI N02, taxi reports (raw snapshots + SHA-256 ledger)
python3 analysis/build_segments.py           # directed segments + flow prior + A/B/C specs -> data/processed/segments.parquet
python3 analysis/run_relocation.py           # origins, walking neighborhoods, optimizer + heuristics -> tables/relocation_results.csv
python3 analysis/analyze_stats.py            # bootstrap CIs, agreement, sensitivity tables
python3 analysis/make_figures.py             # figures/fig1-6 (pdf+png)
python3 analysis/build_manuscript.py         # output/MANUSCRIPT_inline.docx, COVER_LETTER.docx
soffice --headless --convert-to pdf --outdir output output/MANUSCRIPT_inline.docx
```

Sensitivity variants: `SIGMA=150 SUFFIX=_sig150 python3 analysis/build_segments.py` (and `_sig500`).

## Provenance
- Raw snapshots: `data/raw/` with `acquisition_ledger.jsonl` (URL, UTC, bytes, SHA-256, license). Raw OSM/NLNI data are large; they are excluded from git (`.gitignore`) but fully regenerable from the URLs in the ledger.
- Fixed seed: 42 everywhere (origins, random-relocation draws, bootstrap).
- Manuscript numbers trace to `tables/*.csv` + `model_agreement.json` + `sigma_sensitivity.json` at build time (no hardcoded statistics).

## Deliverables
- `output/MANUSCRIPT_inline.docx` (figures/tables embedded, OMML equations, Vancouver refs)
- `output/MANUSCRIPT_clean.pdf`, `output/COVER_LETTER.docx`
- `output/STREET_HAIL_TAXI_submission.zip`
- Governance docs: GO_NOGO_REPORT, NOVELTY_ASSESSMENT, DATA_SOURCE_AUDIT, ACCESSIBILITY_MODEL_SPECIFICATION, METHODS_TECHNICAL_APPENDIX, HOSTILE_REVIEW, FINAL_HANDOFF
