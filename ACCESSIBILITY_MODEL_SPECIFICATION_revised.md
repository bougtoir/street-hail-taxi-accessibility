# OPPORTUNITY SCORE SPECIFICATION — REVISED

Terminology: all measures are **public-data-derived relative street-hail
opportunity scores** (z-standardized, SD units). Nothing here is observed taxi
flow, vacant-taxi availability, or a waiting-time estimate.

## Unit and time
Directed road segment e (OSM drive edge (u,v,key)); t = hour × {weekday,
weekend}; 10 representative periods.

## Circulation-potential proxy (replaces "taxi-flow prior")

    P_circ(e,t) = w_road(e) · (0.3 + D(e)) · P(h;ctx(e))

Same components as before — documented as a *modeled* proxy: road-class
capacity, demand-attractor kernel field D(e) (σ=300 m; sensitivity 150/500),
hourly multiplier P(h;ctx) from the published monitor-survey profile with a
modeled nightlife blend and weekend boost (assumption, not observation).

## Specifications (ablation family)

- **S_ROAD (road-only):** z(z w_road + 0.5·z log1p deg + 0.3·z log1p lanes).
  No attractor terms.
- **S_ATTR (attractor-only):** z(z log1p k_station + 0.6·z log1p k_nightlife +
  0.5·z log1p k_hotel_hosp + 0.4·z log1p k_transit + 0.8·stand100).
  No road-hierarchy terms beyond mapping scores to segments.
- **S_PROXY (circulation-potential):** z(log1p P_circ) — the renamed prior.
- **S_COMB (combined):** z(z log1p P_circ + 0.5·S + 0.4·C) — unchanged former
  Model C.

## Metrics (recalibrated)
- **Primary:** absolute gain in standardized score, G = S*(x0,t) − S0;
  fraction of origins improved; distance to prespecified score improvement.
- **Secondary:** RAG retained only where |S0|>1e-6, flagged as denominator-
  unstable near zero; never a headline statistic. Rank/percentile improvement
  reported where informative.
- Utility framing: gain per 100 m walked / Pareto summaries; no conversion to
  minutes.
