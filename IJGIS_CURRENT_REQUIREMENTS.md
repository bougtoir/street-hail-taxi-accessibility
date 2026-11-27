# IJGIS current requirements (International Journal of Geographical Information Science, Taylor & Francis)

Access date: 2026-11-10 (UTC). Raw captures and SHA-256 rows: `data/raw/journal/ACQUISITION_LEDGER.csv`.

## Source access notes
- The official Instructions for Authors page (https://www.tandfonline.com/action/authorSubmission?show=instructions&journalCode=tgis20) returns HTTP 403 (Cloudflare challenge) to curl, the session Chrome (CDP) and r.jina.ai. Wayback has no 200 capture after 2023-08 (2024-2026 captures are 403).
- A server-side text fetch succeeded but was truncated by the fetch tool after the heading "Style Guidelines" (`data/raw/journal/ijgis_instructions_webfetch_2026-11-10.md`). Everything before that heading is quoted from the official page; sections after it (Style guidelines, References, Checklist, Data Sharing Policy, Publication Charges) could not be read verbatim from the official page.
- For those later sections, the authoritative sources used are: (a) the official T&F Reference Style V guide PDF (`tf_v.pdf`), (b) the official T&F AI policy and data-sharing policy pages, (c) the verbatim quotation of the IJGIS Data and Codes Availability instructions printed in an IJGIS article (doi:10.1080/13658816.2025.2603586). Third-party summaries (scispace/Articlo) are recorded as non-authoritative and used only to locate the official documents.

## Requirements and compliance

| # | Requirement | Source | Exact requirement (quoted or paraphrased) | Manuscript status / change |
|---|---|---|---|---|
| 1 | Q1 / no mandatory charge | About page | "5.9 (2025) Impact Factor; Q1 Impact Factor Best Quartile"; hybrid "Open Select" — APC only "to make your article open access" | PASS: subscription route, no APC/submission fee. Colour/page charges: section unreadable — AUTHOR ACTION to confirm in ScholarOne. |
| 2 | Aims & scope | About page | "Fundamental and computational issues of geographic information"; "The design, implementation and use of geographical information for monitoring, prediction and decision making" | Manuscript reframed around constructed geographic information products and the validity of optimization on them. |
| 3 | Article types | Instructions | "research articles, review articles, technical communication, software tool articles, book reviews and foresight papers" | Research Article selected (IJGIS_ARTICLE_TYPE_DECISION.md). |
| 4 | Double-anonymous review | Instructions | "double anonymous peer reviewed"; figures/tables "inserted into the main document to facilitate double anonymous peer reviews" | Blinded main manuscript + separate title page. |
| 5 | Preprints | Instructions / About | "does not consider manuscripts with copies deposited in preprint servers that disclose the authors' identities before acceptance" | See IJGIS_PREPRINT_POLICY_AUDIT.md (public mirror carried earlier manuscript files). |
| 6 | Institutional email | Instructions | "All authors should use an institutional email ... non-institutional email will not be considered for peer review" | AUTHOR ACTION (ScholarOne account). |
| 7 | English only | Instructions | "only publishes manuscripts in English" | PASS. |
| 8 | Structure/order | Instructions | "title page; abstract; key policy highlights (if appropriate); keywords; main text introduction, materials and methods, results, discussion; declaration of interest statement; references; appendices" | Followed; title page is a separate file for anonymity. |
| 9 | Figures/tables | Instructions | "Table(s) with caption(s) and figures with captions should be inserted into the main document" | Figures inline after first citation; tables inline after first citation. Separate PNG/PDF figure files also supplied. |
| 10 | Key policy highlights | Instructions | "(if appropriate)"; 3-5, ~100 words, for policy makers | Not appropriate (methodological paper with no policy finding); omitted. CEUS-style Highlights file retired. |
| 11 | Word limit | Instructions | "There are no word limits ... approximately 5,000-8,000 words" ; "Please include a word count" | Word count stated on title page and in the blinded manuscript header. |
| 12 | Abstract | Not readable on official page | Third-party: unstructured, <=200 words | Abstract cut to <=200 words, unstructured (conservative). |
| 13 | Keywords | Not readable on official page | Third-party: 2-5 | 5 keywords (conservative). |
| 14 | Reference style | tf_v.pdf | T&F Reference Style V (Harvard): author surname + year in text, alphabetical list | Converted from Vancouver to author-date Harvard; all 41 refs retained, plus 3 directly-supporting IJGIS GIScience refs (44; see IJGIS_CITATION_ECOLOGY_FINAL.md). If IJGIS now accepts any consistent style, Harvard remains compliant. |
| 15 | Title | Third-party | Sentence case | Title in sentence case. |
| 16 | Data & codes | IJGIS text quoted in doi:10.1080/13658816.2025.2603586; T&F Open Data + FAIR | "ANONYMIZE your data and codes and deposit them in ... Figshare or Dryad ... include a PRIVATE SHARING LINK ... in your Data and Codes Availability Statement"; CC BY/CC0; DOI-minting repository; no "available upon reasonable request" | Anonymized review bundle built (IJGIS_ANON_REVIEW_REPRO_BUNDLE.zip); Figshare private link = AUTHOR ACTION; placeholder in statement. |
| 17 | Software availability | Instructions (Software Tool Articles) | statement before references; anonymous VCS version; archived DOI | Mandatory for software tool articles only; analogous code statement included. |
| 18 | AI disclosure | T&F AI policy | statement with "full name of the tool used (with version number), how it was used and the reason for use"; AI not an author | Disclosure statement included (Devin, Cognition AI). |
| 19 | Declaration of interest | Instructions (structure) | declaration of interest statement | "No potential conflict of interest was reported by the author." |
| 20 | Funding | T&F standard | funding statement | "This work received no external funding." (title page; neutral in blinded file) |
| 21 | Image descriptions | Instructions | optional alt text | Not supplied (optional). |

## Deviations from the handoff prompt
- Highlights: the prompt allows regeneration only if required; IJGIS requires none (only optional policy highlights), so no highlights file is produced.
- Abstract/keyword limits are taken from non-official summaries because the official section was unreadable; the conservative values are used and flagged for author check in ScholarOne.
