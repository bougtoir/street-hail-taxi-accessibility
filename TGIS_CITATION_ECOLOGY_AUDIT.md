# TGIS citation-ecology audit (starting bibliography: 44 items)

Purpose: check whether the existing bibliography supports a Transactions in GIS framing (spatial data quality/uncertainty, geocomputation, spatial optimization, spatial networks, spatial decision support) without citation gaming. Crossref responses: `data/raw/crossref_tgis/` (ledger with SHA-256).

## Classification of the 44 existing references (citation key as rendered in APA 7)

| Category | Items | n |
|---|---|---|
| Spatial sciences / GIS | Goodchild 1992; Longley et al. 2015 | 2 |
| Spatial data quality / uncertainty | Heuvelink et al. 1989; Openshaw 1984; Fotheringham & Wong 1991; Jelinski & Wu 1996 | 4 |
| Spatial analysis / reproducibility | Kedron et al. 2021 | 1 |
| Spatial statistics / autocorrelation / null models | Moran 1950; Getis & Ord 1992; Anselin 1995; Besag & Diggle 1977; Manly 2007 | 5 |
| Spatial networks / taxi network models | Yang & Wong 2002; Wong et al. 2005; Yang et al. 2010 | 3 |
| Accessibility | Hansen 1959; Handy & Niemeier 1997; Geurs & van Wee 2004; Kwan 1998; Miller 1999; Shen 1998; Mavoa et al. 2012 | 7 |
| Decision support / composite indicators | Freudenberg 2003; OECD/JRC 2008; Saltelli et al. 2008; Greco et al. 2019 | 4 |
| Taxi / transport data mining | J. Yuan et al. 2011; N. J. Yuan et al. 2013; Zheng et al. 2011; Moreira-Matias et al. 2013; Ocalir et al. 2010; Hwang et al. 2015; Tokyo Hire-Taxi Association 2025 | 7 |
| Robustness / specification | Steegen et al. 2016; Simonsohn et al. 2020; Simmons et al. 2011; Gelman & Loken 2013 | 4 |
| Prospective infrastructure siting | Kuby & Lim 2005, 2007; He et al. 2013; Melendez & Milbrandt 2008 | 4 |
| Data sources | OpenStreetMap contributors 2026; MLIT 2023; Tokyo Taxi Center 2024 | 3 |
| **Total** | | **44** |

## Gaps relative to the TGIS framing

1. Representation uncertainty as part of geographic knowledge/spatial data quality: only the 1980s–90s MAUP and error-propagation sources; no source for representation (not just measurement) uncertainty or for the spatial data quality research programme.
2. Uncertainty in optimization-based spatial decision support: the argument that an optimum inherits its construction has no SDSS-optimization source.
3. Sensitivity of accessibility results to network/location encoding: claimed in the Introduction, supported only by MAUP and composite-indicator sources.
4. Spatial optimization in contemporary GIS workflows: no source.
5. No Transactions in GIS paper (not itself a reason to add one).

## Candidates (Crossref-verified; KEEP only if a precise existing claim needs support)

| Full citation | DOI | Journal | Precise claim supported | Location | Decision | Reason |
|---|---|---|---|---|---|---|
| Aerts, J. C. J. H., Goodchild, M. F., & Heuvelink, G. B. M. (2003). Accounting for spatial uncertainty in optimization with spatial decision support systems. 7(2), 211–230 | 10.1111/1467-9671.00141 | Transactions in GIS | Input uncertainty propagates into solutions of SDSS optimization models | Introduction ¶ on SDQ; §4.6 | KEEP | Gap 2; directly about optimization under spatial uncertainty |
| Couclelis, H. (2003). The certainty of uncertainty: GIS and the limits of geographic knowledge. 7(2), 165–175 | 10.1111/1467-9671.00138 | Transactions in GIS | Uncertainty arises from representational choices, not only measurement error | Introduction ¶ on SDQ | KEEP | Gap 1 |
| Devillers, R., Stein, A., Bédard, Y., Chrisman, N., Fisher, P., & Shi, W. (2010). Thirty years of research on spatial data quality. 14(4), 387–400 | 10.1111/j.1467-9671.2010.01212.x | Transactions in GIS | Spatial data quality as an established research tradition including fitness for use | Introduction ¶ on SDQ | KEEP | Gap 1 |
| Kim, J., & Horner, M. W. (2024). Assessing the effects of centroid assignment methods on measuring spatial accessibility. 28(7), 2025–2043 | 10.1111/tgis.13228 | Transactions in GIS | Location encoding changes accessibility results | Introduction ¶ on SDQ | KEEP | Gap 3 |
| Almusidi, M. (2025). Interchangeable or inconsistent? A comparative analysis of web routing services for pedestrian accessibility. 29(8), e70179 | 10.1111/tgis.70179 | Transactions in GIS | Network/routing representation changes pedestrian accessibility results | Introduction ¶ on SDQ | KEEP | Gap 3; pedestrian network case matches walking-radius design |
| Murray, A. T., & Baik, J. (2023). Opensource spatial optimization in GIScience for strategic positioning. 27(3), 646–662 | 10.1111/tgis.13033 | Transactions in GIS | Spatial optimization is embedded in GIS-based planning workflows | Introduction ¶ on SDQ | KEEP | Gap 4 |
| Miller, J. A. (2015). Towards a better understanding of dynamic interaction metrics for wildlife: a null model approach | 10.1111/tgis.12149 | Transactions in GIS | Null models in movement analysis | — | REJECT | Null-model point already supported by Besag & Diggle and Manly; domain unrelated |
| Ostermann, F. O., & Granell, C. (2017). Advancing science with VGI: reproducibility and replicability | 10.1111/tgis.12195 | Transactions in GIS | Reproducibility of VGI studies | — | REJECT | Kedron et al. 2021 already supports the reproducibility sentence |
| Chen, Gong, & Xie (2017). An analysis of movement patterns between zones using taxi GPS data | 10.1111/tgis.12281 | Transactions in GIS | Taxi GPS analysis | — | REJECT | Study does not use GPS data; no sentence needs it |
| Cao, K., & Huang, B. (2019). Spatial optimization for land use planning | 10.1111/tgis.12573 | Transactions in GIS | Spatial optimization in planning | — | REJECT | Redundant with Murray & Baik 2023 |
| Wu et al. (2022). Spatio-temporal neural network for taxi demand prediction | 10.1111/tgis.12943 | Transactions in GIS | Taxi demand prediction with labels | — | REJECT | Labelled prediction is outside the no-label scope; would invite unsupported comparison |
| Huang (2026). Beyond weak replicability: conditional generalization | 10.1111/tgis.70285 | Transactions in GIS | Replicability/generalization | — | REJECT | Very recent; claim already supported by Kedron et al. 2021 |

Result: 6 KEEP (all TGIS), 6 REJECT. One repository citation (Onishi, 2026; the public code/data repository) added for the Data Availability Statement as data citation required by the journal.
