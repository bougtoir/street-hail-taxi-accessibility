# IJGIS — Final QC report v3 (2026-11-11)

Change since v2: reviewer access switched from the Zenodo private draft to the Anonymous GitHub snapshot https://anonymous.4open.science/r/anonymous-spatial-proxy-review-7E02/. The only manuscript text change is the Data and codes availability paragraph (paragraph diff vs v2: 1 paragraph; tables identical). Title page and cover letter availability paragraphs updated accordingly.

Automated gates (analysis/qc_ijgis.py): 25/25 PASS (output/IJGIS_QC_RESULTS.json).

| # | Required gate | Result | Evidence |
|---|---|---|---|
| 1 | Hostile review | PASS (unchanged science; v2 review stands) | HOSTILE_REVIEW_IJGIS_FINAL.md |
| 2 | Hard-coded number audit | PASS | G02 |
| 3 | Science freeze | PASS | canonical_results.json SHA-256 ee1ce5bb26df5605aec7b803c459056b525de133b7f1d9bf8e81d448e33a22ac; tables/ and figures/ no diff vs freeze base f51d0bb; G01 |
| 4 | Clean reproduction | PASS | fresh clone and fresh ZIP: manifest 65/65, registry byte-identical |
| 5 | Reference existence | PASS | G06 (Crossref archive) |
| 6 | Citation coverage | PASS | G07, G08 (44/44) |
| 7 | Figure coverage | PASS | G09, G10, G13 (9 inline) |
| 8 | Table coverage | PASS | G11, G12, G13 (5 inline) |
| 9 | Numeric consistency | PASS | G24; all values via canon() |
| 10 | Reference style (T&F Style V Harvard) | PASS | G05 |
| 11 | OMML | PASS | G14 |
| 12 | Literal asterisk count = 0 | PASS | G15 |
| 13 | Manual line-break count = 0 | PASS | G16 |
| 14 | Stale artifact audit | PASS | G20, G25; package stale-name check |
| 15 | Manuscript anonymity | PASS | G19; IJGIS_FINAL_ANONYMITY_AUDIT_v2.md |
| 16 | Anonymous GitHub content anonymity | PASS | IJGIS_ANON_GITHUB_CONTENT_AUDIT.md |
| 17 | Anonymous GitHub external-view anonymity | PASS | IJGIS_ANON_GITHUB_EXTERNAL_VIEW_AUDIT.md |
| 18 | Fresh-clone reproduction | PASS (quick check; full raw stage not claimed) | IJGIS_ANON_REPO_FRESH_CLONE_REPRODUCTION.md |
| 19 | Preprint policy | PASS (no preprint-server deposit; earlier public repo disclosed) | IJGIS_PREPRINT_POLICY_AUDIT.md |
| 20 | FAIR (review stage) | PASS | IJGIS_OPEN_DATA_FAIR_AUDIT.md; IJGIS_DATA_CODE_AVAILABILITY_PLAN.md |
| 21 | Original repository private | PASS | data/raw/anon_github/06_privacy_recheck.txt |
| 22 | No public author-bearing review artifacts | PASS (Zenodo draft unpublished; snapshot shows no author data) | audits above |
| 23 | ZIP manifest | PASS | make_ijgis_package.py final_v3 verifies every entry's SHA-256 |

Known limitations (unchanged): POI Overpass re-query failed earlier; the full raw-stage pipeline has not been rerun from fresh downloads.
