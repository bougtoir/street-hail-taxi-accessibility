# Sync security audit (2026-11-27 02:31 UTC)

Workflow `.github/workflows/sync-to-repos.yml`: `BRANCH_MAP["devin/1790678085-street-hail-taxi"]="street-hail-taxi-accessibility"`, `SUBDIR_MAP[...]="street-hail-taxi"`, `EXCLUDE_MAP[...]="data/raw/journal data/raw/zenodo_review"`. In the SUBDIR path the workflow reads `origin/<branch>:street-hail-taxi` into a temporary index, drops `.github/workflows/`, then runs `git rm -rf --cached` for each EXCLUDE_MAP entry before `commit-tree`. Both directories are therefore removed on every automatic sync. The manual syncs used the same exclusion: mirror tree = wip subtree minus these two directories (file-list diff empty).

| Possible re-add | Location in wip | Status |
|---|---|---|
| Zenodo preview token, revocation responses, cookies | data/raw/zenodo_review/** | excluded |
| Publisher page captures (copyright) | data/raw/journal/** | excluded |
| Anonymous-GitHub review captures | data/raw/anon_github/** | synced; scan clean (public review mirror metadata only) |
| GitHub visibility-change API responses | data/raw/github_privacy/** | synced; scan clean (no token; responses do not echo the PAT) |
| Submission-system exports, auth JSON | none in street-hail-taxi | n/a |

Merge check: `git merge-tree` of PR head with current master (15 commits ahead) is clean and keeps this EXCLUDE_MAP line. No extension needed and no scientific data is excluded.

Note: Actions runs in bougtoir/wip were refused for billing on 2026-11-24, so automatic sync depends on that being fixed. The exclusion applies whenever it runs.
