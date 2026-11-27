# IJGIS Open Data + FAIR audit

IJGIS requirement (Data and Codes Availability, as quoted in an IJGIS article, doi:10.1080/13658816.2025.2603586; T&F Open Data + FAIR): anonymize data and code, deposit in a DOI-minting repository such as Figshare or Dryad, give a private sharing link for review in the Data and Codes Availability Statement, use an open licence, and avoid "available on request".

| FAIR element | Status | Evidence |
|---|---|---|
| Findable: persistent identifier | NOT YET. Figshare DOI is minted only when the author creates the item. | AUTHOR ACTION |
| Findable: metadata | Bundle README lists pipeline, inputs, licences, seeds | `analysis/anon_bundle/REPRO_README.md` |
| Accessible: private link for review | NOT YET (placeholder `[FIGSHARE PRIVATE SHARING LINK]` in the statement) | AUTHOR ACTION |
| Accessible: public code | public mirror (identifying; not cited in the blinded file) | title page only |
| Interoperable: open formats | CSV, JSON, Parquet, GeoJSON-capable code, PNG/PDF figures | bundle manifest |
| Reusable: licence | MIT for code and CC BY 4.0 for derived tables proposed in the statement; LICENSE file in bundle. The public mirror currently has NO LICENSE file. | AUTHOR to confirm licence choice |
| Reusable: provenance | canonical registry `analysis/canonical_results.json`; Overpass raw responses (`cache/*.json`); acquisition code `analysis/download_data.py` | bundle |
| Third-party data terms | OSM (ODbL), MLIT NLNI (MLIT terms), Tokyo Taxi Center survey (aggregate figures cited, no microdata redistributed) | manuscript Table 1 |
| Raw-data snapshot completeness | PARTIAL. Overpass responses are archived (`cache/`). The original `data/raw/` derived snapshots (GraphML, POI GeoJSON, NLNI N02 zip, `acquisition_ledger.jsonl`) were git-ignored in earlier sessions and are not present in the repository or this VM. See section below. | disclosed |
| Reproduction of reported numbers | PASS: in a clean copy, `build_canonical_results.py` regenerates `canonical_results.json` byte-identically (SHA-256 ee1ce5bb...) from the archived result tables, and the builder regenerates identical manuscript text. | IJGIS_FINAL_QC_REPORT.md |

## Raw-data gap

A re-acquisition with the archived Overpass cache was attempted in a clean copy (see `IJGIS_FINAL_QC_REPORT.md`, section "Raw re-acquisition"). Any re-downloaded files are stored separately under `data/raw/source_redownload_20261110/` with their own checksums and are NOT treated as the original snapshot; differing checksums would mean a re-acquisition, not an exact reproduction of the original inputs.

Status: CONDITIONAL. Compliant statement and anonymized bundle prepared; private link, DOI and licence confirmation are author actions.

## Review-stage status (2026-11-10)
- Findable/Accessible during review: anonymized bundle reachable through a private Zenodo draft link. No account is needed. The download was verified unauthenticated, and its SHA-256 matches the local bundle.
- Not public and no DOI: by design until acceptance. Persistent identification is deferred (IJGIS_DATA_CODE_AVAILABILITY_PLAN.md) and no DOI is claimed.
- Interoperable/Reusable: CSV/JSON/Parquet/NPZ outputs, canonical registry, README and LICENSE are inside the bundle.
- Verdict: **compliant at the review stage**. Public FAIR archiving (DOI) is a post-acceptance action.
