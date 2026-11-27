# TGIS citation ecology — final

Bibliography: **51 items** = 44 existing items (none removed; Crossref-corrected DOI/year/author metadata kept) + 6 Transactions in GIS papers + 1 data/code repository citation. Every item is cited (QC gate 11) and every citation resolves (gate 12). All 50 DOIs have archived Crossref records (`data/raw/crossref_ijgis/`, `data/raw/crossref_tgis/`; gate 10).

| Added | Where cited | Supported sentence |
|---|---|---|
| Couclelis (2003); Devillers et al. (2010) | Introduction, SDQ paragraph | "Uncertainty arises not only from measurement error in spatial data but also from the representational choices through which geographic knowledge is constructed" |
| Kim & Horner (2024); Almusidi (2025) | same paragraph (with Fotheringham & Wong 1991; Greco et al. 2019) | "variable choice, weighting, aggregation, scale and network or location encoding can each change a constructed result" |
| Aerts et al. (2003) | same paragraph; §4.6 | "uncertainty in input data propagates into the solutions of optimization models" |
| Murray & Baik (2023) | same paragraph | "spatial optimization is increasingly embedded in GIS-based planning workflows" |
| Onishi (2026) [repository] | Data Availability Statement | location of derived data, registry and code |

Final composition: spatial sciences/GIS 2; spatial data quality/uncertainty 7 (+Couclelis, Devillers, Aerts); spatial analysis/reproducibility 1; spatial statistics/null models 5; spatial networks 3; accessibility 9 (+Kim & Horner, Almusidi); decision support/indicators/optimization 5 (+Murray & Baik); taxi/transport 7; robustness/specification 4; infrastructure siting 4; data sources 4 (+repository). Transactions in GIS papers: 6 of 51 (12%), each tied to a specific sentence; no self-citation besides the data repository.

## Correction found by the TGIS reference check (reported, not hidden)

- `taxi_demand2` (Hwang, Hsueh, & Chen, 2015): the DOI carried in earlier versions (10.1016/j.ins.2015.03.047) resolves to an unrelated control-theory article; the earlier check had matched only the DOI string. Crossref title search (`data/raw/crossref_tgis/q11_hwang2015.json`) gives the correct record 10.1016/j.ins.2015.03.068, *Information Sciences*, 314, 28–40 (`doi_10.1016_j.ins.2015.03.068.json`). Author, title, year, journal and volume were already correct; DOI and pages are corrected. The supported claim is unchanged. QC gate 2 now checks first author **and** title overlap against Crossref for every DOI.
