# HOSTILE PEER REVIEW — responses recorded before finalization

1. **"This is merely a taxi-density map."**
   Not fatal but the sharpest criticism. Response: the density layer is the input, not the claim. The contribution is (a) that relocation gains are large and robust for ~90-99% of origins, (b) the measured surplus over the naive nearest-major-road heuristic (+0.15 to +0.33 SD in 73-89% of origins at ≥200 m). Wording tightened: claims are about *relocation opportunity structure*, not the map itself.

2. **"The score does not represent vacant taxis."**
   Correct by design. The manuscript never claims vacant taxis; all language calibrated to "relative accessibility potential". Abstract and Limitations state this is uncalibrated — the Paper 2 boundary. Fatal only if a reader demands availability claims; mitigated by title and framing.

3. **"Walking to a major road explains everything."**
   Partially. The best reachable segment is a major road in 25-76% of origins, and no optimizer can beat "best major road in radius" (oracle). But the *naive* rule — nearest major road — underperforms by a mean 0.05-0.33 SD, and 24-75% of optimal picks are non-major segments at short radii. We report both the surplus over the naive rule AND the oracle bound (opt>bestmajor ≈ 0) honestly in Table `strategy_comparison.csv`.

4. **"The weights in the accessibility index are arbitrary."**
   The weights are transparent, untuned and standardized; the key robustness result is that conclusions hold across A/B/C and σ variants (ρ 0.85-0.99). A data-driven weighting is impossible in Paper 1 (no outcome to fit) — stated explicitly.

5. **"Synthetic/aggregated prior cannot support passenger-level claims."**
   The prior is real public data (not simulated): OSM + FY2023 station passengers + FY2023 published taxi-use profile. Claims are restricted to relative gradients — defensible. A real trajectory prior (Pseudo-PFLOW) is flagged as the top Paper 2/refinement input.

6. **"No real waiting-time validation exists."**
   True — and declared. The GO decision is conditional on calibrated claims. The manuscript is a feasibility study; Discussion dedicates a subsection to the validation design.

7. **"The result is Tokyo-specific."**
   Partially. Magnitudes are Tokyo-specific; the method is portable (needs only OSM + attractor data + aggregate temporal profile). Claim restricted accordingly; other cities may show weaker gradients.

8. **"The optimization objective has no empirically calibrated units."**
   Acknowledged: we report gains in SD units and gain-per-distance, deliberately avoiding conversion to minutes. Utility analysis presented as Pareto/rate statistics, not a calibrated cost function.

9. **"Novelty disappears against the taxi-trajectory literature."**
   T-Finder/PUDO literature recommends walkable pickups but *requires* fleet telemetry. Ours is the first (to our audit) that is simultaneously: no telemetry, segment-level, passenger-side, heuristic-benchmarked, and a dry feasibility framework. Each element alone is precedented; the conjunction is not. Desk-rejection risk assessed as moderate.

10. **"The tourism application is speculative."**
    Conceded and repositioned: visitors are an application case (Discussion 4.5), not the scientific population; no behavioral claims are made about them.

## Residual unresolved weaknesses
- The flow prior's spatial realism is untested against any independent taxi-flow observation (the single deepest gap; irreducible in a dry study).
- Weekend temporal structure is a modeled assumption, not data.
