# IJGIS anonymity risk audit (double-anonymous review)

Date: 2026-11-10. Policy: IJGIS is double-anonymous; figures/tables are inserted in the main document "to facilitate double anonymous peer reviews".

## 1. Blinded manuscript (`IJGIS_MAIN_MANUSCRIPT_BLINDED.docx` / `.pdf`)

Checked by `analysis/qc_ijgis.py` gate G19, plus manual inspection.

| Item | Status |
|---|---|
| Author name, affiliation, correspondence, ORCID | absent |
| Repository URL / GitHub handle | absent (replaced by Figshare private-link placeholder) |
| Acknowledgements | none in blinded file |
| Funding | "no external funding" (non-identifying) |
| Self-citation in first person | none (no prior publication by the author is cited) |
| DOCX core properties (creator, lastModifiedBy, title, comments) | blank |
| Comments / tracked changes (`w:ins`, `w:del`) / headers / footers | none |
| Internal paths (`/home/...`) | none |
| PDF metadata Author | none (LibreOffice export, no Author field) |
| AI statement | names the tool vendor (Cognition AI), not the author |

Result: the blinded files contain no direct identifiers. PASS.

## 2. Title page / cover letter

`IJGIS_TITLE_PAGE.docx` and `IJGIS_COVER_LETTER.docx` carry the author name, the public GitHub URL and placeholders for affiliation, institutional email and ORCID. They are uploaded as "not for review" files and are not part of the reviewer PDF.

## 3. Indirect identification risk (not removable by blinding)

| Risk | Evidence | Severity |
|---|---|---|
| Public mirror with earlier manuscripts | `bougtoir/street-hail-taxi-accessibility` (public) contains `output/CEUS_*MAIN_MANUSCRIPT*.docx/pdf`, cover letters and handoff files naming the author, from the earlier CEUS submission. The earlier title ("Stress-testing public-data urban accessibility proxies: street-hail taxi relocation without fleet telemetry") and the same study are searchable. | HIGH |
| Public git history | Even if those files are removed from the current tree, they remain in public commit history. History has NOT been rewritten (rewriting would not undo forks/caches and the handoff forbids simulating anonymity). | HIGH (residual) |
| Repository name / account | Repository name is topic-only (no journal name), but the account handle links to the author. | MEDIUM |
| Distinctive study design | A reviewer who searches the topic may find the public repository. | MEDIUM |

## 4. Actions taken

- The new IJGIS title, blinded manuscript, builders that contain the author name, and the IJGIS cover letter are NOT pushed to the public mirror or to the sync branch (`devin/1790678085-street-hail-taxi`), so the new submission is not linked publicly to the author during review.
- An anonymized reproduction bundle (`IJGIS_ANON_REVIEW_REPRO_BUNDLE.zip`) is built from the analysis pipeline only and scanned for identifying strings (`analysis/make_ijgis_package.py`).
- The cover letter discloses the public repository and its earlier manuscript files to the Editor.

## 5. Author actions

1. Decide whether to remove the earlier manuscript/submission files from the current public tree (history would still contain them) or to make the repository private during review. Either is the author's decision; neither makes anonymity perfect.
2. Upload the anonymized bundle to Figshare as a private item and paste the private link into the Data and codes availability statement.

Conclusion: blinded files PASS; overall anonymity is NOT perfect because of the public repository history. This is disclosed, not hidden.

## Update (2026-11-10): public-mirror risk mitigated
The mirror is now PRIVATE (IJGIS_GITHUB_PRIVACY_ACTION.md). Reviewers receive only an anonymized Zenodo private-draft download link (IJGIS_FIGSHARE_PRIVATE_LINK_AUDIT.md). The public-mirror residual risk falls from HIGH to LOW–MEDIUM (caches or clones from the earlier public period). The final regression is in IJGIS_FINAL_ANONYMITY_AUDIT.md.
