# TECHNICAL APPENDIX — STRESS TEST

Identical computational pipeline to METHODS_TECHNICAL_APPENDIX_FINAL;
analyses frozen during reframing. Key reporting units:
- Origins: 2,000 sampled (seed 42); 1,961-1,999 with nonempty reachable
  sets per radius; ~19,970 origin-period rows descriptive only.
- Cluster unit: origin. Period-invariant specs: unique-origin inference.
  Period-varying: origin-clustered bootstrap, 5,000 replicates; paired
  Wilcoxon on origin-mean differences.
- Transfer: TG(A->B) = S_B(x*_A) - S_B(x0); nine directed transfers;
  clustered CIs.
- Permutation: 500 reps, unconstrained + within-ward; empirical
  p=(1+#null>=obs)/(1+N); statistics per radius: fraction improved and
  mean absolute gain.
- Data correction carried over: station-presence (unweighted) kernel after
  N02 FY2023 passenger-field absence discovered.
