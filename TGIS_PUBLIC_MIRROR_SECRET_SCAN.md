# Public mirror secret scan (2026-11-27 02:31 UTC)

Target: bougtoir/street-hail-taxi-accessibility main 051ae248345c41da3e26e547662c0395f21573d1, fresh clone, all 392 tracked files (334,078,707 bytes, binary included as UTF-8-ignore text).

Patterns: JWT (`eyJ….….`), GitHub tokens (ghp_/gho_/ghu_/ghs_/ghr_/github_pat_), query-string secrets (token/access_token/api_key/key/sig/signature/secret ≥12 chars), Bearer values, Authorization headers, AWS/Google/Slack keys, private-key blocks, credentials embedded in URLs, password/secret/api-key assignments, Netscape cookie-jar markers, session/csrftoken cookie values, and the leaked link's random nonce. Filenames: .env*, credentials.json, cj.txt, cookie files, *.pem/*.key, id_rsa, token.json, .netrc/.npmrc/.pypirc.

Result: filename hits 0; content hits 0.

Not secrets, and present by design: DOIs, Zenodo record id 24106479 and link id (no token), public GitHub URLs, ORCID 0000-0001-7261-9062, public institutional e-mail.

The submission ZIP was also scanned (32 members, DOCX XML included): no JWT, token value, link nonce, cookie or GitHub token. The only hits are the path name `zenodo_review` in audit prose.

**NO LIVE SECRET FOUND**
