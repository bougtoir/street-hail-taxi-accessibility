# GO / NO-GO REPORT — REVISED

Revised criterion (Phase 12 of the revision brief): "Is there a sufficiently
non-trivial and robust public-data-derived spatial ranking to justify empirical
validation in Paper 2?"

## Ablation evidence (n=2000 origins, 10 day-type×hour periods)

| Spec | ρ vs combined | % origins improved (300 m) | % beats nearest major (300 m) | % beats random |
|---|---|---|---|---|
| Road-only | 0.73 | 95.3% | 66.4% | 99.8% |
| Attractor-only | 0.52 | 99.0% | 99.2% | 99.8% |
| Circulation-potential proxy | 0.93 | 98.3% | 82.4% | 99.8% |
| Combined | — | 98.3% | 79.7% | 99.8% |

Paired Wilcoxon signed-rank tests of optimizer-minus-nearest-major: p ≈ 0 for
all specs/radii (effect sizes reported with bootstrap CIs in
tables/ablation_summary.csv; significance not relied on alone).

## Reassessment

- The relocation signal does **not** collapse under ablation: both component
  families independently yield large local gains (the spatial heterogeneity is
  real within the modeled construct, not tautological to the composite).
- The combined model's ranking is mostly the circulation-proxy (ρ 0.93);
  attractor-only rankings diverge substantially (ρ 0.52) yet still produce
  positive relocation contrasts — consistent independent gradients, the
  stronger allowed claim.
- Caveat preserved: combined optimizer exceeds the *naive* nearest-major-road
  in 60–89% of origins; the optimum segment is usually major-class at large
  radii. Value = which corridor, not "walk to a big street".

## Decision: **GO**

(Upgraded confidence vs pre-ablation WEAK-GO risk on criterion 4; not STRONG
GO because rankings are only moderately specification-stable: attractor-only
ρ 0.52 and best-major coincidence at 500 m show the score family still matters.)

## Failure modes checked
- Result does not disappear under ROAD-ONLY: large gains persist (road
  structure alone has local variation) — but the combined/proxy ranking is
  only moderately similar (ρ 0.73), so conclusions are stated per-construct.
- Result does not disappear under ATTRACTOR-ONLY.
- Nearest-major-road does not explain most of the result at radii ≤300 m for
  PROXY/COMB and essentially never for ATTR.
- Composite is not a tautology of its inputs: components were evaluated
  separately and the combined optimum differs from any single-component one.
