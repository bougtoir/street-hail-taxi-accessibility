# IJGIS citation ecology — final

Bibliography: 44 items = all 41 previous items retained + 3 additions. No item removed. Every item is cited in text (QC gate G08) and every DOI has an archived Crossref record (`data/raw/crossref_ijgis/`, gate G06).

## Additions (each supports a specific sentence)

| Added reference | Crossref check | Where cited | Claim supported |
|---|---|---|---|
| Goodchild, M.F., 1992. Geographical information science. *IJGIS* 6 (1), 31–45. doi:10.1080/02693799208901893 | `goodchild1992.json` (title, volume, pages match) | Introduction, paragraph 1 | constructed surfaces are geographic information products in the GIScience sense |
| Heuvelink, G.B.M., Burrough, P.A., and Stein, A., 1989. Propagation of errors in spatial modelling with GIS. *IJGIS* 3 (4), 303–322. doi:10.1080/02693798908941518 | `heuvelink1989.json` | Introduction paragraph 2; Discussion 4.6 | uncertainty in inputs and specification propagates to derived outputs; the stress tests ask the decision-level complement |
| Kedron, P., Li, W., Fotheringham, S., and Goodchild, M., 2021. Reproducibility and replicability: opportunities and challenges for geospatial research. *IJGIS* 35 (3), 427–445. doi:10.1080/13658816.2020.1802032 | `kedron2021.json` | Methods 2.13; Discussion 4.6 | reproducibility/replicability across analysts and specifications is a recognized geospatial challenge |

## Considered and not added

Candidates on spatial cross-validation, geographically weighted models, UGCoP, and spatial data quality were considered, but none supports a sentence the manuscript actually makes without adding new claims; they were not added (no citation gaming).

## Final composition

GIScience/representation 4 (Goodchild 1992, Heuvelink et al. 1989, Kedron et al. 2021, Longley et al. 2015); accessibility 7; MAUP/scale 3; spatial autocorrelation/nulls 5; robustness/specification 8; taxi/mobility 10; infrastructure siting 4; data sources 3. IJGIS papers: 3 (all directly relevant). Taxi literature is 10/44, consistent with its role as the empirical demonstration rather than the novelty.

## Corrections to pre-existing metadata (found by Crossref check, reported, not hidden)

- `nicholas2004`: the DOI in the earlier list resolves to Melendez and Milbrandt (2008), not Nicholas and Ogden (2004); the reference now matches the DOI (same supporting claim: hydrogen station siting under prospective demand).
- `gelman2014`: the Gelman and Loken manuscript is dated 2013; corrected.
- Further DOI/page/year fixes are listed in `IJGIS_REFERENCE_AUDIT.md`.
