# IJGIS — Anonymous GitHub review repository: content audit (Phase 3)

Source of content: the approved anonymized bundle `IJGIS_ANON_REVIEW_REPRO_BUNDLE.zip` (pre-upload audit PASS), unpacked into a **new empty directory outside the working tree** (no fork, no `git clone --mirror`, no `.git` copied). Changes relative to the bundle:

| Change | Reason |
|---|---|
| `REPRO_README.md` → `README.md` rewritten | reviewer-facing README (Phase 4): neutral wording, no title, author, institution, journal, PR or links |
| `+ DATA_SOURCE_AUDIT.md` | **reproducibility fix**: `build_canonical_results.py` reads it, and the bundle's quick check failed without it. 0 identifying hits |
| `+ data/processed/ceus_rerun.log` | **reproducibility fix**: the registry reads `segments/hail_ok` from it. Absolute paths `/home/ubuntu/repos/wip/street-hail-taxi/` in warning lines were replaced with `./`; no values changed |
| `+ requirements.txt` | pinned versions of the environment that produced the results |
| `+ tests/verify_reproduction.py` | reviewer QC: checks the manifest and regenerates the registry |
| `MANIFEST.csv` regenerated | 65 files, SHA-256 |

## Recursive scan (all 69 tracked files, contents and file names)
Patterns: onishi, tatsuki, 大西, bougtoir, shiga, shiga-u, biwako, ORCID pattern `\d{4}-\d{4}-\d{4}-\d{3}[\dX]` and `0000-0001-7261-9062`, e-mail pattern, github.com, pull/803, street-hail-taxi-accessibility, devin.ai, devin/17, `/home/`, `/Users/`, `C:\Users`.

| Finding | Assessment |
|---|---|
| Author name / handle / institution / ORCID / author e-mail / GitHub or PR or Devin URLs / absolute paths | **0 hits** |
| `shiga` × 18, in `cache/*.json` only | substrings of Tokyo OSM place names (Hitotsu**bashiga**shi, **Shiga**raki Street, Zo**shiga**ya, Ichigaya "**Shiga**ku Kaikan"). Not identifying. Left untouched (frozen data) |
| e-mail pattern × 2 in `ablation_results.parquet`, `fig2_map.pdf` | false positives in compressed binary bytes |
| 50 e-mail addresses in `cache/*.json` | third-party OSM POI `contact:email` tags (public ODbL data), unrelated to the author |
| CITATION.cff, pyproject.toml, setup.py/cfg, .zenodo.json, git config files | none present |
| LICENSE | "Copyright (c) 2026 The authors (anonymized for peer review)" |
| Figures | PNG/PDF metadata limited to Matplotlib creator strings (pre-upload audit) |
| Manuscript, title page, cover letter, CEUS documents | none included |

Anonymous GitHub term list: **do not** include "Shiga". The service would replace the OSM place-name substrings above with XXX and corrupt the cached data. The content is already clean, so the term list is only a safety net: `Onishi`, `Tatsuki`, `bougtoir`, `shiga-u`, `biwako` (0 occurrences each).

Result: **NO author-identifying information remains.**
