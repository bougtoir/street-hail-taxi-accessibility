# ACCESSIBILITY MODEL SPECIFICATION

All accessibility measures are **relative, standardized (z-score) quantities in SD units**. No specification claims to estimate vacant-taxi counts, probabilities, or waiting times.

## Analytical unit

Directed road segment `e` (each `(u,v,key)` directed edge of the OSM drive graph; opposite directions on two-way streets are distinct units), time interval `t` = hour × {weekday, weekend}. Ten representative periods analyzed: {08,13,17,21,23} × {weekday, weekend}.

## Taxi-flow prior

    F(e,t) = w_road(e) · (0.3 + D(e)) · P(h; ctx(e))

- `w_road`: road-class capacity weight (motorway/trunk/primary 1.0, secondary 0.7, tertiary 0.5, residential/unclassified 0.25, living_street/service 0.10) — assumption, varied implicitly via road-class sensitivity (major-only vs all-roads candidate sets).
- `D(e)`: demand-attractor field = Gaussian kernel (σ=300 m; sensitivity 150/500 m) over attractors weighted as: NLNI station passengers log1p ×1.0, nightlife POI log1p ×0.8, hotel/hospital ×0.6, transit POI ×0.4, plus `w_road` ×1.0 and log1p(node degree) ×0.3. Equal-order-of-magnitude weights; each component log-compressed to avoid single-hotspot dominance.
- `P(h;ctx)`: hourly multiplier from the Tokyo Taxi Center FY2023 monitor survey (normalized histogram), blended toward a +3h-shifted "night" profile by the segment's nightlife-context share `nl_share` (logistic of z-scored nightlife kernel). Weekend × {1 + 0.4·nl_share} boost — assumption, documented.

Segments on motorway/trunk/pedestrian classes are excluded from candidacy (vehicles cannot legally/safely stop for street hails): `hail_ok`.

## Specifications

- **Model A (flow-only):** `A_A(e,t) = z(log1p F(e,t))`
- **Model B (flow + road suitability):** `A_B(e,t) = z(z(log1p F) + 0.5·S(e))`, `S = z(w_road) + 0.5·z(log1p deg) + 0.8·stand100` (within-100 m taxi stand)
- **Model C (flow + road + context):** `A_C(e,t) = z(z(log1p F) + 0.5·S + 0.4·C(e))`, `C = z(log1p k_station) + 0.6·z(log1p k_nightlife) + 0.5·z(log1p k_hotel_hosp)`

Weights are transparent, additive, standardized — chosen as defensible equal-order components, not tuned. The scientific claim rests on whether relocation gain persists *across* A/B/C and σ ∈ {150,300,500}, not on any single score.

## What the models deliberately omit

- No supervised fit against observed vacant taxis (none exist in Paper 1 by design).
- No weather/event terms (not material to the core question; Phase 4).
- No fare, speed, or traffic-congestion fields (not publicly reproducible at segment level for Tokyo).

## Relocation quantities

- `G_A = A*(x0,t) − A0` (best reachable vs origin, within radius r ∈ {100,200,300,500} m network distance)
- `RAG = (A* − A0)/|A0|` where |A0| > 1e-6
- Distance-to-improvement: min walking distance achieving +10/+25/+50/+100% of |A0|
- Utility framing (no minute-equivalent claims): `U(x|x0,t) = Â(x) − λ·walk_m(x)` reported via gain-per-100 m and Pareto summaries rather than λ-commensuration with minutes.
