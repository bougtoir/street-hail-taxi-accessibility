# Hostile review — IJGIS final

Reviewer stance: an IJGIS referee looking for reasons to reject. Each objection is answered with what the manuscript does, and residual risk is stated.

| # | Objection | Response in manuscript | Residual risk |
|---|---|---|---|
| 1 | "This is an urban/taxi paper, not GIScience." | Title and abstract no longer name taxis; the Introduction opens with constructed geographic information products (Goodchild 1992; Longley et al. 2015) and error propagation (Heuvelink et al. 1989); the taxi case is labelled the empirical demonstration and "not the source of novelty" (Introduction); Discussion 4.6 states the GIScience implication (representation choice as a testable component of decision support). | Medium: the empirical sections remain taxi-specific by design (frozen analysis). |
| 2 | "Maxima exceeding a baseline is trivial." | Agreed and stated: gains are "partly structural by construction" (2.6, 3.2, 4.1). The paper's point is exactly that this gain is not evidence; it is the starting point that the other tests must constrain. | Low. |
| 3 | "Transfer is sensitivity analysis renamed." | 4.5 distinguishes them: sensitivity asks whether an answer changes; transfer evaluates the decision chosen under one representation against another, a falsification-oriented test. The novelty audit concedes the components are standard. | Medium. |
| 4 | "Spatial permutation is standard." | Agreed (Besag and Diggle 1977; Manly 2007). It is used as a calibrated reference for what optimization delivers on any heterogeneous surface; the result (nulls reproduce prevalence and give larger gains) is reported in full, and the constrained-null sensitivity (2.10, 3.7) checks the null's strength. Autocorrelation-preserving surrogates are named as a future direction (4.9). | Medium. |
| 5 | "No external ground truth." | Stated as the premise, not hidden: no fleet telemetry exists; the paper claims internal evidence only; 4.11 lists what external validation would need. No claim of improved taxi access. | Low (by design). |
| 6 | "Proxy surfaces are arbitrary." | They are defensible alternatives built from public data (2.4, Table 1); arbitrariness among defensible constructions is the representation uncertainty the audit measures. | Low–medium. |
| 7 | "Tokyo only." | Limitations (4.10) restrict claims to the study area; the method transfers, the numbers do not. | Medium. |
| 8 | "The framework is not validation." | Agreed and stated: the audit can falsify naive readings but cannot validate; wording uses "practical" and "exposes the distinction", never that the framework validates the proxy (language-lock gate G17). | Low. |
| 9 | "Better suited to a transport journal." | The contribution is about optimization on constructed geographic representations, within IJGIS scope ("use of geographical information for ... decision making"); cover letter states this. | Medium (editor judgment). |
| 10 | "Negative result; what is the contribution?" | The contribution is a reusable audit sequence and a demonstration that it changes the interpretation of a headline gain; 4.9 gives four research directions. | Medium. |
| 11 | "Public repository breaks anonymity." | Disclosed (IJGIS_ANONYMITY_RISK_AUDIT.md; cover letter). Blinded files clean; anonymized Figshare bundle for reviewers. | HIGH until the author decides on the public mirror. |
| 12 | "Preprint policy." | No preprint-server copy; public GitHub holds earlier manuscript files — disclosed (IJGIS_PREPRINT_POLICY_AUDIT.md). | Medium–high. |
| 13 | "Open Data + FAIR incomplete." | Statement compliant in form; private link, DOI and licence confirmation pending (IJGIS_OPEN_DATA_FAIR_AUDIT.md). Original derived raw snapshots partly missing; Overpass responses archived and network rebuilt with identical edge/node counts. | Medium until the deposit exists. |
| 14 | "Too little GIScience/IJGIS literature." | Three directly relevant IJGIS papers added, each tied to a sentence; no citation padding (IJGIS_CITATION_ECOLOGY_FINAL.md). | Low–medium. |

## Additional checks

- Unfavourable findings retained verbatim in substance: weak cross-family transfer, nulls reproducing improvement prevalence with larger mean gains, prevalence advantage small and radius-dependent.
- Stress-test / falsification framing retained (Introduction contribution list, 4.5, Conclusion).
- A pre-existing rendering defect was found and fixed: the CEUS manuscript printed the literal text "{NWE}-edge" in 2.3 because one string lacked the f-prefix; the IJGIS build prints the canonical walk-edge count.

Verdict of hostile review: no fatal scientific objection beyond the disclosed design limits; the decisive risks are procedural (anonymity, preprint, data deposit).
