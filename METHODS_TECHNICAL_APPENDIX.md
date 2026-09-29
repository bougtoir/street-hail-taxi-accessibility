# TECHNICAL APPENDIX

## Coordinate/distance handling
Lat/lon equirectangular projection at latitude 35.68N: dx = 111320·cos(lat)·Δlon, dy = 110540·Δlat (meters). Applied to all kernel and proximity computations. Walk distances use true OSM walk-network shortest paths (`networkx.single_source_dijkstra_path_length`, cutoff 500 m, weight `length`).

## Reachability construction
- Origins: 2,000 hail-feasible directed segments sampled without replacement (`numpy.default_rng(42)`).
- For each origin: nearest walk node to the origin edge midpoint → Dijkstra cutoff 500 m → reachable walk nodes → candidate drive edges = any hail-feasible edge whose midpoint lies within 25 m of a reachable walk node; distance credited = shortest walk-node distance.
- Cached in `data/processed/reach.json` (deterministic).

## Models
See ACCESSIBILITY_MODEL_SPECIFICATION.md. Implementation: `analysis/build_segments.py` (env vars SIGMA ∈ {150,300,500}, SUFFIX for sensitivity variants).

## Temporal profile
Published histogram (Tokyo Taxi Center monitor FY2023, hours 6→5): counts = [50,17,133,161,172,157,188,203,176,178,175,223,166,110,103,145,86,78,69,31,18,14,5,4], normalized. Night variant = +3h cyclic shift; weekend nightlife boost = 1.4 on the nightlife share.

## Statistics
Bootstrap 95% CIs: 2,000 resamples per group. Spearman rank correlations (scipy.stats.spearmanr). Because coverage is near-population (all segments within the polygon; all 2,000 sampled origins over all periods), p-values and CIs describe sampling variation of the origin sample, not superpopulation inference; reported as such.

## Strategy definitions
- stay: A at origin segment.
- random: mean over 10 fixed-seed draws of reachable candidates.
- nearest major road: A at the closest reachable segment with w_road = 1 (motorway/trunk/primary).
- best major road (oracle bound): max A among major-class candidates — upper bound of any major-road-only rule.
- flow-only optimum: argmax of Model A — shows whether suitability/context terms change picks.
- full optimizer: argmax of the active model A.

## Software
Python 3.10, osmnx 2.0.7, geopandas 1.1.4, networkx, scipy, pandas, matplotlib, python-docx. Fixed seed 42 throughout.

## Sensitivity inventory (executed)
| Factor | Values | Where |
|---|---|---|
| walking radius | 100/200/300/500 m | strategy_comparison.csv |
| specification | A/B/C | model_agreement.json, gain_corr_across_models.csv |
| improvement threshold | +10/25/50/100% | distance_to_threshold.csv |
| candidate set | all vs major-only (oracle bound) | strategy_comparison.csv (opt_gt_bestmajor) |
| kernel bandwidth | 150/300/500 m | sigma_sensitivity.json |
| temporal | 10 day-type×hour periods | temporal_heterogeneity.csv |
| spatial aggregation | 5 wards | ward_heterogeneity.csv |
| walking penalty | gain per 100 m / per minute proxy | gain_per_meter.csv, utility_summary.csv |
