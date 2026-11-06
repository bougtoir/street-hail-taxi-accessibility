# OPPORTUNITY SCORE SPECIFICATION — FINAL (CEUS)

Same as the revised specification with one data correction:
- Station term is now an UNWEIGHTED station-presence kernel over the 329
  NLNI N02 stations in/near the study area (FY2023 N02 has no passenger
  field; the earlier N02_004-as-passengers reading was a defect, corrected).
- All scores z-standardized; sigma=300 m (150/500 sensitivity); specs
  S_ROAD / S_ATTR / S_PROXY / S_COMB unchanged in form.
- Inference: origin-clustered bootstrap (5,000 reps); ROAD/ATTR evaluated on
  unique origins (period-invariant).
- New audit metrics: cross-specification transfer gain TG(A->B) and
  spatial permutation nulls (unconstrained + within-ward, 500 perms).
