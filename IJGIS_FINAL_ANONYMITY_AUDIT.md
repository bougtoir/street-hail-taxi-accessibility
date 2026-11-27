# IJGIS — Final anonymity audit (double-anonymous review)

Date: 2026-11-10. Scan pattern (case-insensitive): onishi, tatsuki, shiga, biwako, bougtoir, orcid, 0000-0001-7261, gmail, github.com, street-hail-taxi-accessibility, pull/803, devin.ai/sessions, /home/ubuntu.

| Item | Scope | Result |
|---|---|---|
| Blinded DOCX `IJGIS_MAIN_MANUSCRIPT_BLINDED_FINAL.docx` | every XML/rels part (body, headers, footers, footnotes, core/app properties) | 0 hits |
| DOCX comments / tracked changes | `word/comments.xml`, `<w:ins>`, `<w:del>` | none / 0 / 0 |
| DOCX properties | core.xml creator/lastModifiedBy; app.xml Company | empty (revision 1, default timestamps only) |
| DOCX embedded figures (9) | PNG text chunks | only `Software: Matplotlib`; no author or path |
| Blinded PDF `IJGIS_MAIN_MANUSCRIPT_BLINDED_FINAL.pdf` | full text plus pdfinfo | 0 hits; no Author/Title metadata (Creator Writer, Producer LibreOffice) |
| Anonymized bundle `IJGIS_ANON_REVIEW_REPRO_BUNDLE.zip` (61 entries) | file names and contents (cache/ excluded only for third-party OSM contacts; see the pre-upload audit) | 0 hits; no .git, no .pyc; empty ZIP comment |
| Manuscript availability statement | review link | Zenodo **direct file download** URL only; no GitHub URL, name, institution, ORCID or e-mail |
| Self-citation | reference list | no self-citations; nothing to anonymize |
| Acknowledgements / funding / AI statement | blinded manuscript | anonymized ("withheld for review") or non-identifying |
| Title page / cover letter | non-blinded, uploaded separately | carry author metadata by design (IJGIS requires them) |

## Residual risks (disclosed, not hidden)
1. **Zenodo landing page HTML source.** If a reviewer deliberately removes the `/files/...` part of the link and opens the record page, the page source contains the deposit owner's profile. The rendered page shows "Anonymous". Risk: LOW (deliberate action required). Details: IJGIS_FIGSHARE_PRIVATE_LINK_AUDIT.md.
2. **Earlier public repository.** The repository was public until 2026-11-10 and is now PRIVATE (IJGIS_GITHUB_PRIVACY_ACTION.md). Caches or clones from the earlier public period may persist. Risk: LOW–MEDIUM. Disclosed to the Editor in the cover letter.
3. **Topic searchability.** A reviewer could search for the topic or title (ordinary for double-anonymous review). There is no active public preprint.

Verdict: **PASS** for double-anonymous review, with residuals 1–2 disclosed. Perfect anonymity is not claimed.
