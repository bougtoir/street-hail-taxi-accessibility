# FINAL HANDOFF — street-hail-taxi (Paper 1)

## Final decision: **GO** (not STRONG, not WEAK)

Rationale (≤10 bullets):
- 96-99.6% of sampled origins have a strictly higher-accessibility segment within 200-500 m network distance; 68-99% gain >0.1 SD.
- Mean gain 0.78→2.12 SD across 100→500 m radii (bootstrap CIs exclude zero).
- Optimizer beats random relocation in 94-100% of origins.
- Optimizer beats the naive "nearest major road" in 60-89% of origins (+0.05 to +0.33 SD mean surplus).
- Honest bound reported: the optimum segment is usually a major road at large radii (76% at 500 m); the value added is *which* major road, not "walk to a big street".
- Segment rankings robust: Spearman 0.85-0.97 across specifications A/B/C; gain ρ 0.98-0.99 across kernel bandwidths 150/300/500 m.
- Temporal/district patterns are interpretable (morning peak, ward block-structure differences), not artifact-driven.
- All inputs are legally public: OSM (ODbL), MLIT NLNI, Tokyo Taxi Center/THTA published statistics; acquisition ledger with SHA-256 persisted.
- Claims calibrated: relative accessibility potential only; no vacant-taxi/waiting-time claims; Paper 2 boundary explicit.
- Manuscript, figures, tables, docx/PDF/cover letter and submission ZIP delivered.

## Strongest scientific contribution
A fully public-data, reproducible demonstration that street-hail accessibility has actionable local structure — and a benchmark showing optimization adds real surplus over the "walk to the nearest big road" folk heuristic.

## Weakest assumption
The taxi-flow prior: a proxy built from attractors × road hierarchy × an aggregate hourly profile, untested against any observed vacant-taxi flow (Pseudo-PFLOW was access-restricted, not license-blocked — a joint-research application could supply it).

## Most likely reviewer objection
"The score is not vacant-taxi availability, so the optimization is over a proxy of a proxy." — Mitigated by calibrated language and robustness, but remains the core limitation until Paper 2.

## Does Paper 2 remain justified?
Yes — more so. Paper 1 shows large, robust gradients; calibrating them to measured waiting times is now the binding question.

## What Paper 2 should observe first
Vacant vs occupied taxi passage counts at paired segments (high vs low modeled accessibility, matched by road class) during one weekday evening and one weekend night — the cheapest falsification of the prior's spatial ordering. Waiting-time measurement second; recommendation A/B third.

## Deliverable locations
- Manuscript + letter + ZIP: `output/`
- Code: `analysis/`; data: `data/` (raw excluded from git, regenerable via ledger)
- Tables: `tables/`; Figures: `figures/` (pdf+png)
