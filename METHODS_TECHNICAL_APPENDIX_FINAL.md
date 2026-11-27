# TECHNICAL APPENDIX — FINAL (CEUS)

Adds to the revised appendix:
- Clustering unit: origin (2,000 sampled, 1,961-1,999 with nonempty
  reachable sets). ROAD/ATTR: period-invariant scores -> unique origins.
  PROXY/COMB: origin-clustered bootstrap over all period rows, 5,000
  replicates; paired Wilcoxon on origin-mean differences.
- Cross-specification transfer: TG(A->B) = S_B(x*_A) - S_B(x0), same period
  for varying evaluators; all nine directed transfers; clustered CIs.
- Spatial permutation: scores shuffled across all 27,887 hail-feasible
  segments (500 reps) preserving marginals, geometry, origins, candidate
  counts; constrained variant shuffles within ward. Empirical
  p = (1 + #{null >= obs})/(1 + N).
- Data defect note: station passenger weights removed (N02 FY2023 lacks the
  field); unweighted presence kernel substituted; full rebuild performed.
