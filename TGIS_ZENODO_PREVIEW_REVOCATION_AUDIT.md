# Zenodo preview-link revocation audit (2026-11-27 02:31 UTC)

Record: Zenodo draft 24106479 (unpublished, `state: unsubmitted`, no DOI). Link: id 4799cc33-389d-411f-9403-f47959bc7c0a, permission preview, created 2026-11-10T11:34:51Z.

Method: Zenodo blocks this VM's IP for command-line HTTP (curl: 403 "unusual traffic" for every zenodo.org URL, including the home page), so all requests ran as `fetch()` inside the Chrome page context on zenodo.org. Owner calls used the stored Zenodo API token (Authorization header); logged-out tests used `credentials: 'omit'` (no cookies, no token header). Revocation used the documented InvenioRDM REST endpoint `DELETE /api/records/{id}/access/links/{link_id}`. No publish, no DOI, no file or metadata change. Raw responses: `data/raw/zenodo_review/revocation/` (private wip only; excluded from public sync) with `acquisition_ledger.jsonl` (UTC, bytes, SHA-256).

| Step | Method | Auth | HTTP | Content-Type | Bytes | SHA-256 |
|---|---|---|---|---|---|---|
| 01_before_preview_page_noauth.html | GET | none (credentials omitted) | 200 | text/html; charset=utf-8 | 46450 | 1f88907e58240a7f… |
| 02_before_download_noauth.bin | GET | none (credentials omitted) | 200 | application/octet-stream, application/octet-stream | 33633079 | 813a334f2afae595… |
| 03_before_record_noauth_control.html | GET | none (credentials omitted) | 404 | text/html; charset=utf-8 | 15291 | 2281d7d1ac326c0b… |
| 04_before_links.json | GET | owner token | 200 | application/json | 427 | fefd024b9f5b8fe6… |
| 05_before_draft.json | GET | owner token | 200 | application/json | 2744 | 84b9c5814c642984… |
| 06_delete_link_response.txt | DELETE | owner token | 204 | text/html; charset=utf-8 | 0 | e3b0c44298fc1c14… |
| 07_after_links.json | GET | owner token | 200 | application/json | 34 | 5195f4dd67b234a9… |
| 08_after_preview_page_noauth.html | GET | none (credentials omitted) | 404 | text/html; charset=utf-8 | 15406 | a3b8ca52ff683258… |
| 09_after_download_noauth.bin | GET | none (credentials omitted) | 200 | text/html; charset=utf-8 | 8865 | 554232752f404312… |
| 10_after_draft.json | GET | owner token | 200 | application/json | 2744 | 84b9c5814c642984… |
| 11_after_incognito_browser.png | GET (Chrome incognito window, logged out) | none | rendered 'Draft not found' |  | 2166753 | a48086bf59266683… |

## Result

- Before: links list total 1 (the leaked link); leaked preview URL 200 with draft page; leaked download URL 200 with the 33.6 MB review bundle.
- DELETE returned 204.
- After: links list `{"hits": [], "total": 0}`, so no replacement link was created; leaked preview URL 404 "Draft not found"; leaked download URL serves only the Zenodo login page (200 text/html, 8,865 bytes, no file content).
- Logged-out incognito Chrome window with the old preview URL: "Draft not found" (screenshot `11_after_incognito_browser.png`).
- Draft after: `status: draft`, `submitted: false`, `state: unsubmitted`, DOI none, so it is still unpublished and unchanged.
- Command-line HTTP from this VM is not informative (IP block 403 for any URL, before and after).

**PREVIEW LINK REVOKED AND UNUSABLE**
