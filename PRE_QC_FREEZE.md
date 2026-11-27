# PRE-QC FREEZE — scientific content snapshot before the submission-engineering QC pass

Snapshot of the accepted-GO package `CEUS_STRESS_TEST_submission_SCIENCE_FINAL.zip`
(commit d5549a52f). This QC pass must not silently change science; every
correction below is document-engineering/reproducibility only.

## Title
"Stress-testing public-data urban accessibility proxies: street-hail taxi
relocation without fleet telemetry"

## GO decision
GO — see GO_NOGO_STRESS_TEST_SUBMISSION_FINAL.md (stress-test framing internally
consistent; null/limiting results reported transparently; no validated-siting
claim).

## Frozen scientific claims (from FINAL_HANDOFF_CEUS_SCIENCE_FINAL.md)
- One-sentence contribution: falsification-oriented framework for auditing
  spatial optimization of constructed urban proxies; self-optimization alone
  is insufficient evidence of meaningful or transferable opportunity.
- Supporting results (canonical values in analysis/canonical_results.json):
  COMB 300 m: frac_pos = 0.9844, mean_G = 1.5000 SD, ci_G = [1.462, 1.539];
  ROAD→ATTR frac_pos = 0.5283 / mean_TG = 0.038 SD;
  ATTR→ROAD frac_pos = 0.4347 / mean_TG = 0.082 SD;
  permutation (weekday_17) empirical p (frac) = 1.0 / 0.030 / 0.074 / 0.086
  at 100/200/300/500 m; null mean gain 2.608 SD vs observed 1.499 SD at 300 m;
  beats nearest-major 81.5% at 300 m (diff 0.223 SD, CI [0.211, 0.235]).
- Strongest supported claim: optimization gain and proxy validity are
  separate questions; apparent gains can survive despite limited
  transferable structure.
- Claim deliberately NOT made: selected locations improve actual taxi
  access or waiting time.
- Key negative finding: weak bidirectional transfer between component
  families; null magnitude exceeding observed magnitude.

## Canonical analysis outputs (frozen inputs)
- tables/ablation_summary_clustered.csv (17 spec×radius cells)
- tables/transfer_summary.csv (36 selector×evaluator×radius cells)
- tables/permutation_null.json + data/processed/perm_null_arrays.npz (2 periods × 4 radii)
- tables/ablation_rank_agreement.csv, tables/sigma_sensitivity.json,
  tables/model_agreement.json, tables/strategy_comparison.csv and other
  tables/*.csv
- data/processed/{ablation_results.parquet, transfer_results.parquet,
  perm_null_arrays.npz} (committed intermediates)

## Abstract conclusions
Large apparent within-score gains (98% of origins improved, +1.50 SD at
300 m) coexisting with weak cross-specification transfer (~53%/~43%
positive, near-chance) and permutation surfaces that reproduce ~all
improvement prevalence with larger mean magnitudes → self-optimization
alone is insufficient validation; ablation + transfer + null comparison +
heuristic benchmarking proposed as internal stress tests.

## Known engineering defects to fix (do NOT alter science)
hardcoded analysis values in builders; 43%/44% ATTR→ROAD inconsistency;
figure numbering not in first-citation order; uncited tables/figures;
plain-text math instead of OMML; literal asterisks; stale Figure 1
terminology; corrupted §3.3 sentence ("the nearest major These values
establish…"); incomplete public-repository availability statement.
