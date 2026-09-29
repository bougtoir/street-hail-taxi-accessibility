# REPRODUCIBILITY — FINAL (CEUS)

Pipeline order (seeded):
1. analysis/download_data.py all
2. analysis/build_segments.py            # SIGMA env: 300 default; 150/500 variants
3. analysis/run_relocation.py            # caches reach.json
4. analysis/analyze_stats.py
5. analysis/run_ablation.py              # component specs + baselines
6. analysis/run_ceus_analyses.py         # clustered inference, transfer, permutation nulls
7. analysis/make_figures.py              # fig1-6
8. analysis/make_ceus_figures.py         # fig7 ablation, fig8 transfer matrix, fig9 permutation
9. analysis/build_manuscript_ceus.py     # docx + highlights + cover letter
10. soffice --headless --convert-to pdf

Final package: output/CEUS_submission_FINAL.zip. Provenance:
data/raw/acquisition_ledger.jsonl. Known correction: N02 station passenger
weights removed (field absent in FY2023); station-presence kernel used.
