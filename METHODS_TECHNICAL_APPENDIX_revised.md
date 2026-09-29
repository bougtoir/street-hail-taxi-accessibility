# TECHNICAL APPENDIX — REVISED

Unchanged mechanics: equirectangular metric at 35.68N; Dijkstra reachable
sets on the OSM walk graph cached in data/processed/reach.json; 2,000 origins
(seed 42); 10 draws for random relocation (seed 43); 2,000-resample bootstrap
CIs; near-population coverage caveat for p-values (descriptive inference over
the origin sample).

## Added in revision
- run_ablation.py: specs S_ROAD / S_ATTR / S_PROXY / S_COMB evaluated on the
  identical origins, reachable sets, periods and radii; paired Wilcoxon
  signed-rank test of optimizer-vs-nearest-major per spec×radius; top-1%
  segment Jaccard and segment-level Spearman vs combined.
- tables/ablation_summary.csv, ablation_rank_agreement.csv; figure
  fig7_ablation.
- Terminology audit: the constructed proxy renamed "circulation-potential
  proxy" throughout; temporal patterns reclassified as modeled behavior.
- Metric note: relative percentage gain is unstable when S0≈0 (z-scores
  cross zero); primary reporting uses absolute SD-unit gain.

## Sensitivity inventory (now includes ablation)
radius 100–500 m; specs ROAD/ATTR/PROXY/COMB; thresholds +10–100% (secondary);
candidate set all-vs-major (oracle bound retained); kernel σ 150/300/500 m;
10 temporal periods; 5 wards; walking penalty via gain-per-100 m.
