# IJGIS — anonymized review bundle: pre-upload audit

Bundle audited: `output/IJGIS_ANON_REVIEW_REPRO_BUNDLE.zip`
(61 entries; SHA-256 `813a334f2afae595eca7c223aa263e34b47e7bab7fd5b3a0706eb3fcdbf28791`).
The bundle was audited by unpacking it in full and scanning every file, including binaries where that was possible.

| Check | Method | Result |
|---|---|---|
| Author surname / given name (Onishi, Tatsuki) | case-insensitive recursive `grep -I` over all text files | none |
| GitHub username (bougtoir), public-mirror name, `github.com` URLs | same | none |
| Affiliation (Shiga, Shiga University, biwako.shiga-u) | same | none |
| ORCID | same | none |
| Author e-mail (gmail / institutional) | regex over all e-mail-shaped strings | none; all hits are third-party business contacts in the public OpenStreetMap response `cache/4339f7…json` (hotel/shop `contact:email` tags). These were kept as they are, per instruction |
| Devin session links, PR links (`devin.ai`, `pull/803`), branch names (`devin/17…`) | same | none |
| Internal paths (`/home/ubuntu`) | same | none |
| Git metadata (`.git*`, `.pyc`) | `find` | none |
| ZIP archive comment / entry comments | `unzip -z`, `unzip -Z` | none; entries carry only timestamps and permissions |
| LICENSE copyright holder | read | "The authors (anonymized for peer review)" |
| PNG metadata | Pillow `Image.info` | only `Software: Matplotlib 3.10.9` |
| PDF figure metadata | `/Author /Creator /Producer /Title` | only Matplotlib Creator/Producer; no Author or Title |
| Manuscript title in bundle | grep for the title | absent (the bundle holds no manuscript files) |
| Acknowledgements | grep | none |

Non-identifying residue, noted rather than modified because analysis code is frozen:
- The script names `run_ceus_analyses.py` and `make_ceus_figures.py`, and comments in `build_canonical_results.py`, keep the historical prefix "CEUS". This says the analysis was run for an earlier journal pass. It does not identify a person. `REPRO_README.md` already describes the name as historical.
- The HTTP User-Agent in `download_data.py` is `devin-research/1.0 (academic study)`. This names a tool, not a person, and is consistent with the AI-use statement.

Verdict: **PASS.** The review bundle contains no author-identifying information.
