# IJGIS — Final anonymity audit v2 (Anonymous GitHub architecture, 2026-11-11)

Architecture: original development repository PRIVATE + separate private upstream (one fresh root commit, neutral metadata) + public Anonymous GitHub snapshot https://anonymous.4open.science/r/anonymous-spatial-proxy-review-7E02/ + blinded manuscript containing only that URL + non-blinded title page with author metadata.

| Item | Result | Evidence |
|---|---|---|
| Blinded manuscript text/tables: name, handle, institution, ORCID, e-mail, github, paths | PASS (0 hits) | QC G19 |
| Blinded manuscript DOCX metadata (dc:creator, lastModifiedBy), comments, tracked changes | PASS (empty / none) | QC G19; docProps/core.xml |
| Blinded PDF metadata | PASS (no Author field; Creator Writer / LibreOffice) | pdfinfo; QC G25 |
| Only review URL in blinded manuscript | PASS: https://anonymous.4open.science/r/anonymous-spatial-proxy-review-7E02/ | all other URLs are reference DOIs and data-source sites |
| Zenodo link removed from manuscript, title page, cover letter (DOCX and PDF) | PASS (0 hits) | text extraction |
| Title page: author metadata present (non-blinded, not for review) | PASS | analysis/author_meta.json |
| Cover letter disclosure (previously public, made private, no preprint, separate anonymous repository) | PASS | cover letter text |
| Anonymous repository content | PASS | IJGIS_ANON_GITHUB_CONTENT_AUDIT.md |
| Anonymous repository git metadata | PASS (Review Materials / review@example.invalid; no parents; no fork) | IJGIS_ANON_GIT_METADATA_AUDIT.md |
| Reviewer-side external view (logged out) | PASS | IJGIS_ANON_GITHUB_EXTERNAL_VIEW_AUDIT.md |
| Original repository private | PASS (API private; unauthenticated 404; 2026-11-11T03:48:38Z) | data/raw/anon_github/06_privacy_recheck.txt |
| Upstream of snapshot private | PASS (same check) | same |

## Residual risks (not claimed to be zero)
- Earlier public period of the development repository: caches/third-party clones cannot be removed. Disclosed in the cover letter. LOW–MODERATE.
- Search/discoverability of the review snapshot: robots.txt disallows /r/; no indexed hit for the slug. LOW.
- Study area and data could hint at a Japan-based author; inherent to the science. LOW.
- Zenodo landing-page owner exposure: no longer relevant to reviewers (link removed); draft remains unpublished.

Decision: ANONYMITY PASS (residuals disclosed).
