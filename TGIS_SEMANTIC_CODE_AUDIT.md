# TGIS semantic code audit

Scope: code that turns the frozen analysis into the TGIS documents. Analysis code (download, segments, relocation, ablation, transfer, permutation, figures, `build_canonical_results.py`) is untouched (canonical SHA unchanged; QC gates 1 and 3).

| Code | What it does | Semantic check | Result |
|---|---|---|---|
| `analysis/make_tgis_bib.py` → `tgis_bib.json` | APA 7 bibliography (51 items) | 44 previous IDs and years preserved; 6 TGIS items and 1 repository item added; DOIs checked against Crossref (author + title); Hwang et al. DOI/pages corrected | PASS |
| `analysis/make_tgis_builder.py` | derives `build_manuscript_tgis.py` from frozen `_lit_builder_head.py` + `_lit_body.py` | every edit is an exact-match substitution that fails loudly if the target text is absent or duplicated; edits are limited to citation style, figure/table placement, equation numbering, author block, abstract, keywords, one SDQ framing paragraph, AI sentence in Methods, evidence-level wording (5 levels) and §4.6 heading/paragraph | PASS |
| `cite()` | APA 7 parenthetical citations | `(Author, Year; Author, Year)`, alphabetical within parentheses, '&' for two authors; unknown keys fail loudly | PASS (gates 12–13) |
| `FIGURE()` | records figure name + legend, no embedding | legends listed after tables; files copied byte-identical to `output/tgis_figures/Figure_k.png`; build fails if caption number ≠ position | PASS (gates 14, 16, 26) |
| `TABLES.append(TABLEk)` | defers the frozen table functions until after References | same functions, same canonical inputs; editable copy in `TGIS_TABLES_EDITABLE.docx` | PASS (gates 15, 17) |
| `EQ()` | appends sequential equation numbers | OMML unchanged, numbers (1)–(3) | PASS (gate 20) |
| Abstract | 135 words; all numbers via `canon()` (`AB`, `TF`, `NSEG`, `NOR`) | build fails above 150 words | PASS (gates 7, 32) |
| `_tgis_tail.py` | statements, references, word count, outputs | refuses to build unless `review_access.json` is `public_github`; fails if any bibliography item is uncited; heading styles forced black/Times | PASS (gates 11, 22, 23) |
| `_tgis_cover.py` | cover letter | numbers via canonical helpers; "I/my" only | PASS (gate 4) |
| Evidence-level paragraph (§3.9) | reworded from 4 to 5 levels | Level contents unchanged; Level 1 (computational correctness) and Level 5 (external validation, not available) made explicit as the handoff requires; no numeric change | PASS |

Residual: the five-level hierarchy text in §3.9 is the only place where results are summarized in new words; it was checked against Tables 3–5 (no new value, direction unchanged: prevalence marginally above the null, mean gain below the null).
