# IJGIS novelty audit

## Claim boundary

Not novel (stated in the manuscript): ablation, cross-specification transfer as such, spatial permutation tests (Besag and Diggle 1977; Manly 2007), heuristic baselines, clustered bootstrap, multiverse/specification-curve ideas (Steegen et al. 2016; Simonsohn et al. 2020), MAUP and error propagation (Openshaw 1984; Heuvelink et al. 1989).

Claimed contribution (Introduction, final paragraph): the integration of (i) component ablation, (ii) cross-specification transfer, (iii) spatial-null comparison and (iv) heuristic benchmarking into one internal audit of *optimization performed on a constructed geographic information product*, with explicit evidence levels separating apparent optimization gain from transferable spatial structure — and an empirical demonstration in which the audit constrains the naive reading.

## Differentiation

| Neighbouring work | What it does | What this paper adds |
|---|---|---|
| Composite-indicator sensitivity (OECD/JRC 2008; Saltelli et al. 2008; Greco et al. 2019) | varies weights/aggregation, reports rank stability | evaluates the *decision* (selected location) under another specification and against spatial nulls |
| Multiverse / specification curve | enumerates analysis paths for an estimate | applies the idea to spatial optimization outputs; transfer gain as the quantity |
| GIS error propagation (Heuvelink et al. 1989) | propagates input uncertainty to outputs | asks whether an optimum survives alternative representations and randomized ones |
| Taxi hotspot/recommender studies (Yuan et al. 2011, 2013) | validated against fleet GPS | addresses the case where no fleet data exist; makes no operational claim |
| Infrastructure siting (Kuby and Lim 2005) | optimizes a demand proxy | provides internal tests for such proxy optimization |

## Risk

A reviewer may judge integration of standard tests as incremental. The manuscript answers this with an empirical result that changes the interpretation (weak cross-family transfer; nulls reproducing improvement prevalence with larger gains), not by claiming new methods. The central message — a geographic proxy is not validated merely because it can be optimized — is kept as the headline.
