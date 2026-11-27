# Transactions in GIS — current submission requirements audit

Access date for all sources: 2026-11-24 (UTC). Saved copies, SHA-256 and HTTP status: `data/raw/journal/tgis/ACQUISITION_LEDGER.csv`.

**Evidence limitation.** The journal-specific Wiley pages (`onlinelibrary.wiley.com/page/journal/14679671/...`) returned a Cloudflare security challenge (HTTP 403) to curl, Playwright via CDP, a text proxy and the GUI browser on 2026-11-24. Journal-specific rules below therefore come from the **latest available Wayback snapshot of the TGIS Author Guidelines (2022-03-08)** and the **Wayback journal home page (2025-07-02)**. Wiley-wide policies were read **live**. Rows are labelled H (historical journal-specific snapshot) or L (live publisher page). H rows must be re-checked on the Research Exchange submission form at upload (see FINAL_HANDOFF_TGIS.txt).

Sources:
- [S1] TGIS Author Guidelines, Wayback 2022-03-08: http://web.archive.org/web/20220308102520/https://onlinelibrary.wiley.com/page/journal/14679671/homepage/forauthors.html (file `01_forauthors_wayback20220308.html`)
- [S2] TGIS journal home, Wayback 2025-07-02: http://web.archive.org/web/20250702041826/https://onlinelibrary.wiley.com/journal/14679671 (`02_...`)
- [S3] Wiley data sharing policy (live): https://authorservices.wiley.com/author-resources/Journal-Authors/open-access/data-sharing-citation/data-sharing-policy.html (`05_...`)
- [S4] Wiley Free Format submission (live): https://authorservices.wiley.com/author-resources/Journal-Authors/Prepare/free-format-submission.html (`08_...`)
- [S5] Wiley AI guidelines (live): https://www.wiley.com/en-us/publish/article/ai-guidelines (`11_...`)
- [S6] Wiley self-archiving (live): https://authorservices.wiley.com/author-resources/Journal-Authors/licensing/self-archiving.html (`12_...`)
- [S7] Wiley ethics guidelines (live): https://authorservices.wiley.com/ethics-guidelines/index.html (`04_...`)

| # | Item | Exact requirement (source) | Compliance | Action taken / required |
|---|---|---|---|---|
| 1 | Aims and scope | Advances in spatial sciences, GIScience, geocomputation, spatial analysis, spatial data quality and decision support; Research Articles in scope [S1 H, S2 H] | Compliant: question framed as representation/specification uncertainty in optimization of constructed spatial representations | Light reframe in Introduction and §4.6 only |
| 2 | Article type | Research Article [S1 H] | Compliant | Select "Research Article" at upload |
| 3 | Peer-review model | Single-blind peer review [S1 H] | Compliant: author-identified manuscript and title page; anonymous-review wording removed | Re-confirm on submission form |
| 4 | Abstract | ≤150 words, no citations [S1 H] | 135 words, no citations | — |
| 5 | Keywords | 5–6 keywords [S1 H] | 6 | — |
| 6 | Formatting | Free Format at initial submission; 12-pt standard font preferred, double spacing [S1 H, S4 L] | Times New Roman 12 pt, double-spaced, single DOCX + PDF | — |
| 7 | Title page | Informative title without abbreviations, running title <40 characters, full author names, affiliations, COI, acknowledgments [S1 H] | Running title 39 characters; separate title page with name, affiliation, email, ORCID, COI, acknowledgments | — |
| 8 | Tables | Tables on separate pages after the reference list, editable [S1 H] | 5 editable Word tables after References (also in `TGIS_TABLES_EDITABLE.docx`) | — |
| 9 | Figures | Figures uploaded as separate files; legends in manuscript [S1 H; Free Format S4 L allows inline at first submission] | 9 separate PNG files `Figure_1.png`–`Figure_9.png`; captions after tables | — |
| 10 | Equations | Display equations numbered sequentially [S1 H] | 3 OMML display equations numbered (1)–(3) | — |
| 11 | Reference style | APA author-date, alphabetical, DOIs where available [S1 H] (2022 text cites APA 6th; APA 7 used here as current APA) | 51 references, APA 7, alphabetical, all cited, DOIs given where they exist | — |
| 12 | Data sharing | Journal expects data in a public repository; Data Availability Statement mandatory for all research articles [S1 H, S3 L] | DAS present; public source data, derived data/code and raw-stage limitation separated | Public repository must be visible before upload (TGIS_PUBLIC_REPOSITORY_AUDIT.md) |
| 13 | Code sharing | Scripts and analytic artifacts publicly archived whenever possible [S1 H] | Code, canonical registry and tables in public GitHub repository | — |
| 14 | Conflict of interest | COI statement required [S1 H, S7 L] | "The author declares no conflict of interest." in manuscript and title page | — |
| 15 | Funding | Funding in Acknowledgments [S1 H] | "This research received no external funding." in Acknowledgments | — |
| 16 | ORCID | ORCID iD requested at submission [S1 H] | ORCID 0000-0001-7261-9062 on title page and cover letter | Link ORCID in Research Exchange |
| 17 | AI use | Disclose AI assistance with drafting/editing/formatting in Acknowledgments; AI assistance with methodology/data/analysis in Methods [S5 L] | Acknowledgments (full statement) + Methods §2.13 sentence | — |
| 18 | Supplementary information | Optional; may be supplied as separate files [S1 H] | None submitted; all supporting material in the public repository | — |
| 19 | Submission system | Research Exchange: https://wiley.atyponrex.com/journal/TGIS [S1 H] | — | Upload there |
| 20 | Open access / subscription | Hybrid; OnlineOpen optional, APC only if chosen; otherwise standard copyright transfer [S1 H, S2 H] | Standard subscription route chosen; no APC | Decline OnlineOpen at acceptance |
| 21 | Preprints | Submitted version may be self-archived at any time [S6 L] | No preprint posted (not required) | — |
| 22 | Originality | Not under consideration elsewhere [S7 L] | Stated in cover letter | — |
