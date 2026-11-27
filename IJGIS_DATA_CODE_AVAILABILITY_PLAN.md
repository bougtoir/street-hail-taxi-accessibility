# IJGIS — data and code availability plan

## A. During review (current state)
| Element | State |
|---|---|
| GitHub repository `bougtoir/street-hail-taxi-accessibility` | to be **PRIVATE** for the duration of IJGIS review (see IJGIS_GITHUB_PRIVACY_ACTION.md for the verified state) |
| Reviewer access | anonymized bundle `IJGIS_ANON_REVIEW_REPRO_BUNDLE.zip` (SHA-256 813a334f…28791) through a private, unpublished Zenodo draft (record 24106479) with a `preview` access link. The direct-download URL needs no account and is given in the blinded manuscript |
| Blinded manuscript | gives only the anonymized private review link. No GitHub URL, author name, institution, ORCID or e-mail |
| Title page (not sent to reviewers) | author metadata, the GitHub URL with its review-period private status, and the private review link |
| DOI | **none**. No DOI is reserved or minted, and none is claimed |

## B. After acceptance
1. Return the GitHub repository to PUBLIC (Settings → Danger Zone → Change visibility). History is preserved, so this needs no history rewrite.
2. Optionally publish a de-anonymized archival deposit (a new Zenodo version or record with real creators) to obtain a DOI. Only after that DOI exists, cite it in the accepted manuscript's Data and codes availability statement together with the GitHub URL.
3. Licences for the public release: code MIT, derived tables CC BY 4.0 (author to confirm). Third-party inputs remain under their own terms (OSM ODbL; MLIT National Land Numerical Information terms).
4. The review draft (record 24106479) can then be deleted, or kept unpublished. It must not be published with the "Anonymous" creator in the long run.

## C. Constraints honoured
- The manuscript never calls the private review link a public archive.
- No DOI is promised as existing.
- No git history was rewritten and no files were removed from the repository.

## Update 2026-11-11: review-stage access via Anonymous GitHub
- Blinded manuscript: "available at: https://anonymous.4open.science/r/anonymous-spatial-proxy-review-7E02/" (only URL in the statement).
- Title page: development repository private during review; anonymized copy at the same URL; permanent public repository and DOI after acceptance.
- Cover letter: development repository previously public, made private before submission; no preprint-server deposit; separate anonymous repository used for review.
- Upstream of the snapshot: private repository with one fresh root commit (neutral commit metadata), no ancestry from the original repository.
- Zenodo draft: superseded, unpublished fallback.
- After acceptance: publish code/data with a DOI (code MIT; derived tables CC BY 4.0) and update the statement.
