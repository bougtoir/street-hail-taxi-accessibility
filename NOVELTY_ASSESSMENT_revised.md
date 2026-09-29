# NOVELTY ASSESSMENT — REVISED

## Positioning change
Passenger relocation toward pickup opportunity is itself precedented
(T-Finder, TKDE 2013; walkable PUDO in SMoD systems). We no longer imply
relocation novelty.

## Claimed novelty (data/measurement architecture)
- no fleet GPS telemetry and no proprietary dispatch data anywhere;
- a public-data-derived *opportunity ranking* (not an availability estimate);
- passenger-side candidate relocation generation at road-segment level;
- explicit robustness across alternative public-data constructions
  (road-only / attractor-only / proxy / combined ablation) — a test prior
  recommender systems did not run because they fit observed telemetry.

## Closest prior work (unchanged table, updated interpretation)
T-Finder recommends walkable pickup spots from >12k taxi trajectories; our
ablation framing is distinct: the question is what rankings survive with zero
telemetry. Ocalir/FMOTS and p-median stand models are fleet/planning side.
Yang–Wong–Bell bilateral search equilibria are theoretical.

## Residual novelty statement
"Multiple independent public-data constructions identify consistent local
gradients in modeled street-hail opportunity" — supported by ablation
(ρ 0.52–0.93 across families, positive gain under every construction).

## Desk-rejection risk
Reduced by terminology correction (no observed-flow claims) and ablation;
still moderate because the construct is uncalibrated. Appropriate venues:
transport methods journals tolerant of simulation-based feasibility studies.
