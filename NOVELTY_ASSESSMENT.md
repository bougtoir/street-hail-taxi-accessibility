# NOVELTY ASSESSMENT — Paper 1 (public-data street-hail accessibility + pedestrian relocation)

## Closest prior studies

| Study | Data | Unit | Objective | Passenger side? | Relocation? | Public data only? |
|---|---|---|---|---|---|---|
| T-Finder (Yuan et al., TKDE 2013) | GPS trajectories, >12,000 taxis | location grid | recommend pickup spots within walking distance | Yes | Yes (short walks) | No (fleet telemetry) |
| Yang, Wong & Bell bilateral taxi–customer search equilibrium models (TR-B 2010) | theory/calibrated | network | equilibrium meeting probabilities | model-level | No | n/a |
| Taxi-stand location models (SCP/MCLP/p-median; Ocalir 2010; Sage 2020) | GPS demand extraction | stand sites | fleet/planning side | Partial (access willingness) | Stand siting | No |
| Walkable PUDO on-demand shared mobility (ITS/SMoD studies) | Manhattan taxi trip records | pickup points | assignment minimizing rejects/walk/wait | Yes | Yes | Trip records public, but still telemetry-derived |
| Taxi demand/cruising-area prediction (deep learning, Sustainability 2024 etc.) | GPS | grid/area | driver-side cruising optimization | No | No | No |
| NYC TLC / Porto public trip datasets | public trip records | trips | descriptive/prediction | No | No | Yes (but telemetry, different cities) |
| CSIS Pseudo-PFLOW v3.0 business-traffic (taxi/freight) trajectories | synthetic public-ish (JoRAS joint-research application) | trip trajectories | people-flow simulation | No | No | Restricted access (not openly downloadable) |

## Direct overlap

- Passenger-side "walk to a better pickup point" recommendation exists (T-Finder; PUDO literature).
- Taxi-flow estimation from GPS trajectories is a large literature.
- Road-segment accessibility scoring is related to taxi-demand heat maps.

## Residual novelty (do not overstate)

1. **Public-data-only construction**: no fleet telemetry at any stage. The taxi-flow prior is built from OSM road hierarchy, NLNI station passenger volumes, OSM POI attractors, and a published hourly taxi-use profile (Tokyo Taxi Center monitor survey). This makes the pipeline transferable to any city with OSM coverage.
2. **Passenger-side relative accessibility, not availability prediction**: the outcome is a *relative* street-hail accessibility gradient, explicitly not a vacant-taxi probability or waiting time.
3. **Systematic optimizer-vs-heuristics audit**: quantifies the added value of optimization over "walk to the nearest big road" and random relocation at population scale across all sampled origins, which prior recommender work did not benchmark.
4. **Two-paper framing**: Paper 1 is a deliberately dry feasibility study; Paper 2 (not implemented) supplies empirical calibration.

## Closest threat

T-Finder already recommends walkable pickup locations — but it is built on proprietary taxi GPS and outputs pickup-probability estimates learned from telemetry. Our contribution is the *measurement layer* (what can be said with public data alone) plus the benchmark of optimizer surplus over trivial heuristics.

## Desk-rejection risk

Moderate. Risks: (a) "synthetic prior → no real information"; mitigated by framing as feasibility + robustness across specifications and by the optimizer-vs-heuristic result; (b) lack of validation; mitigated by explicit claim calibration and the Paper 2 boundary. A methods/transport journal (e.g., Transportation Research Interdisciplinary Perspectives, J. Transport Geography, IATSS Research) is the realistic venue; avoid venues demanding empirical validation.
