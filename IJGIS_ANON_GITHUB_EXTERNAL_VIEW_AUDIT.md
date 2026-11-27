# IJGIS — Anonymous GitHub external-view audit

Reviewer URL: https://anonymous.4open.science/r/anonymous-spatial-proxy-review-7E02/
Service: Anonymous GitHub (anonymous.4open.science). Snapshot of private upstream commit a1821d6d4dfb86cd489765b354c7735ccb1aed73.
Snapshot settings (from public `/api/repo/<id>/options`): anonymized 2026-11-11T03:42:34Z; expires 2027-05-11T03:37:47Z; ZIP download enabled; no website; no submodules; no truncated folders. Auto-update: off (author choice; content fixed to the audited commit). Expiry action: remove (author was told not to choose redirect).
Created by the author through the service's GitHub App, with access granted to the single repository `anonymous-spatial-proxy-review` only.
Evidence: data/raw/anon_github/external_view/ (ledger: data/raw/anon_github/acquisition_ledger.jsonl).

## Method
- Headless Chrome, fresh browser context (no cookies, not signed in to GitHub or the service): root page and README page rendered; screenshots, rendered DOM, all links, all images and all network requests recorded.
- curl without cookies against the public file-tree, file, options and ZIP endpoints.
- All 66 served files downloaded one by one and compared with the upstream commit.
- Served ZIP downloaded and compared with the upstream commit; fresh reproduction from the ZIP (see IJGIS_ANON_REPO_FRESH_CLONE_REPRODUCTION.md, section "Reviewer path via the Anonymous GitHub ZIP").

## Results
| Check | Result | Evidence |
|---|---|---|
| Accessible without sign-in | PASS | rendered tree + README (ext_root.png) |
| Owner / organization shown | PASS (none) | rendered DOM: 0 hits `bougtoir`, `github.com/`, avatar URLs |
| Avatar / profile image | PASS (none) | no `<img>` elements; no avatars.githubusercontent.com requests |
| Commit author / e-mail / history | PASS (not exposed) | no history UI; `/commits`, `/branches`, repo-metadata endpoints return 401 `not_connected` |
| Link to upstream or original repository | PASS (none) | ext_links.txt: only service-internal links, service sign-in, and the service maintainer's donation link |
| Author name, institution, ORCID, website | PASS (none) | rendered DOM and all 66 files: 0 hits for Onishi/Tatsuki/bougtoir/shiga-u/biwako/ORCID |
| Manuscript title / journal name | PASS (none) | README gives only a neutral study description |
| Served content == audited upstream commit | PASS | 66/66 files byte-identical (mirror_compare.csv); ZIP 66/66 identical |
| Term replacement did not corrupt data | PASS | identical bytes (terms do not occur in content; standalone "Shiga" deliberately not used) |
| Network requests to third parties | Cloudflare challenge/insights only | ext_links.txt |
| Upstream repository private | PASS | unauthenticated HTML 404; API `private: true` (06_privacy_recheck.txt) |
| Original development repository private | PASS | unauthenticated HTML 404; API `private: true` |

## Residual risks
- The URL slug and the private upstream share the name `anonymous-spatial-proxy-review`. The upstream is private (404), so the name does not lead to the owner. Risk LOW.
- Search/discoverability: the service's robots.txt disallows `/r/`; a DuckDuckGo query for the slug returned no indexed result. Risk LOW.
- The service operator knows the owner's GitHub account (inherent to the service). Not visible to reviewers.
- Deliberately not evaluated: any deanonymization by reviewers from scientific content (study area, data), which is inherent to the paper.

Decision: ANONYMOUS GITHUB EXTERNAL VIEW PASS.
