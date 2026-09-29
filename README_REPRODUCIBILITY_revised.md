# REPRODUCIBILITY — street-hail-taxi (REVISED package)

Pipeline (seeded, deterministic):
1. analysis/download_data.py all      # raw snapshots + SHA-256 ledger
2. analysis/build_segments.py         # segments + proxy + A/B/C scores
3. analysis/run_relocation.py         # origins, reachability, strategies
4. analysis/analyze_stats.py          # baseline tables
5. analysis/run_ablation.py           # NEW: ROAD/ATTR/PROXY/COMB ablation
6. analysis/make_figures.py           # fig1-6 (+ fig7 inline snippet)
7. analysis/build_manuscript_revised.py  # revised docx + cover letter
8. soffice --headless --convert-to pdf ... # clean revised PDF

Revised outputs: output/*_revised.*, tables/ablation_*.csv,
figures/fig7_ablation.*. Governance docs: *_revised.md set. Data provenance:
data/raw/acquisition_ledger.jsonl (URL, UTC, SHA-256, license).
