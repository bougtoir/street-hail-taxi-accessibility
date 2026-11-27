# IJGIS — GitHub repository privacy action

| Field | Value |
|---|---|
| Repository | https://github.com/bougtoir/street-hail-taxi-accessibility |
| Old visibility | PUBLIC (`data/raw/github_privacy/before.json`) |
| New visibility | **PRIVATE** (`data/raw/github_privacy/after.json`: `"private": true, "visibility": "private"`) |
| Change made by | the author, in the GitHub web UI (Settings → General → Danger Zone → Change repository visibility) |
| Change timestamp (GitHub `updated_at`) | 2026-11-10T12:22:23Z |
| Verified at | 2026-11-10T12:22:50Z |
| Purpose | temporary privacy for the duration of IJGIS double-anonymous review; it is not historical erasure |

The session's own API token was refused the visibility change (HTTP 403, "Resource not accessible by integration"; `patch_response.json`). The author therefore made the change himself. A first attempt did not complete, because the confirmation dialog was not finished and the API still reported `public`. The second attempt succeeded.

## Verification (Phase 6)
| Check | Result |
|---|---|
| Repository metadata (authenticated API) | `private: true`, `visibility: private` |
| Unauthenticated repository page | HTTP 404 |
| Unauthenticated raw file (`main/README.md`) | HTTP 404 |
| Unauthenticated `git ls-remote` | denied |
| Branches after change | `["main"]`, unchanged |
| `main` head after change | `0dc2baddfc16c8aa4127ff5ae6ccf7f8b52a5982`, unchanged; no history rewrite |
| Repository name, default branch, tags, code | unchanged (name and URL unchanged; default branch `main`; no tags existed; no files removed) |
| Stars, forks, watchers lost | none (all were 0 before the change) |
| Working clone (`bougtoir/wip`) and PR #803 | unaffected; PR #803 lives in `bougtoir/wip`, a separate private repository |

Not done: no history rewrite, no branch or tag deletion, no code removal, no rename, no default-branch change.
Residual: copies of the repository fetched or cached by third parties while it was public cannot be recalled (see IJGIS_PREPRINT_POLICY_AUDIT.md).
After acceptance: return to PUBLIC (IJGIS_DATA_CODE_AVAILABILITY_PLAN.md §B).
