# IJGIS — Anonymous GitHub feasibility (Phase 1)

Date: 2026-11-10. Account available in this session: personal user `bougtoir` (token with `repo` scope). Organizations available: none (`GET /user/orgs` returned `[]`).

| Option | Assessment | Verdict |
|---|---|---|
| A. Public repository under the author's account | The owner handle `bougtoir` appears in the URL, the owner page and the avatar. | **Rejected** |
| B. Neutral organization | None exists. Organizations cannot be created through the API for a personal account (web UI only). Even under an organization, the public repository events API (`/repos/{o}/{r}/events`) shows the `actor` login of whoever created the repository or pushed to it. A public repository therefore leaks the author through metadata outside the file contents. | **Not safe** |
| C. Anonymous GitHub service (anonymous.4open.science, open source, tdurieux/anonymous_github) | An established service for double-anonymous artifact review, widely used in software-engineering and computer-science venues. It proxies a snapshot and hides the owner, organization and repository name, the commit history and authors, and issues. It also replaces configured terms in file contents and names. The upstream repository can stay **PRIVATE**: the service reads it through the owner's GitHub authorization, so reviewers never touch github.com. One human action is required: the author signs in to the service with GitHub (OAuth) and creates the anonymization. This session cannot complete a GitHub OAuth login. | **Feasible (preferred)** |
| D. New "neutral" GitHub account | GitHub Terms of Service: "One person or legal entity may maintain no more than one free Account". A second account created to hide identity would also be a fabricated persona. | **Rejected** |

## Decision
**ANONYMOUS GITHUB FEASIBLE** via option C, with:
- a fresh upstream repository `bougtoir/anonymous-spatial-proxy-review`, kept **PRIVATE**, with fresh history, a neutral commit identity, and issues, wiki and projects disabled;
- the reviewer-facing URL `https://anonymous.4open.science/r/<id>`;
- the author's one-time sign-in to Anonymous GitHub to create the anonymization (term list: Onishi, Tatsuki, bougtoir, Shiga, shiga-u, biwako).

Safeguard: the validated Zenodo private-draft link stays the fallback. It is replaced in the manuscript only after the Anonymous GitHub URL passes the logged-out external-view audit (Phase 7). If the service cannot read a private upstream, the upstream is **not** made public: a public upstream under `bougtoir` would be found by exact-string search on github.com. The Zenodo route is then retained.
