# IJGIS preprint policy audit

Policy (IJGIS Instructions, official page, captured 2026-11-10, `data/raw/journal/ijgis_instructions_webfetch_2026-11-10.md`): the journal "does not consider manuscripts with copies deposited in preprint servers that disclose the authors' identities before acceptance".

| Question | Finding |
|---|---|
| Preprint on arXiv / SSRN / OSF / Research Square / EarthArXiv? | None posted by this pipeline; no preprint DOI exists. AUTHOR to confirm none was posted independently. |
| Earlier manuscript versions publicly accessible? | YES. The public GitHub mirror holds DOCX/PDF manuscripts of the earlier CEUS version with the author's name (`output/CEUS_*`, `output/MANUSCRIPT_*`, handoff files). |
| Is a GitHub repository a "preprint server"? | Not by the usual definition (no DOI, not a preprint service). The literal policy targets preprint servers. However, the files are a public, author-identified copy of an earlier version of the same work, so an editor could treat them as equivalent. |
| Current IJGIS version public? | NO. The IJGIS title, text, builders and cover letter are kept out of the public mirror and sync branch. |

## Risk level

MEDIUM-HIGH. The literal policy (preprint servers) is probably not triggered, but the spirit (identity-disclosing public copy before acceptance) is at risk.

## Mitigations (author decision)

1. Disclose in the cover letter (done: the letter states no preprint-server copy exists and that the public repository held earlier manuscript files).
2. Remove earlier manuscript files from the current public tree, or set the repository private for the review period. No history rewrite is performed by this pipeline.
3. If unsure, ask the IJGIS editorial office before submission.

## Recheck after review-stage actions (2026-11-10)
- The GitHub repository that held author-named manuscript files from the earlier (CEUS) submission is now **PRIVATE** (verified: unauthenticated HTTP 404; IJGIS_GITHUB_PRIVACY_ACTION.md). Active public availability of those files has stopped.
- No independent preprint-server deposit is known (author statement; no arXiv, SSRN, OSF, EarthArXiv or Preprints.org record known to the author).
- Previous public exposure did happen. Search-engine caches or third-party clones made while the repository was public may persist. This is **residual discoverability**, not an active public deposition, and it cannot be undone without misrepresentation.
- Accurate wording, used in the cover letter: "The repository had previously been public but was made private before IJGIS submission; no independent preprint server deposit is known."
- Status: **resolved for review purposes, with a disclosed residual (LOW–MEDIUM)**. The cover letter tells the Editor about the earlier public repository.
