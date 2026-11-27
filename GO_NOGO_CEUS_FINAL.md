# CEUS GO/NO-GO — FINAL DECISION: WEAK GO

Reassessed after the three mandated corrections. Decision rule applied exactly.

## Corrections applied
1. **Cluster-aware inference.** Unique origins n=1,961–1,999 (vs 19,970
   origin-period rows). Origin-clustered bootstrap (5,000 reps) for
   period-varying specs; unique-origin inference for period-invariant
   ROAD/ATTR. CIs and conclusions essentially unchanged — the earlier
   intervals were already tight and clustering did not alter signs.
2. **Cross-specification transfer (300 m).** Road→Attractor: +0.04 SD, 53%
   positive. Attractor→Road: +0.08 SD, 44% positive. ATTR↔PROXY moderate
   (+0.19–0.27 SD, 69–73% positive). ROAD↔PROXY strong (nested). Verdict:
   weak, partially-nested transfer between distinct component families.
3. **Spatial permutation null (500 perms, unconstrained + within-ward).**
   Fraction improved marginally above null at 200–500 m (empirical
   p=0.02–0.09), not at 100 m. Mean gain is BELOW the null (observed 1.50 SD
   vs null 2.61 SD at 300 m) — gain magnitude is fully consistent with
   generic maximum-selection over a heterogeneous surface.

## Rubric match
WEAK GO: self-optimization results are strong; off-diagonal transfer between
the two distinct component families is weak; observed gains are only
modestly distinguishable from the permutation null; the combined optimizer
retains contrast beyond nearest-major-road (81.5% of origins at 300 m,
Wilcoxon p<0.001, clustered CI [0.21,0.23]).

The submission is honest about this: the abstract, results, and conclusion
state the narrow claim — public data yield a candidate ranking with
reliability marginally above a spatial null — not that gains are spatially
exceptional. If a reviewer requires off-diagonal transfer to be strong, the
correct verdict is NO-GO; we report the evidence, not a preferred label.

## Defect found and corrected during this pass
NLNI N02 FY2023 has no passenger-count field (N02_004 = operator name);
k_station was silently all zeros. Corrected to an unweighted
station-presence kernel; the entire pipeline was rebuilt (build_segments,
relocation, stats, ablation, CEUS analyses, figures, tables).
