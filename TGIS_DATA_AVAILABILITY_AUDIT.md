# TGIS data availability audit

Requirement: Data Availability Statement mandatory (Wiley data sharing policy, live); journal expects public repository deposit and public archiving of scripts (TGIS guidelines, Wayback 2022-03-08). See TGIS_CURRENT_REQUIREMENTS.md rows 12–13.

| Material | Where | Public? | Licence / terms | DAS wording | Status |
|---|---|---|---|---|---|
| OpenStreetMap road, pedestrian, POI data | Overpass API via OSMnx 2.0.7; archived Overpass responses `cache/*.json` (pedestrian/drive network queries) | Yes (source); cached responses in repository | ODbL 1.0, © OpenStreetMap contributors | "Public source data … (ODbL)" | OK |
| Japanese public geospatial data: National Land Numerical Information N02 railway stations FY2023 | MLIT download (`analysis/download_data.py`) | Yes (source) | MLIT terms of use | "National Land Numerical Information railway data (N02, FY2023; MLIT terms of use)" | OK |
| Tokyo Taxi Center monitor survey; Tokyo Hire-Taxi Association statistics | published reports (aggregate figures cited only) | Yes (reports) | publisher terms; no microdata redistributed | Table 1 | OK |
| Derived study data | `data/processed/*.parquet|npz`, `tables/` | Yes (public repository) | CC BY 4.0 | "Derived study data … openly available" | OK once repository is public |
| Canonical numerical registry | `analysis/canonical_results.json` (SHA-256 ee1ce5bb…a22ac) | Yes | CC BY 4.0 | "canonical numerical registry from which every reported analysis value is generated" | OK |
| Machine-readable tables | `tables/*.csv|json` | Yes | CC BY 4.0 | "machine-readable result tables" | OK |
| Analysis and document-generation code | `analysis/*.py` | Yes | MIT | "analysis and document-generation code" | OK |
| Raw-data acquisition ledgers | `data/raw/*/ACQUISITION_LEDGER.csv|acquisition_ledger.jsonl` (public-data provenance only) | Yes | — | "raw-data acquisition ledger with SHA-256 checksums" | OK |
| Original raw-stage snapshots (GraphML, POI GeoJSON, N02 zip) | not retained from the original run | No | — | "original point-of-interest responses were not retained … full raw-stage recreation is therefore not claimed" | Limitation stated |
| Re-acquired inputs | `data/raw/source_redownload_20261110/` (separate, own checksums) | Yes | source terms | not presented as the original snapshot | OK |
| Publisher guideline snapshots | `data/raw/journal/` | No (kept in private working repository; third-party copyrighted pages) | publisher copyright | not cited as data | OK |

Licences file: `LICENSE` (MIT code; CC BY 4.0 derived tables/figures; third-party terms retained).

Claims not made: full raw-stage reproduction; DOI-minted archive (GitHub repository cited instead; Onishi, 2026). Persistent archiving (e.g., Zenodo DOI) can be added at acceptance without changing any result.

Verdict: DAS compliant and non-overstated, conditional on the public repository being reachable (QC gate 34).
