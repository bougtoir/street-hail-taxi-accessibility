# IJGIS — Final QC report v2

Automated QC (`analysis/qc_ijgis.py`): **25/25 PASS** (output/IJGIS_QC_RESULTS.json), run after the final regeneration of DOCX, PDF, title page and cover letter.

| # | Required gate | Result | Evidence |
|---|---|---|---|
| 1 | Scientific analysis unchanged | PASS | no script under analysis/ that produces results was modified; only manuscript builder and packaging changed |
| 2 | Canonical registry unchanged | PASS | canonical_results.json SHA-256 ee1ce5bb…a22ac (frozen value) |
| 3 | Reference existence | PASS | Crossref-verified (data/raw/crossref_ijgis) |
| 4 | All references cited | PASS | QC gate |
| 5 | All citations resolved | PASS | QC gate (fail-loud `cite()`) |
| 6 | All figures cited | PASS | QC gate (9/9) |
| 7 | All tables cited | PASS | QC gate (5/5) |
| 8 | Numeric consistency | PASS | all numbers via `canon()`; QC gate |
| 9 | Figure/table numbering | PASS | QC gate |
| 10 | Reference style (T&F Style V Harvard) | PASS | QC gate |
| 11 | OMML equations | PASS | QC gate |
| 12 | Literal asterisk count = 0 | PASS | QC gate |
| 13 | Manual line-break count = 0 | PASS | QC gate |
| 14 | No stale artifacts | PASS | QC G25 (PDF newer than DOCX) plus package stale-check |
| 15 | Double anonymity | PASS (residuals disclosed) | IJGIS_FINAL_ANONYMITY_AUDIT.md |
| 16 | Private review access | PASS (**Zenodo private draft instead of Figshare**: author has no Figshare account) | IJGIS_FIGSHARE_PRIVATE_LINK_AUDIT.md; unauthenticated download SHA-256 matches; record without token returns 404; unpublished, no DOI |
| 17 | GitHub repository private | PASS | IJGIS_GITHUB_PRIVACY_ACTION.md (API private; unauthenticated 404) |
| 18 | Preprint-policy risk reassessed | PASS | IJGIS_PREPRINT_POLICY_AUDIT.md (recheck section) |
| 19 | Open Data + FAIR review-stage compliance | PASS | IJGIS_OPEN_DATA_FAIR_AUDIT.md, IJGIS_DATA_CODE_AVAILABILITY_PLAN.md |
| 20 | Blinded manuscript has no public author-identifying URL | PASS | anonymity audit (0 hits for github.com / name / ORCID) |
| 21 | Title page has correct author metadata | PASS (taken from the author's existing author block; author asked for "the appropriate choice") | analysis/author_meta.json |
| 22 | Final ZIP manifest matches contents | PASS | make_ijgis_package.py verifies every entry's SHA-256 against its MANIFEST |

Known limitations (unchanged and disclosed): partial raw re-acquisition (POI Overpass re-query refused); official IJGIS instructions page partly behind Cloudflare.
