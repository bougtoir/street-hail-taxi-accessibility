# FINAL HANDOFF — CEUS

**A. Decision: WEAK GO.** Cross-specification transfer between distinct
component families is weak (ROAD->ATTR 53%, ATTR->ROAD 44% positive), and
gain magnitudes do not exceed the spatial permutation null — but
improvement reliability marginally does (p=0.02-0.09), ablation shows the
signal survives decomposition, and the combined optimizer retains contrast
beyond nearest-major-road (82% at 300 m).

**B. Cluster correction.** Previous inferential n: 19,970 origin-period
rows treated as independent. Corrected: 1,961-1,999 unique origins
(origin-clustered bootstrap, 5,000 reps; unique-origin inference for
period-invariant specs). CIs widened slightly; no conclusion changed.

**C. Cross-specification transfer (300 m, mean TG / % positive):**
| selector | ->ROAD | ->ATTR | ->PROXY | ->COMB |
|---|---|---|---|---|
| ROAD | (self) | 0.04 / 53% | 1.48 / 90% | 1.37 / 93% |
| ATTR | 0.08 / 44% | (self) | 0.27 / 69% | 0.36 / 69% |
| PROXY | 1.58 / 87% | 0.19 / 73% | (self) | 1.46 / 97% |

**D. Spatial permutation (300 m, weekday 17:00, 500 perms).** Fraction
improved: observed 0.983 vs null 0.979 (p=0.074); at 200/500 m p=0.03/0.09.
Mean gain: observed 1.50 SD vs null 2.61 SD (p=1.0 — magnitude NOT above
null). Within-ward null: same pattern. Interpretation: the real surface
offers reliability, not magnitude.

**E. Nearest-major-road:** combined optimum retains non-trivial contrast —
82% of origins better, +0.22 SD mean surplus, clustered CI [0.21,0.23],
Wilcoxon p<0.001.

**F. Strongest supported claim:** "Public urban data yield a candidate
ranking of modeled street-hail opportunity whose local improvement
reliability marginally exceeds a spatial permutation null and whose
contrasts weakly transfer between distinct data layers — a testable basis
for empirical validation, not evidence of waiting-time benefit."

**G. Most important unresolved limitation:** no empirical link from score to
vacant-taxi passage/waiting time (and now quantified: gain magnitude is
consistent with generic max-selection).

**H. Paper 2 top priority:** roadside vacant/occupied taxi passage counts at
high- vs low-ranked segments within 300 m walks — the minimal test of
whether the ranking tracks reality.

**I. CEUS fit (3-5 sentences).** The paper is a geospatial computation
study of urban information structure: opportunity fields on a directed road
network, walking-distance accessibility, and a validation architecture for
public-data mobility models. The taxi application demonstrates a general
method for data-constrained mobility settings. It does not address fleet
operations, matching, or dispatch, and so belongs with CEUS's
geospatial/urban-computation scope rather than a transportation-operations
venue.

**J. Remaining author inputs:** author names/affiliations on title page;
optional abstract trim (~10 words) if the strict 250-word limit is enforced;
Editorial Manager submission metadata; final sign-off on the WEAK-GO
framing.
