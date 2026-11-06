# FINAL HOSTILE REVIEW (post-QC)

Adversarial pass over the FINAL_QC package:

1. Self-optimization circularity — addressed head-on in 2.6 (inequality
   shown as OMML) and 4.5; claims calibrated to evidence levels (3.9).
2. 43% vs 44% transfer inconsistency — resolved by single rounding rule
   (nearest whole %) applied to canonical 0.434652 -> 43% everywhere.
3. "Observed taxi flow" terminology — removed; surfaces are consistently
   called modeled public-data proxies (Figure 1 regenerated).
4. Corrupted sentence ("nearest major These values establish") — repaired;
   prose corruption scan finds no residual malformed text.
5. Statistical coherence — clustered bootstrap + Wilcoxon + permutation
   nulls reported with effects, CIs, p-values together; period-invariant
   specs correctly analyzed on unique origins (n=1,997 not 19,970).
6. Negative results preserved — null surfaces reproduce prevalence almost
   fully and EXCEED observed gain magnitude; weak transfer kept central.
7. Scope honesty — street-hail is labeled a motivating case; no
   operational validation claimed; limitations enumerate data gaps.
8. Reproducibility — public repo URL in Declarations; clean-clone
   regeneration demonstrated; fail-loud builders.
9. Remaining fair criticisms: proxies remain uncalibrated (no ground truth
   obtainable); temporal profile partly assumed; these are disclosed in
   4.9, not hidden.
