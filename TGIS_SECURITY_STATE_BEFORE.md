# TGIS security state before revocation (verified 2026-11-27 02:31 UTC)

| Check | Result |
|---|---|
| Public mirror bougtoir/street-hail-taxi-accessibility visibility | public (GitHub API) |
| Default branch | main; head 051ae248345c41da3e26e547662c0395f21573d1 |
| `data/raw/zenodo_review/04_access_link.json` in current tree | absent (raw URL 404) |
| Sync workflow exclusion | `EXCLUDE_MAP["devin/1790678085-street-hail-taxi"]="data/raw/journal data/raw/zenodo_review"` (applied in the SUBDIR path via `git rm --cached` on the temp index) |
| Mirror commits containing the file | 30cb0d6, a1c9f3d (public since 2026-11-24); removed in d01efcf |
| Leaked credential | Zenodo InvenioRDM preview link token (HS512 JWT, 240 chars; payload id 4799cc33-389d-411f-9403-f47959bc7c0a, no expiry claim) and Zenodo session cookies in `cj.txt` (expired 2026-11-15/17) |
| Baseline test of leaked URL before revocation | LIVE: preview page HTTP 200 (draft title rendered); file download HTTP 200, 33,633,079-byte ZIP, SHA-256 813a334f… = archived review bundle |

## Current-tree search (git grep on mirror main 051ae24)

| Pattern | Files | Classification |
|---|---|---|
| `token=` / `preview=1` | IJGIS_FIGSHARE_PRIVATE_LINK_AUDIT.md | harmless: URL truncated before the token value (`token=…`) |
| `access_link_id`, `4799cc33-…` | analysis/review_access.json, IJGIS_FIGSHARE_PRIVATE_LINK_AUDIT.md | harmless: link identifier, not the bearer token; useless without the signed JWT |
| `zenodo_review`, `cj.txt` | audit/handoff text, review_access.json | harmless: path names in audit prose |
| `csrftoken`, `sessionid`, exact token value | none | — |

Verdict before revocation: current tree clean; historical commits hold a LIVE credential → revocation required.
