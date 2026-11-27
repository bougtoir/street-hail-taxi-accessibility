# Hostile review — TGIS submission (final)

Reviewer stance: a TGIS referee looking for reasons to reject. Five areas (manuscript, statistical design, figures/tables, reproducibility, claim strength), each issue ranked by severity / effect of fixing / feasibility with current data. Values are those of `analysis/canonical_results.json` (unchanged).

## 1. Manuscript and fit

| # | Objection | Severity | Response in this version | Status |
|---|---|---|---|---|
| M1 | "A taxi relocation paper; transport, not GIScience." | desk-reject risk | Introduction now frames the problem as representation/specification uncertainty in constructed spatial surfaces used by spatial decision support (Couclelis, 2003; Aerts et al., 2003; Devillers et al., 2010); the taxi case is the demonstration. Cover letter states the GIScience question first. | Resolved |
| M2 | "Nothing new: ablation, permutation nulls, heuristic benchmarks exist." | major | No component is claimed as new. The stated contribution is only their integration into an internal falsification-oriented audit with a five-level evidence hierarchy (TGIS_NOVELTY_AUDIT.md). | Resolved (claim calibrated) |
| M3 | "No ground truth, so what is validated?" | major | Paper states explicitly that Levels 1–4 are addressed and Level 5 (external empirical validation) was not performed; it claims no waiting-time, availability, hail-success or welfare effect. | Resolved |
| M4 | Length 5,722 words + 5 tables + 9 figures. | minor | TGIS sets no hard word limit in the archived guideline; figure count is high but each figure is cited and carries a distinct diagnostic. | Accept as is; editor may ask to move Figures 8–9 to supplement |

## 2. Statistical design

| # | Objection | Severity | Response | Status |
|---|---|---|---|---|
| S1 | Origins are not independent (spatial clustering). | major | Clustered bootstrap by ward/grid reported in Methods and tables; CIs come from it. | Resolved |
| S2 | Permutation p-values (0.030 at 200 m; 0.074 / 0.086 at 300/500 m; 1.000 at 100 m) are mixed and multiple. | major | Reported unadjusted and interpreted as weak discrimination; the text does not claim the null is rejected across radii; the gain-magnitude null exceeds observed values at all radii and is stated as unfavourable. | Resolved (no overclaim) |
| S3 | Permutation that preserves autocorrelation? | major | Unconstrained and within-ward constrained permutations both reported; the Discussion states that autocorrelation can compress local extrema but does not by itself produce the observed prevalence. | Resolved |
| S4 | Transfer asymmetry (ROAD→ATTRACTOR ≈53% positive vs ATTRACTOR→ROAD ≈43%). | moderate | Reported both directions; described as weak transferable structure, not as near-chance or as failure. | Resolved |
| S5 | Heuristic surplus (≈+0.22 SD, ≈81.5% of origins) is within the same score. | moderate | Stated as a same-score comparison (Level 2), not as validity. | Resolved |

## 3. Figures and tables

| # | Objection | Severity | Response | Status |
|---|---|---|---|---|
| F1 | Figures embedded or tables inline would violate format. | format | 0 inline images; 9 separate PNG files; legends after tables; 5 editable tables after References. | Resolved (gates 14–17, 30) |
| F2 | Numbers in figures differ from text. | major | Figures produced by frozen scripts from the same tables; text/table/canonical consistency gates 18–19 PASS. | Resolved |

## 4. Reproducibility

| # | Objection | Severity | Response | Status |
|---|---|---|---|---|
| R1 | "Code available on request." | major | Public GitHub repository (Onishi, 2026) with MANIFEST.csv and a one-command registry check; clean-clone byte identity documented (TGIS_CLEAN_CLONE_REPRODUCTION.md). | Resolved once repository is public (gate 34) |
| R2 | Raw OSM POI responses not retained. | moderate | Stated in the DAS and README; reproduction is from archived derived data; raw-stage recreation not claimed. | Disclosed limitation |
| R3 | One reference DOI pointed to an unrelated article. | moderate | Found in this pass (Hwang et al., 2015) and corrected against Crossref; gate 2 now checks author and title for all DOIs. | Resolved |

## 5. Claim strength

Banned phrases (near-chance, chance-level, coin flip, statistically equivalent to 50%, minimal framework, the framework works) absent (gate 2/26 text scan). "A geographic proxy is not validated merely because it can be optimized" retained. No operational, causal or external-validity claim.

## Prioritised list

- 最優先（投稿前に必須）: public repository reachable logged-out with TGIS files (R1, gate 34).
- 高優先: none open.
- 中優先: editor may request fewer figures (M4); optional Zenodo DOI at acceptance.
- 任意: repository still contains historical files named after earlier target journals; harmless under single-blind review but can be pruned in a later release.

## Verdict

No unresolved blocking issue in manuscript, statistics, figures/tables or claims. Remaining blocker is external availability of the public repository only (checked separately by gate 34).
