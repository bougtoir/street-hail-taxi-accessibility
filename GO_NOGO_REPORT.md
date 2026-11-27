# GO / NO-GO REPORT

Decision recorded **before** manuscript polishing, per Phase 12.

## Evidence against the six criteria (Model C unless noted; n=2000 sampled origins, 10 periods)

1. **Meaningful local heterogeneity** — YES. Fraction of origins with a strictly better reachable segment: 83% (100 m), 96% (200 m), 98% (300 m), 99.6% (500 m). Fraction gaining >0.1 SD: 68%→99% across 100→500 m.
2. **Non-trivial vs random relocation** — YES. Optimizer > random in 94% (100 m) → 100% (500 m) of origins; random relocation yields ~zero mean gain.
3. **Added value beyond the naive major-road heuristic** — YES, with nuance. Optimizer > *nearest* major road in 60% (100 m) → 89% (500 m), mean surplus +0.05→+0.33 SD (bootstrap CIs exclude 0). However, the optimum segment *is itself a major road* in 25% (100 m) → 76% (500 m) of cases, and the optimizer never beats "best major road in radius" (an oracle, not a naive rule). The added value is choosing *which* major road — a real but bounded contribution.
4. **Specification robustness** — YES. Segment-level Spearman ρ between A/B/C = 0.85–0.97; per-origin gain ρ across models ≈ high (see `tables/gain_corr_across_models.csv`); kernel bandwidth σ 150/300/500: gain ρ 0.98–0.99, same-optimum-edge 69–88%. Gain-class transition matrix shows no mass flipping to "none".
5. **Interpretable spatial/temporal patterns** — YES. Gains larger in central commercial wards (Chuo, Chiyoda) and at 500 m; modest hour-of-day variation (highest weekday 08:00), nightlife-shifted weekend evening structure. No single district drives results.
6. **Defensible claim without field validation** — YES, conditional on calibrated language: we claim *relative accessibility gradients and relocation opportunity*, not waiting times.

## Decision: **GO**

(Not STRONG GO: criterion 3's nuance — optimal segments are disproportionately major roads — means part of the value is "which major road, how far"; and scores are uncalibrated to waiting time. Not WEAK GO: effects are large, highly robust, and clearly non-trivial vs naive heuristics.)

## If it had failed (recorded for completeness)
- Failure mode would have been criterion 3 (optimizer ≡ nearest major road). The paired analysis shows this is not the case for the *naive* comparator.
- Paper 2 could rescue even a weak outcome by calibrating scores to measured waiting times.
