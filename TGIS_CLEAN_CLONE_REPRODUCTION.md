# TGIS clean-clone reproduction

Date (UTC): 2026-11-24. Source: logged-out clone of the public repository https://github.com/bougtoir/street-hail-taxi-accessibility (main = 30cb0d6), cloned with global/system git config disabled and no credentials.

| Step | Command | Result |
|---|---|---|
| fresh environment | `python3 -m venv venv` (Python 3.10.12); `pip install -r requirements.txt` (numpy 2.2.6, pandas 2.3.3, osmnx 2.0.7, geopandas 1.1.4, …) | PASS |
| manifest | `python tests/verify_reproduction.py` | PASS manifest: 93 files match SHA-256 |
| canonical registry | same script runs `analysis/build_canonical_results.py` | PASS byte-identical, SHA-256 ee1ce5bb26df5605aec7b803c459056b525de133b7f1d9bf8e81d448e33a22ac |
| article documents | `pip install python-docx==1.2.0`; `python analysis/make_tgis_bib.py && python analysis/make_tgis_builder.py && python analysis/build_manuscript_tgis.py` | PASS: 51 references, 5,722 words, abstract 135; manuscript, title page, cover letter and editable tables text-identical to the submitted files (paragraphs and table cells); Figure_1–9.png byte-identical; TGIS_MANUSCRIPT_STATS.json identical |
| tracked files after rebuild | `git status` | only DOCX containers differ (zip timestamps); `analysis/canonical_results.json` unchanged |

Scope and limitation: the check regenerates every reported number, table, figure file and the documents from the archived derived data in the public repository. It does not re-run the hours-long optimization or re-acquire raw inputs; original raw-stage snapshots (GraphML, POI GeoJSON, N02 zip) and the original POI Overpass responses were not retained, so full raw-stage recreation is not claimed (as stated in the Data Availability Statement).

Verdict: PASS.
