# FINAL QC REPORT

| # | Check | Result |
|---|-------|--------|
| 1 | Analysis-derived numbers sourced from canonical registry | PASS (canon() fail-loud; registry generated from committed tables/npz) |
| 2 | 43% vs 44% consistency | PASS (43% everywhere; single rounding rule) |
| 3 | Clean public-repo reproduction | PASS (clean clone regenerates identical canonical JSON + prose) |
| 4 | perm_null_arrays.npz present + provenance | PASS (committed, 12 arrays loadable, documented) |
| 5 | Public repo URL/contents verifiable | PASS (repo live; URL in Declarations + cover letter) |
| 6 | Figures numbered in first-citation order | PASS (renumber_figures_qc.py; F1 framework -> F9 heterogeneity) |
| 7 | All figures/tables cited | PASS (matrix: every item has text citation) |
| 8 | Math as OMML | PASS (10 oMath elements; zero plain-text math) |
| 9 | Literal asterisks | PASS (0) |
| 10 | Stale Figure 1 terminology | PASS (regenerated; stress-test wording only) |
| 11 | Corrupted sentence repaired | PASS + corruption scan clean |
| 12 | Reference existence | PASS (10/10 verified via Crossref/HTTP) |
| 13 | Citation-bibliography 1:1 | PASS (matrix: no bibliography-only or citation-only refs) |
| 14 | Reference order = first appearance | PASS (numbered Vancouver, cite() order) |
| 15 | Line breaks | PASS (0 explicit w:br) |
| 16 | Prose corruption scan | PASS (no artifacts beyond OMML extraction false positives) |
| 17 | Style (TNR 12pt, captions 10pt, no markdown/paths) | PASS |
| 18 | Figure/table content vs canonical values | PASS (tables generated from canon; spot-checked) |
| 19 | Traceability map zero mismatches | PASS (NUMERICAL_PROVENANCE_MAP.csv) |
| 20 | Scientific content unchanged | PASS (values identical to frozen PRE_QC_FREEZE set) |

Overall: 20/20 PASS.
