# IJGIS — Anonymous review repository: git metadata audit (Phase 5)

| Field | Value |
|---|---|
| Upstream repository | `bougtoir/anonymous-spatial-proxy-review`: **PRIVATE**; never shown to reviewers (they see only the Anonymous GitHub proxy URL) |
| Root commit SHA | `a1821d6d4dfb86cd489765b354c7735ccb1aed73` (the only commit; `parents=[]`) |
| Commit author display | `Review Materials` |
| Commit author e-mail | `review@example.invalid` (RFC 2606 reserved domain; impersonates no real person) |
| Committer | same as author |
| GitHub-linked author/committer login | `null` / `null` (the e-mail is not linked to any account) |
| Signature | none (`verified: false`) |
| Commit message | "Reproducibility materials for double-anonymized peer review" |
| Branch | `main` (only branch) |
| Tags | none |
| Remote URL (fresh clone) | `https://github.com/bougtoir/anonymous-spatial-proxy-review.git`. The owner handle appears here only, in the private upstream, and is replaced by the Anonymous GitHub proxy |
| Original ancestry | **none**: content was unpacked from the anonymized ZIP into an empty directory, then `git init`. Not a fork (`fork: false`, `parent: null`), no mirror clone, no `.git` copied; `git rev-list --all --count` = 1 |
| Repository settings | issues, wiki, projects and discussions disabled; no topics; no description or homepage; Actions runs = 0 |
| Identity method | per-command environment variables (`GIT_AUTHOR_*`, `GIT_COMMITTER_*`); no git config was modified |

Evidence: `data/raw/anon_github/01_repo_meta.json`, `02_commits.json`, `05_unauth_checks.txt` (unauthenticated HTML 404, API 403/404).
