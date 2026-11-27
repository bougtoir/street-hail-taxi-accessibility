# Public-mirror history purge decision (2026-11-27 02:31 UTC)

| Condition | Evidence | Met |
|---|---|---|
| Old preview URL unusable | TGIS_ZENODO_PREVIEW_REVOCATION_AUDIT.md: link deleted (204), links total 0, page 404, download serves only the login page, incognito "Draft not found" | yes |
| No other live secret | TGIS_PUBLIC_MIRROR_SECRET_SCAN.md: no live secret; the `cj.txt` session cookies in the same historical commits expired 2026-11-15/17 and belonged to a session that has ended | yes |
| Current tree clean | mirror main has no zenodo_review, no token value | yes |
| Recurrence prevented | EXCLUDE_MAP for the sync branch; TGIS_SYNC_SECURITY_AUDIT.md | yes |

Affected historical commits: 30cb0d6, a1c9f3d (path `data/raw/zenodo_review/04_access_link.json`, plus `cj.txt` and the ledger/HTML captures containing the same token). They now hold only a dead credential.

**HISTORY PURGE NOT REQUIRED**

No force-push was made; mirror history and provenance are preserved.
