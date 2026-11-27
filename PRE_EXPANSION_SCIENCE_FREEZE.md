# PRE-EXPANSION SCIENCE FREEZE (literature-expansion pass)

- Title: "Stress-testing public-data urban accessibility proxies: street-hail
  taxi relocation without fleet telemetry"
- Central claim (unchanged): self-optimization alone is insufficient
  validation of a constructed urban spatial proxy; ablation/transfer/nulls/
  heuristics are complementary internal stress tests.
- Key results (frozen, all from analysis/canonical_results.json):
  COMB.300 frac_pos=98%, mean_G=1.50 SD, gt_nearmaj=81%, diff_nearmaj=0.223
  [0.211,0.235], Wilcoxon p<0.001; transfer ROAD->ATTR 53% / ATTR->ROAD 43%;
  weekday_17 emp_p_frac=1.0/0.03/0.07/0.09; null_reproduces_frac ~100%.
- Limitations: no ground truth, uncalibrated proxies, modeled temporal
  structure, Tokyo specificity, roadside feasibility imperfect, unweighted
  station term.
- Figures: fig1_framework..fig9_heterogeneity (9). Tables: 1-5.
- References: 10. Word counts: Abstract 248, Intro 446, Methods 388,
  Results 564, Discussion 671, Conclusion 93, main text ~2410.
- Constraint: no analysis-derived number may change; unfavorable
  transfer/null findings stay visible.
