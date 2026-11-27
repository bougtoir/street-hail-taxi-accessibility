#!/usr/bin/env python3
"""Writes ijgis_bib.json: T&F Reference Style V (Harvard) entries for the same
41 works as new_bib.json. Metadata corrected against Crossref records saved in
data/raw/crossref_ijgis (see IJGIS_REFERENCE_AUDIT.md)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda d: f" https://doi.org/{d}"
B = {
 "tfinder": ("Yuan et al.", 2013, "Yuan, N.J., Zheng, Y., Zhang, L., and Xie, X., 2013. T-Finder: a recommender system for finding passengers and vacant taxis. IEEE Transactions on Knowledge and Data Engineering, 25 (10), 2390–2403." + D("10.1109/TKDE.2012.153")),
 "yuan2011": ("Yuan et al.", 2011, "Yuan, J., Zheng, Y., Zhang, L., Xie, X., and Sun, G., 2011. Where to find my next passenger? In: Proceedings of the 13th International Conference on Ubiquitous Computing (UbiComp 2011), Beijing. New York: ACM, 109–118." + D("10.1145/2030112.2030128")),
 "zheng2010": ("Zheng et al.", 2011, "Zheng, Y., Liu, Y., Yuan, J., and Xie, X., 2011. Urban computing with taxicabs. In: Proceedings of the 13th International Conference on Ubiquitous Computing (UbiComp 2011), Beijing. New York: ACM, 89–98." + D("10.1145/2030112.2030126")),
 "yang2002": ("Yang and Wong", 2002, "Yang, H. and Wong, S.C., 2002. Demand–supply equilibrium of taxi services in a network under competition and regulation. Transportation Research Part B: Methodological, 36 (9), 799–819." + D("10.1016/S0191-2615(01)00031-5")),
 "wong2008": ("Wong et al.", 2005, "Wong, K.I., Wong, S.C., Bell, M.G.H., and Yang, H., 2005. Modeling the bilateral micro-searching behavior for urban taxi services using the absorbing Markov chain approach. Journal of Advanced Transportation, 39 (1), 81–104." + D("10.1002/atr.5670390107")),
 "hakusyo2025": ("Tokyo Hire-Taxi Association", 2025, "Tokyo Hire-Taxi Association, 2025. Tokyo no Taxi 2025 [online]. Tokyo: Tokyo Hire-Taxi Association. Available from: https://taxi-tokyo.or.jp/ [Accessed 29 September 2026]."),
 "taxi_demand": ("Moreira-Matias et al.", 2013, "Moreira-Matias, L., Gama, J., Ferreira, M., Mendes-Moreira, J., and Damas, L., 2013. Predicting taxi–passenger demand using streaming data. IEEE Transactions on Intelligent Transportation Systems, 14 (3), 1393–1402." + D("10.1109/TITS.2013.2262376")),
 "taxi_stand": ("Ocalir et al.", 2010, "Ocalir, E.V., Ercoskun, O.Y., and Tur, R., 2010. An integrated model of GIS and fuzzy logic (FMOTS) for location decisions of taxicab stands. Expert Systems with Applications, 37 (7), 4892–4901." + D("10.1016/j.eswa.2009.12.026")),
 "taxi_demand2": ("Hwang et al.", 2015, "Hwang, R.H., Hsueh, Y.L., and Chen, Y.T., 2015. An effective taxi recommender system based on a spatio-temporal factor analysis model. Information Sciences, 314, 200–211." + D("10.1016/j.ins.2015.03.047")),
 "yang2010": ("Yang et al.", 2010, "Yang, H., Leung, C.W.Y., Wong, S.C., and Bell, M.G.H., 2010. Equilibria of bilateral taxi–customer searching and meeting on networks. Transportation Research Part B: Methodological, 44 (8–9), 1067–1083." + D("10.1016/j.trb.2009.12.010")),
 "hansen1959": ("Hansen", 1959, "Hansen, W.G., 1959. How accessibility shapes land use. Journal of the American Institute of Planners, 25 (2), 73–76." + D("10.1080/01944365908978307")),
 "handy1997": ("Handy and Niemeier", 1997, "Handy, S.L. and Niemeier, D.A., 1997. Measuring accessibility: an exploration of issues and alternatives. Environment and Planning A, 29 (7), 1175–1194." + D("10.1068/a291175")),
 "geurs2004": ("Geurs and van Wee", 2004, "Geurs, K.T. and van Wee, B., 2004. Accessibility evaluation of land-use and transport strategies: review and research directions. Journal of Transport Geography, 12 (2), 127–140." + D("10.1016/j.jtrangeo.2003.10.005")),
 "kwan1998": ("Kwan", 1998, "Kwan, M.-P., 1998. Space-time and integral measures of individual accessibility: a comparative analysis using a point-based framework. Geographical Analysis, 30 (3), 191–216." + D("10.1111/j.1538-4632.1998.tb00396.x")),
 "miller1999": ("Miller", 1999, "Miller, H.J., 1999. Measuring space-time accessibility benefits within transportation networks: basic theory and computational procedures. Geographical Analysis, 31 (2), 187–212." + D("10.1111/j.1538-4632.1999.tb00976.x")),
 "shen1998": ("Shen", 1998, "Shen, Q., 1998. Location characteristics of inner-city neighborhoods and employment accessibility of low-wage workers. Environment and Planning B: Planning and Design, 25 (3), 345–365." + D("10.1068/b250345")),
 "mavoa2015": ("Mavoa et al.", 2012, "Mavoa, S., Witten, K., McCreanor, T., and O'Sullivan, D., 2012. GIS based destination accessibility via public transit and walking in Auckland, New Zealand. Journal of Transport Geography, 20 (1), 15–22." + D("10.1016/j.jtrangeo.2011.10.001")),
 "freudenberg2003": ("Freudenberg", 2003, "Freudenberg, M., 2003. Composite indicators of country performance: a critical assessment. OECD Science, Technology and Industry Working Papers 2003/16. Paris: OECD Publishing." + D("10.1787/405566708255")),
 "oecd2008": ("OECD/JRC", 2008, "OECD/JRC, 2008. Handbook on constructing composite indicators: methodology and user guide. Paris: OECD Publishing." + D("10.1787/9789264043466-en")),
 "saltelli2008": ("Saltelli et al.", 2008, "Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., and Tarantola, S., 2008. Global sensitivity analysis: the primer. Chichester: Wiley." + D("10.1002/9780470725184")),
 "greco2019": ("Greco et al.", 2019, "Greco, S., Ishizaka, A., Tasiou, M., and Torrisi, G., 2019. On the methodological framework of composite indices: a review of the issues of weighting, aggregation, and robustness. Social Indicators Research, 141 (1), 61–94." + D("10.1007/s11205-017-1832-9")),
 "fotheringham1991": ("Fotheringham and Wong", 1991, "Fotheringham, A.S. and Wong, D.W.S., 1991. The modifiable areal unit problem in multivariate statistical analysis. Environment and Planning A, 23 (7), 1025–1044." + D("10.1068/a231025")),
 "jelinski1996": ("Jelinski and Wu", 1996, "Jelinski, D.E. and Wu, J., 1996. The modifiable areal unit problem and implications for landscape ecology. Landscape Ecology, 11 (3), 129–140." + D("10.1007/BF02447512")),
 "openshaw1984": ("Openshaw", 1984, "Openshaw, S., 1984. The modifiable areal unit problem. Concepts and Techniques in Modern Geography 38. Norwich: Geo Books."),
 "longley2015": ("Longley et al.", 2015, "Longley, P.A., Goodchild, M.F., Maguire, D.J., and Rhind, D.W., 2015. Geographic information science and systems. 4th ed. Hoboken, NJ: Wiley."),
 "moran1950": ("Moran", 1950, "Moran, P.A.P., 1950. Notes on continuous stochastic phenomena. Biometrika, 37 (1–2), 17–23." + D("10.2307/2332142")),
 "getis1992": ("Getis and Ord", 1992, "Getis, A. and Ord, J.K., 1992. The analysis of spatial association by use of distance statistics. Geographical Analysis, 24 (3), 189–206." + D("10.1111/j.1538-4632.1992.tb00261.x")),
 "anselin1995": ("Anselin", 1995, "Anselin, L., 1995. Local indicators of spatial association – LISA. Geographical Analysis, 27 (2), 93–115." + D("10.1111/j.1538-4632.1995.tb00338.x")),
 "besag1977": ("Besag and Diggle", 1977, "Besag, J. and Diggle, P.J., 1977. Simple Monte Carlo tests for spatial pattern. Applied Statistics, 26 (3), 327–333." + D("10.2307/2346974")),
 "manly2007": ("Manly", 2007, "Manly, B.F.J., 2007. Randomization, bootstrap and Monte Carlo methods in biology. 3rd ed. Boca Raton, FL: Chapman & Hall/CRC." + D("10.1201/9781315273075")),
 "steegen2016": ("Steegen et al.", 2016, "Steegen, S., Tuerlinckx, F., Gelman, A., and Vanpaemel, W., 2016. Increasing transparency through a multiverse analysis. Perspectives on Psychological Science, 11 (5), 702–712." + D("10.1177/1745691616658637")),
 "simonsohn2020": ("Simonsohn et al.", 2020, "Simonsohn, U., Simmons, J.P., and Nelson, L.D., 2020. Specification curve analysis. Nature Human Behaviour, 4 (11), 1208–1214." + D("10.1038/s41562-020-0912-z")),
 "simmons2011": ("Simmons et al.", 2011, "Simmons, J.P., Nelson, L.D., and Simonsohn, U., 2011. False-positive psychology: undisclosed flexibility in data collection and analysis allows presenting anything as significant. Psychological Science, 22 (11), 1359–1366." + D("10.1177/0956797611417632")),
 "gelman2014": ("Gelman and Loken", 2013, "Gelman, A. and Loken, E., 2013. The garden of forking paths: why multiple comparisons can be a problem, even when there is no 'fishing expedition' or 'p-hacking' and the research hypothesis was posited ahead of time [online]. New York: Department of Statistics, Columbia University. Available from: https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf [Accessed 10 November 2026]."),
 "kuby2009": ("Kuby and Lim", 2005, "Kuby, M. and Lim, S., 2005. The flow-refueling location problem for alternative-fuel vehicles. Socio-Economic Planning Sciences, 39 (2), 125–145." + D("10.1016/j.seps.2004.03.001")),
 "kuby2009b": ("Kuby and Lim", 2007, "Kuby, M. and Lim, S., 2007. Location of alternative-fuel stations using the flow-refueling location model and dispersion of candidate sites on arcs. Networks and Spatial Economics, 7 (2), 129–152." + D("10.1007/s11067-006-9003-6")),
 "he2013": ("He et al.", 2013, "He, F., Wu, D., Yin, Y., and Guan, Y., 2013. Optimal deployment of public charging stations for plug-in hybrid electric vehicles. Transportation Research Part B: Methodological, 47, 87–101." + D("10.1016/j.trb.2012.09.007")),
 "nicholas2004": ("Melendez and Milbrandt", 2008, "Melendez, M. and Milbrandt, A., 2008. Regional consumer hydrogen demand and optimal hydrogen refueling station siting. Technical Report NREL/TP-540-42224. Golden, CO: National Renewable Energy Laboratory." + D("10.2172/928253")),
 "osm": ("OpenStreetMap contributors", 2026, "OpenStreetMap contributors, 2026. OpenStreetMap planet data and Overpass API [online]. Licensed under ODbL. Available from: https://www.openstreetmap.org [Accessed 29 September 2026, via OSMnx 2.0.7]."),
 "nlni": ("MLIT", 2023, "MLIT (Ministry of Land, Infrastructure, Transport and Tourism, Japan), 2023. National Land Numerical Information: railway data (N02), FY2023 [dataset]. Available from: https://nlftp.mlit.go.jp/ksj/ [Accessed 29 September 2026]."),
 "monitor": ("Tokyo Taxi Center", 2024, "Tokyo Taxi Center, 2024. Taxi user monitor survey: FY2023 tabulation report [online]. Tokyo: Tokyo Taxi Center. Available from: https://www.tokyo-tc.or.jp/center/uploads/monitor_2024.pdf [Accessed 29 September 2026]."),
 "goodchild1992": ("Goodchild", 1992, "Goodchild, M.F., 1992. Geographical information science. International Journal of Geographical Information Systems, 6 (1), 31–45." + D("10.1080/02693799208901893")),
 "heuvelink1989": ("Heuvelink et al.", 1989, "Heuvelink, G.B.M., Burrough, P.A., and Stein, A., 1989. Propagation of errors in spatial modelling with GIS. International Journal of Geographical Information Systems, 3 (4), 303–322." + D("10.1080/02693798908941518")),
 "kedron2021": ("Kedron et al.", 2021, "Kedron, P., Li, W., Fotheringham, S., and Goodchild, M., 2021. Reproducibility and replicability: opportunities and challenges for geospatial research. International Journal of Geographical Information Science, 35 (3), 427–445." + D("10.1080/13658816.2020.1802032")),
}
if __name__ == "__main__":
    old = json.load(open(f"{ROOT}/analysis/new_bib.json"))
    NEW = {"goodchild1992", "heuvelink1989", "kedron2021"}
    assert set(old) | NEW == set(B), (set(old) | NEW) ^ set(B)
    assert len({(c, y) for c, y, _ in B.values()}) == len(B), "author-year collision"
    out = {k: {"cite": c, "year": y, "ref": r} for k, (c, y, r) in B.items()}
    json.dump(out, open(f"{ROOT}/analysis/ijgis_bib.json", "w"), ensure_ascii=False, indent=1)
    print(len(out), "entries")
