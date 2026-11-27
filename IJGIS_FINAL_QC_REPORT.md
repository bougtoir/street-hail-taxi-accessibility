# IJGIS final QC report

Automated gates: `python3 analysis/qc_ijgis.py` -> `output/IJGIS_QC_RESULTS.json`. Result: 25/25 PASS.

| Gate | Status |
|---|---|
| G01 canonical_results.json unchanged vs pre-IJGIS freeze | PASS |
| G02 no hard-coded canonical result literals in _lit_body.py | PASS |
| G03 build_manuscript_ijgis.py == head+body | PASS |
| G04 reference count == bibliography size (all cited) | PASS |
| G05 references alphabetical (T&F Style V Harvard) | PASS |
| G06 every DOI has an archived Crossref record | PASS |
| G07 every author-year citation resolves to bibliography | PASS |
| G08 every bibliography item cited in text | PASS |
| G09 all figures cited | PASS |
| G10 figure first-citation order sequential | PASS |
| G11 all tables cited | PASS |
| G12 table first-citation order sequential | PASS |
| G13 figures and tables embedded inline | PASS |
| G14 OMML equations present | PASS |
| G15 no literal asterisks | PASS |
| G16 no manual line breaks | PASS |
| G17 language lock (banned phrases absent in all documents) | PASS |
| G18 claim calibration (no external/operational validity claims) | PASS |
| G19 blinded manuscript free of identity/paths/metadata/comments/tracked changes | PASS |
| G20 no stale target-journal wording (CEUS) in IJGIS documents | PASS |
| G21 main text within IJGIS typical 5,000-8,000 words | PASS |
| G22 abstract <= 200 words, 2-5 keywords, title present | PASS |
| G23 IJGIS required statements present | PASS |
| G24 cover-letter numbers identical to manuscript numbers | PASS |
| G25 PDF regenerated from current DOCX, title present, no author metadata | PASS |

## Additional gates (scripted or manual)

| Gate | Status |
|---|---|
| X01 Clean-copy reproduction: build_canonical_results.py regenerates canonical_results.json byte-identical (SHA-256 ee1ce5bb26df...) and builder reproduces identical manuscript text | PASS |
| X02 Raw re-acquisition (cache-served Overpass): walk graph 182,538 edges / 60,804 nodes == canonical; N02 zip re-downloaded; POI re-query FAILED (Overpass connection refused) — stored in data/raw/source_redownload_20261110/ (local, git-ignored) with SHA256SUMS.txt | PARTIAL |
| X03 Anonymized review bundle: 61 files == manifest, identity-string scan clean (make_ijgis_package.py) | PASS |
| X04 Submission ZIP == manifest, no stale CEUS/superseded files (make_ijgis_package.py) | PASS |
| X05 Hostile review (14 objections) completed: HOSTILE_REVIEW_IJGIS_FINAL.md | PASS |
| X06 IJGIS requirements table: IJGIS_CURRENT_REQUIREMENTS.md (abstract/keyword limits from non-official summaries — author check) | PASS* |
| X07 Repository anonymity (public mirror history contains earlier identified manuscripts) | RISK — author decision |
| X08 Preprint policy (no preprint-server copy; public GitHub copies of earlier version) | RISK — disclosed |
| X09 Open Data + FAIR (Figshare private link / DOI / licence confirmation pending) | CONDITIONAL — author action |

## Manuscript statistics

Title (130 characters): Optimization gain is not proxy validity: internal stress tests for constructed spatial opportunity surfaces without outcome labels
Main text 5,418 words (Introduction to Conclusion, excluding abstract, captions, tables, statements, references); abstract 169 words; 5 keywords; 44 references (T&F Reference Style V, Harvard); 9 figures and 5 tables inline.

## Defect found and fixed

The CEUS-era builder printed the literal text "{NWE}-edge" in section 2.3 (missing f-string prefix). The IJGIS build prints the canonical walk-edge count. No numerical result changed.

## Scientific freeze

`analysis/canonical_results.json`, `tables/`, `figures/` byte-identical to the pre-IJGIS freeze (G01; PRE_IJGIS_FREEZE.md). No new data, analysis or result.
