# IJGIS — private review-link audit (Figshare requested → Zenodo private draft used)

## Why the platform changed
The author has no Figshare account (author statement, 2026-11-10), and the session could not create one or log in on the author's behalf. The author asked whether Anonymous GitHub could be used instead. Two things ruled it out:
- Anonymous GitHub needs an interactive GitHub OAuth login.
- Its source would be the public mirror, which holds earlier, author-named manuscript files.

The author's existing Zenodo account was reachable through its API token, so a private **unpublished draft** was used instead. IJGIS/T&F accepts data and code shared with reviewers through a private or anonymous link; the platform is not prescribed (IJGIS_CURRENT_REQUIREMENTS.md).

## Item
| Field | Value |
|---|---|
| Platform | Zenodo (InvenioRDM), unpublished draft |
| Private item (draft record) ID | 24106479 |
| Title | Anonymous review materials for IJGIS manuscript |
| Creators shown | "Anonymous (double-anonymous peer review)" (organizational) |
| Description | Anonymized code, derived data, machine-readable outputs, and reproducibility materials supplied for double-anonymized peer review. |
| File | IJGIS_ANON_REVIEW_REPRO_BUNDLE.zip, 33,633,079 bytes, md5 75b881a6…, SHA-256 813a334f…28791 (identical to the local bundle) |
| Published? | **No** (status `draft`; never submitted to the publish action) |
| DOI | **None reserved or minted** (the `reserve_doi` action was not called) |
| Access link | id 4799cc33-389d-411f-9403-f47959bc7c0a, permission `preview`, no expiry, created 2026-11-10T11:34:51Z |
| Link in manuscript | direct file download: `https://zenodo.org/records/24106479/files/IJGIS_ANON_REVIEW_REPRO_BUNDLE.zip?download=1&preview=1&token=…` (full URL in `analysis/review_access.json`) |

Raw API responses are kept in `data/raw/zenodo_review/` (01–07). The API token itself is not stored.

## Verification (unauthenticated, fresh client, no cookies)
| Test | Result |
|---|---|
| Draft URL without token | HTTP 404, so the item is not publicly visible |
| Landing page with token | HTTP 200 |
| Direct download with token | HTTP 200, `content-disposition: attachment`; downloaded SHA-256 equals the local bundle |
| Account or login needed by recipient | No |
| Download response headers | no owner, creator or account fields |
| Rendered landing page (headless Chrome DOM text) | shows only "Anonymous (double-anonymous peer review)"; no author name, affiliation or username |
| Landing page HTML source (embedded JSON) | **contains the account owner's profile** (`full_name`, `affiliations`, `username`) inside the record's `parent.access.owned_by` block |

## Identity exposure and mitigation
- The **visible** landing page does not show the author's identity. Its **HTML source** does: Zenodo embeds the draft owner's profile in that page. This is how Zenodo works and cannot be configured per record.
- Mitigation: the blinded manuscript gives only the **direct file-download URL**. That URL returns the anonymized ZIP and nothing else, with no HTML page and no owner metadata.
- Residual risk (LOW): a reviewer who deliberately rewrites the URL to open the landing page and then reads the page source would see the owner. Doing so requires an intentional de-anonymization step.

## Verdict
The private review access is usable, requires no recipient account, and keeps the item unpublished with no DOI. The link given to reviewers does not expose the author's identity. The deliberate-URL-edit residual risk is disclosed above.

## Status update 2026-11-11: SUPERSEDED
The Zenodo draft link is superseded by the Anonymous GitHub snapshot (IJGIS_ANON_GITHUB_EXTERNAL_VIEW_AUDIT.md) and has been removed from the blinded manuscript, title page and cover letter. The draft stays unpublished (no DOI) as a fallback; the evidence in data/raw/zenodo_review/ is retained. Known defect if the fallback were ever used: that bundle lacks DATA_SOURCE_AUDIT.md and data/processed/ceus_rerun.log, so its quick check would fail; it would need re-upload first.
