# TGIS public repository audit

Review model: single-blind (TGIS author guideline, Wayback 2022-03-08) → author-identified public repository; the anonymous review repository (bougtoir/anonymous-spatial-proxy-review) is not cited and not part of the package.

Repository: https://github.com/bougtoir/street-hail-taxi-accessibility (topic name, no journal name). Cited as Onishi (2026) in the manuscript and DAS. `analysis/review_access.json`: mode public_github.

## Actions (2026-11-24 UTC)

1. Visibility changed private → public (GitHub API PATCH by owner token; response visibility=public).
2. Sync: the wip sync workflow could not run (GitHub Actions jobs refused: "recent account payments have failed or your spending limit needs to be increased"). The same operation the workflow performs was done manually: tree of `street-hail-taxi/` at wip branch devin/1795503313-tgis (also pushed to the mapped sync branch devin/1790678085-street-hail-taxi), committed by wip-sync on top of the previous mirror head and pushed to main. `data/raw/journal/` (publisher page captures) excluded from the public tree.

## Logged-out checks (2026-11-24T07:19:44Z)

| URL | HTTP |
|---|---|
| https://github.com/bougtoir/street-hail-taxi-accessibility | 200 |
| https://raw.githubusercontent.com/bougtoir/street-hail-taxi-accessibility/main/README.md | 200 |
| https://raw.githubusercontent.com/bougtoir/street-hail-taxi-accessibility/main/analysis/canonical_results.json | 200 |
| https://raw.githubusercontent.com/bougtoir/street-hail-taxi-accessibility/main/analysis/build_manuscript_tgis.py | 200 |
| https://raw.githubusercontent.com/bougtoir/street-hail-taxi-accessibility/main/MANIFEST.csv | 200 |
| raw canonical_results.json SHA-256 | ee1ce5bb26df5605aec7b803c459056b525de133b7f1d9bf8e81d448e33a22ac (= frozen) |
| data/raw/journal/ | 404 (excluded) |
| anonymous git clone (no credentials, no git config) | success; see TGIS_CLEAN_CLONE_REPRODUCTION.md |

## Content check

- README author-identified (name, affiliation, ORCID), install, one-command check, full pipeline, limitations; LICENSE (MIT code; CC BY 4.0 derived data/figures; ODbL/MLIT third-party terms); requirements.txt pinned; MANIFEST.csv (93 files, SHA-256).
- Credentials: a content scan (Devin Review, 2026-11-24) found the unpublished Zenodo draft preview access link (`data/raw/zenodo_review/04_access_link.json`, plus expired Zenodo session cookies in `cj.txt`) in the first public sync. Removed from the mirror tree in a follow-up sync commit (raw URL 404); `data/raw/zenodo_review` and `data/raw/journal` are now in the sync workflow's `EXCLUDE_MAP` for `devin/1790678085-street-hail-taxi`. The two earlier mirror commits still contain the file. The preview link was revoked at Zenodo on 2026-11-27 and verified unusable, so the historical copies are a dead credential and no history rewrite is needed (TGIS_ZENODO_PREVIEW_REVOCATION_AUDIT.md, TGIS_GIT_HISTORY_PURGE_DECISION.md). The originals stay in the private wip repository (raw data are not deleted). No other token value is tracked (exact-value scan of all tracked files).
- Residual: the repository also holds historical documents from earlier target-journal preparations and pipeline scripts with historical names (e.g. `run_ceus_analyses.py`). Not a TGIS policy issue under single-blind review; renaming frozen scripts would break provenance, so they are kept.
- Persistence: GitHub is not a DOI archive; a Zenodo release can be minted at acceptance without changing contents.

Verdict: PASS (public, reachable without login, registry SHA matches, TGIS builder present, clean clone reproduces).
