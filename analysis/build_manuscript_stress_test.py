#!/usr/bin/env python3
"""Stress-test reframing: CEUS_STRESS_TEST_MAIN_inline.docx, cover letter,
highlights, submission zip. Reuses frozen analysis tables."""
import os, json, zipfile
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAB, FIG, OUT = (f"{ROOT}/{d}" for d in ["tables", "figures", "output"])

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from lxml import etree as ET

M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
def m_el(t): return ET.Element(f"{{{M_NS}}}{t}")
def m_run(t):
    r = m_el("r"); tt = m_el("t"); tt.text = str(t); r.append(tt); return r
def m_sub(b, s):
    e = m_el("sSub"); be = m_el("e"); se = m_el("sub")
    be.append(m_run(b)); se.append(m_run(s)); e.extend([be, se]); return e
def add_omml(p, els):
    om = m_el("oMath")
    for e in els: om.append(e if not isinstance(e, str) else m_run(e))
    p._p.append(om); return p

abl = pd.read_csv(f"{TAB}/ablation_summary_clustered.csv")
ts = pd.read_csv(f"{TAB}/transfer_summary.csv")
perm = json.load(open(f"{TAB}/permutation_null.json"))
sigma = json.load(open(f"{TAB}/sigma_sensitivity.json"))
nullarr = np.load(f"{ROOT}/data/processed/perm_null_arrays.npz")

def ab(spec, r, c): return abl[(abl.spec == spec) & (abl.radius == r)][c].iloc[0]
def tf(a, b, c): return ts[(ts.selector == a) & (ts.evaluator == b) & (ts.radius == 300)][c].iloc[0]
def pc(x): return f"{100*x:.0f}%"
def f2(x): return f"{x:.2f}"
def ci(x): return eval(x) if isinstance(x, str) else x
po = perm["weekday_17"]["obs"]; pn = perm["weekday_17"]["null_mean"]

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(11)
def H(t, l=1): doc.add_heading(t, level=l)
def P(t):
    p = doc.add_paragraph(); p.add_run(t); return p
def EQ(els):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; add_omml(p, els)
def FIGURE(name, cap, w=6.0):
    doc.add_picture(f"{FIG}/{name}.png", width=Inches(w))
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(cap).italic = True

REFS = []
def cite(*ids):
    for r in ids:
        if r not in REFS: REFS.append(r)
    return "[" + ",".join(str(REFS.index(r) + 1) for r in ids) + "]"

tp = doc.add_paragraph(); tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
tr = tp.add_run("Stress-testing public-data urban accessibility proxies: "
                "street-hail taxi relocation without fleet telemetry")
tr.bold = True; tr.font.size = Pt(16)

H("Abstract")
P("Many urban-computing studies optimize constructed spatial proxies — "
  "accessibility indices, amenity scores, availability surfaces — where "
  "direct operational ground truth is unavailable. Because a heterogeneous "
  "surface contains local maxima, optimizing a proxy under its own score "
  "mechanically produces apparent gains, and self-optimization is not "
  "external validation. Using street-hail taxi relocation as a motivating "
  "case study, we construct four public-data-derived opportunity surfaces "
  "on the directed road network of Tokyo's five central wards (27,887 "
  "segments) and audit relocation optimization over 2,000 origins at "
  "100-500 m walking radii through component ablation, cross-specification "
  "transfer, a simple road-hierarchy heuristic, and 500-permutation spatial "
  "nulls with origin-clustered inference. Apparent gains are large "
  f"({pc(ab('COMB',300,'frac_pos'))} of origins improved, mean "
  f"{f2(ab('COMB',300,'mean_G'))} SD at 300 m) and exceed the nearest-major-"
  f"road heuristic in {pc(ab('COMB',300,'gt_nearmaj'))} of origins, but "
  "cross-specification transfer between conceptually distinct component "
  "families is weak (53% and 44% of origins positive), and spatially "
  "permuted surfaces reproduced improvement prevalence almost fully, with "
  "only a small observed advantage at some walking radii (empirical "
  "p=0.02-0.09, below 0.05 only at 200 m), while producing larger mean "
  "gain magnitudes than the observed surface. Large within-score "
  "optimization gains therefore did "
  "not translate into equally strong cross-specification evidence and were "
  "partly reproducible under spatial nulls: self-optimization alone is "
  "insufficient validation of a constructed urban spatial proxy. We "
  "therefore propose cross-specification transfer, component ablation, "
  "spatial-null comparison, and simple heuristic benchmarking as "
  "complementary internal stress tests when external outcome labels are "
  "unavailable.")
P("Keywords: urban accessibility; geocomputation; spatial optimization; "
  "mobility proxy; permutation test; public urban data")

H("1. Introduction")
P("Urban planning and mobility research increasingly relies on constructed "
  "spatial proxies — accessibility indices, amenity opportunity scores, "
  "pedestrian safety surfaces, micromobility availability proxies, "
  "EV-charging and service-location maps — because direct operational "
  "measurements are proprietary, expensive, or unavailable. These surfaces "
  "are then optimized: choose the best location, the highest-accessibility "
  "node, the highest-opportunity zone.")
P("A methodological problem follows. The same score defines both what "
  "'better' means and which candidate is selected, so a large apparent gain "
  "can arise mechanically from score heterogeneity, candidate-set size, and "
  "order statistics rather than from meaningful urban structure. Studies "
  "often report the internal gain without testing whether the selected "
  "location transfers to an alternative plausible specification, whether "
  "the gain exceeds what a spatially permuted surface would yield, or "
  "whether a simple heuristic explains most of it.")
P("Street-hail taxi relocation is an ideal case study: the operational "
  "telemetry that could measure vacant-taxi opportunity is proprietary "
  "(systems like T-Finder " + cite("tfinder") + " require fleet "
  "trajectories), the passenger decision is spatial, public-data proxies "
  "are tempting, and walking defines a natural local optimization problem "
  + cite("yang2010") + ". Prior taxi-demand " + cite("taxi_demand") +
  " and recommendation work " + cite("taxi_demand2", "taxi_stand") +
  " likewise presumes observed demand; pickup-point assignment in "
  "ride-sharing " + cite("pudo") + " assumes known trip requests.")
P("The contribution is methodological. The paper makes five related "
  "contributions: (1) it formalizes the distinction between within-proxy "
  "optimization gain and evidence of transferable spatial structure — "
  "a location selected under score A may have a higher value under score "
  "A (apparent optimization gain), may or may not improve a distinct "
  "plausible score B (transferable internal structure), and neither is "
  "evidence of a real-world outcome (external validity); (2) it "
  "operationalizes cross-specification transfer as an internal validity "
  "stress test; (3) it uses spatial permutation nulls to quantify how "
  "much apparent gain can arise from a heterogeneous surface without "
  "meaningful observed spatial organization; (4) it combines ablation, "
  "transfer, null comparison, and simple heuristic benchmarking into a "
  "practical stress-test framework; and (5) it demonstrates the framework "
  "on street-hail taxi relocation where no proprietary fleet telemetry "
  "exists. The workflow is falsification-oriented: construct a proxy, "
  "optimize it, observe the apparent gain, then attempt to falsify the "
  "naive interpretation — optimization success is treated as a hypothesis "
  "to be challenged, not as validation by itself. These tests are "
  "internal checks, not universally sufficient validation criteria.")

H("1.1 Research questions", 2)
P("RQ1: How large are apparent relocation gains under self-optimization? "
  "RQ2: Do gains persist across alternative component specifications? "
  "RQ3: Do locations selected under one specification improve another "
  "specification's score? RQ4: Do observed gains exceed those of spatially "
  "permuted surfaces with identical marginals? RQ5: How much of the gain "
  "does the nearest-major-road heuristic explain?")

H("2. Materials and Methods")
H("2.1 Study area and case-study rationale", 2)
P("Five contiguous central wards of Tokyo (Chiyoda, Chuo, Minato, Shinjuku, "
  "Shibuya) — a canonical street-hail environment " + cite("hakusyo2025") +
  " where fleet telemetry is inaccessible.")
H("2.2 Public urban data", 2)
P("OpenStreetMap road network and POIs via Overpass " + cite("osm") + "; "
  "FY2023 railway-station locations (MLIT NLNI N02) " + cite("nlni") + "; "
  "hourly taxi-use distribution from the Tokyo Taxi Center monitor survey "
  + cite("monitor") + ". The restricted CSIS Pseudo-PFLOW product was "
  "inaccessible and substituted. The FY2023 N02 schema contains no "
  "passenger-count field, so the station term is an unweighted location "
  "kernel (documented correction).")
H("2.3 Directed road-network representation", 2)
P("27,887 hail-feasible directed segments from the OSM drive graph; "
  "182,538-edge walk graph for pedestrian distances (equirectangular metric).")
H("2.4 Alternative opportunity proxies", 2)
P("A circulation-potential proxy combines road-class weight, a Gaussian "
  "attractor kernel field D(e) (sigma=300 m), and a period multiplier from "
  "the monitor profile blended toward nightlife contexts:")
EQ([m_sub("P", "circ"), m_run("(e,t) = w_road(e)·(0.3 + D(e))·P(h;ctx(e))")])
P("Four z-standardized specifications: road-only (hierarchy, degree, "
  "lanes); attractor-only (station, nightlife, hotel/hospital, transit, "
  "taxi-stand kernels); the circulation proxy; and a combined score "
  "S_COMB = z(z log(1+P_circ) + 0.5 S_road + 0.4 C_ctx). All are modeled "
  "public-data proxies — none is observed taxi availability.")
H("2.5 Local pedestrian relocation optimization", 2)
P("2,000 origins (seed 42); candidates are segments reachable within "
  "100/200/300/500 m walking distance; the selected location maximizes the "
  "score over candidates.")
H("2.6 The self-optimization problem", 2)
P("If S_A(x) is the opportunity score and x*_A = argmax over the "
  "neighborhood N(x0), then")
EQ([m_sub("S", "A"), m_run("(x*"), m_sub("", "A"), m_run(") − "),
    m_sub("S", "A"), m_run("(x0) ≥ 0")])
P("holds by construction whenever a better-scoring candidate exists in "
  "N(x0). Positive self-gain is therefore partly structural and cannot "
  "alone validate the proxy — the central premise of this audit.")
H("2.7 Component ablation", 2)
P("Each specification is optimized separately to test whether apparent "
  "gains depend on one construction.")
H("2.8 Cross-specification transfer", 2)
P("Transfer gain TG(A→B) = S_B(x*_A) − S_B(x0) evaluates locations selected "
  "under specification A under a distinct specification B. Off-diagonal "
  "transfer — especially between the road-only and attractor-only component "
  "families — is the internal validity test; diagonal terms are "
  "self-optimization.")
H("2.9 Spatial permutation null", 2)
P("Scores are permuted across all hail-feasible segments (500 repetitions), "
  "preserving the marginal distribution, network geometry, origin "
  "distribution, and candidate counts. Observed improvement fractions and "
  "gain magnitudes are compared against the null; empirical "
  "p = (1 + #{null ≥ obs})/(1 + N).")
H("2.10 Constrained permutation sensitivity", 2)
P("A within-ward permutation preserves coarse geographic structure and "
  "tests whether fine-scale organization remains non-random.")
H("2.11 Heuristic comparators", 2)
P("Stay; random relocation (10 seeded draws); nearest major-class road.")
H("2.12 Cluster-aware statistical inference", 2)
P("Origin-period rows are repeated measurements. Period-invariant "
  "specifications use unique origins (n = 1,961-1,999); period-varying "
  "specifications use an origin-clustered bootstrap (5,000 replicates) and "
  "paired tests on origin-mean differences. Effects, CIs, and p-values are "
  "reported together.")
H("2.13 Reproducibility", 2)
P("Fixed seeds, raw-data snapshots with a SHA-256 ledger, code and "
  "machine-readable tables provided.")

H("3. Results")
H("3.1 Opportunity surfaces and local heterogeneity", 2)
P("All four surfaces are strongly heterogeneous, with ridges along "
  "arterials and station fronts (Figure 2).")
FIGURE("fig2_map", "Figure 2. Modeled street-hail opportunity surface "
       "(combined specification, SD units), weekday 17:00 and weekend 23:00.")
H("3.2 Apparent gains under self-optimization", 2)
P(f"Self-optimization produces large apparent gains (RQ1): "
  f"{pc(ab('COMB',100,'frac_pos'))}-{pc(ab('COMB',500,'frac_pos'))} of "
  "origins have a higher-scoring segment within reach, mean gain "
  f"{f2(ab('COMB',100,'mean_G'))}-{f2(ab('COMB',500,'mean_G'))} SD "
  "(Figure 4). These gains are partly structural by construction.")
FIGURE("fig4_gain_by_radius", "Figure 4. Apparent self-optimization gains "
       "(SD units) by walking radius, combined specification.")
H("3.3 Comparison with simple heuristics", 2)
P(f"Against heuristics (RQ5): the combined optimum beats random relocation "
  f"in ~{pc(ab('COMB',300,'gt_rand'))} of origins and the nearest major "
  "These values establish the magnitude of apparent within-score gain, "
  "not external validity. The optimum beats the nearest major "
  f"road in {pc(ab('COMB',300,'gt_nearmaj'))} at 300 m (paired surplus "
  f"{f2(ab('COMB',300,'diff_nearmaj'))} SD, clustered 95% CI "
  f"{ci(abl[(abl.spec=='COMB')&(abl.radius==300)].diff_nearmaj_ci.iloc[0])}, "
  "Wilcoxon p<0.001). This shows the constructed score contains spatial "
  "information beyond road hierarchy alone — it does not show the selected "
  "location is better for obtaining a real taxi (Figure 5).")
FIGURE("fig5_strategies", "Figure 5. Mean modeled score by strategy "
       "(combined specification, radii pooled). Error bars = SEM.")
H("3.4 Component ablation", 2)
P(f"Apparent gains persist under every construction (RQ2): at 300 m, "
  f"road-only {pc(ab('ROAD',300,'frac_pos'))}, attractor-only "
  f"{pc(ab('ATTR',300,'frac_pos'))}, proxy {pc(ab('PROXY',300,'frac_pos'))}, "
  f"combined {pc(ab('COMB',300,'frac_pos'))} improved (Figure 7). Segment "
  "rankings agree only moderately to strongly (Spearman 0.52-0.93): the "
  "constructions are alternative readings with varying degrees of "
  "agreement, and persistence is not proof of external validity.")
FIGURE("fig7_ablation", "Figure 7. Component ablation across walking radii.")
H("3.5 Cross-specification transfer", 2)
P(f"Transfer between conceptually distinct component families is weak "
  f"(RQ3): road-selected locations improve the attractor score for "
  f"{pc(tf('ROAD','ATTR','frac_pos'))} of origins (mean "
  f"{f2(tf('ROAD','ATTR','mean_TG'))} SD) and attractor-selected locations "
  f"improve the road score for {pc(tf('ATTR','ROAD','frac_pos'))} "
  f"({f2(tf('ATTR','ROAD','mean_TG'))} SD) — near-chance fractions. "
  f"Transfer into the proxy is stronger (attr→proxy "
  f"{pc(tf('ATTR','PROXY','frac_pos'))}; road→proxy "
  f"{pc(tf('ROAD','PROXY','frac_pos'))}) because the proxy embeds road "
  "hierarchy (Figure 8, Table 4). Weak off-diagonal transfer is itself a "
  "key finding: the constructions partly identify different, non-"
  "transferable structure.")
FIGURE("fig8_transfer_matrix", "Figure 8. Transfer matrix at 300 m. "
       "Diagonal would be self-optimization; off-diagonal entries are "
       "internal transfer evidence.")
H("3.6 Spatial permutation null", 2)
P(f"Against the unrestricted null (RQ4): improvement prevalence marginally "
  f"exceeds permutation at 200-500 m (observed {po['300'][0]:.3f} vs null "
  f"{pn['300'][0]:.3f} at 300 m; empirical p=0.02-0.09) but not at 100 m "
  f"(p=1.0). Mean gain magnitude does not exceed the null at any radius "
  f"(observed {po['300'][1]:.2f} vs null {pn['300'][1]:.2f} SD at 300 m; "
  "Figure 9, Table 5). A spatially unstructured surface with identical "
  "marginals produces larger local contrasts: most of the apparent gain is "
  "generic maximum-selection, while the observed surface's spatial "
  "autocorrelation actually compresses local maxima.")
FIGURE("fig9_permutation_null", "Figure 9. Observed statistics (red) vs "
       "500-permutation null (gray), 300 m, weekday 17:00.")
H("3.7 Constrained-null sensitivity", 2)
P("The within-ward null reproduces the same pattern (marginal prevalence "
  "advantage at 200-500 m; lower observed magnitude), so coarse district "
  "structure does not rescue the gain-magnitude claim.")
H("3.8 Temporal and district secondary analyses", 2)
P("Under the modeled temporal specifications, gains are largest in the "
  "weekday-morning period; the weekend specification shifts modeled "
  "opportunity toward nightlife contexts — input-profile consequences "
  "(Figure 6). Kernel bandwidth 150/500 m leaves gains nearly unchanged "
  f"(rho {sigma['rho_150']:.2f}/{sigma['rho_500']:.2f}).")
FIGURE("fig6_heterogeneity", "Figure 6. Modeled gain by hour/day-type and "
       "ward/radius — model behavior, not observed patterns.")
H("3.9 Summary of evidence levels", 2)
P("Level 1 (self-optimization): large apparent gains — achieved. Level 2 "
  "(internal stress tests): ablation passed; transfer weak; heuristic "
  "contrast retained; permutation shows prevalence marginally above but "
  "magnitude below null. Level 3 (external empirical validation): not "
  "available in this study.")
FIGURE("fig1_framework", "Figure 1. Stress-test workflow: proxy "
       "construction, self-optimization, transfer test, spatial null test.")
FIGURE("fig3_worked_example", "Figure 3. Local optimization example "
       "(200 m, weekday 17:00): apparent gain under the combined score.")

H("4. Discussion")
H("4.1 Large apparent gains do not establish proxy validity", 2)
P("The self-optimization inequality is structural: with ~hundreds of "
  "reachable candidates, a local maximum almost surely exceeds the origin. "
  "The practical lesson is not that gains exist — it is that their size "
  "carries almost no validating information.")
H("4.2 Cross-specification transfer reveals limited robustness", 2)
P("Positive but near-chance transfer between road-only and attractor-only "
  "selections means the two component families partly identify different "
  "places: an improvement under one plausible public-data reading of "
  "'opportunity' is roughly a coin flip under the other. Any deployed "
  "proxy would inherit this specification dependence.")
H("4.3 Spatial permutation shows the role of generic heterogeneity", 2)
P("The decisive result: a shuffled surface reproduces ~98% of the "
  "improvement prevalence and produced larger mean gain magnitudes across "
  "the examined radii. What the "
  "real urban surface contributes is a marginal reliability edge — not "
  "bigger wins. Interpreted honestly, this means the constructed proxy's "
  "fine-scale spatial arrangement adds little beyond generic "
  "heterogeneity for relocation purposes.")
H("4.4 What the nearest-major-road comparison does and does not show", 2)
P("The combined optimum's surplus over the nearest major road shows the "
  "score encodes information beyond hierarchy — a real, if narrow, "
  "computational finding. It says nothing about real taxi encounters.")
H("4.5 From optimization gain to proxy validity", 2)
P("Optimization of a heterogeneous spatial score will tend to locate a "
  "nearby value higher than the starting location: within-score gain is "
  "partly an order-statistical property of the constructed surface, not "
  "evidence about the world. Cross-specification transfer asks a stronger "
  "question — does the selected location remain preferable under another "
  "plausible information structure? Spatial permutation asks another — "
  "does the observed spatial organization yield gains beyond those of "
  "heterogeneous values arranged under a null spatial structure? Here, "
  "weak and asymmetric transfer plus strong null performance show why "
  "the large self-gains should not be interpreted naively: the main "
  "scientific result is not that the taxi relocation proxy succeeded "
  "operationally, but that apparently persuasive optimization gains can "
  "survive despite limited evidence of transferable spatial structure. "
  "This circular validation risk — the score used to select an optimum "
  "is also the score used to declare it successful — applies to a class "
  "of constructed surfaces (accessibility indices, opportunity and "
  "amenity scores, mobility-availability and service-location indices) "
  "that share the same inferential structure; these are problem classes, "
  "not empirically tested applications.")
H("4.6 A practical proxy-auditing framework", 2)
P("A compact internal stress-test workflow follows from the results: "
  "(1) CONSTRUCT one or more plausible proxy surfaces; (2) OPTIMIZE "
  "candidate locations; (3) ABLATE components to test specification "
  "dependence; (4) TRANSFER selected locations across alternative "
  "specifications; (5) NULL-TEST against spatially permuted or otherwise "
  "structured nulls; (6) BENCHMARK against simple domain heuristics; "
  "(7) CALIBRATE claims to the evidence level that survives. This is an "
  "internal, falsification-oriented audit — not a universal standard.")
H("4.7 Implications for prospective infrastructure siting", 2)
P("The problem examined here extends beyond mobility settings in which "
  "operational data are proprietary. Similar inferential constraints arise "
  "when infrastructure is prospective and historical outcome labels do not "
  "yet exist — for example, early-stage hydrogen-refueling or emerging "
  "charging-network siting. Planners may then optimize constructed demand "
  "or accessibility proxies with no observations of realized use. Our "
  "results caution that large within-proxy optimization gains should not "
  "by themselves be interpreted as evidence of meaningful siting "
  "advantage; ablation, transfer, spatial-null comparison, and simple "
  "heuristic benchmarks provide practical internal stress tests until "
  "external validation becomes possible.")
H("4.8 Street-hail taxis as motivating case", 2)
P("The paper is not an operational validation of a taxi recommendation "
  "system. The street-hail case was chosen because it makes the proxy-"
  "optimization problem concrete: no ground truth, a spatial passenger "
  "decision, and tempting public data. Low-friction street-hail "
  "information could also matter for visitors unfamiliar with local "
  "hailing conventions — a motivation, not a tested claim.")
H("4.9 Limitations", 2)
P("No observed vacant-taxi ground truth; scores are uncalibrated public-"
  "data proxies; temporal structure is partly assumed; Tokyo specificity; "
  "roadside hail feasibility imperfectly represented; station term is "
  "unweighted (FY2023 N02 lacks passenger counts); transfer and null tests "
  "are internal checks, not empirical validation.")
H("4.10 Requirements for external empirical validation", 2)
P("Before any operational interpretation, external evidence would require "
  "observed vacant-taxi passage, actual waiting times, or prospective "
  "passenger outcomes.")

H("5. Conclusion")
P("Optimization performance and proxy validity are not equivalent. "
  "Large within-score optimization gains did not translate into equally "
  "strong cross-specification evidence and were partly reproducible under "
  "spatially permuted null surfaces. Self-optimization alone is "
  "insufficient validation of a constructed urban opportunity proxy; "
  "ablation, transfer, and spatial-null tests form a minimal internal "
  "stress-test framework for such studies. The same caution applies to "
  "prospective urban-infrastructure siting in which historical outcome "
  "labels do not yet exist: optimization of a constructed proxy should be "
  "stress-tested against alternative specifications and spatial nulls "
  "before being interpreted as evidence of real-world advantage.")

H("Declarations")
P("Data availability: all inputs are public datasets (Table 1); code and "
  "derived tables in the project repository. Competing interests: none "
  "declared. Funding: none.")

H("References")
BIB = {
 "hakusyo2025": "Tokyo Hire-Taxi Association. Tokyo no Taxi 2025. https://taxi-tokyo.or.jp/ (accessed 2026-09-29).",
 "taxi_demand": "Moreira-Matias L, Gama J, Ferreira M, Mendes-Moreira J, Damas L. Predicting taxi-passenger demand using streaming data. IEEE Trans Intell Transp Syst. 2013;14(3):1393-1402.",
 "taxi_stand": "Ocalir EV, Ercoskun OY, Tur R. An integrated model of GIS and fuzzy logic (FMOTS) for location decisions of taxicab stands. Expert Syst Appl. 2010;37(7):4892-4901.",
 "taxi_demand2": "Hwang RH, Hsueh YL, Chen YT. An effective taxi recommender system based on a spatio-temporal factor analysis model. Inf Sci. 2015;314:28-40.",
 "yang2010": "Yang H, Leung CWY, Wong SC, Bell MGH. Equilibria of bilateral taxi-customer searching and meeting on networks. Transp Res Part B. 2010;44(8-9):1067-1083.",
 "tfinder": "Yuan NJ, Zheng Y, Zhang L, Xie X. T-Finder: a recommender system for finding passengers and vacant taxis. IEEE Trans Knowl Data Eng. 2013;25(10):2390-2403. doi:10.1109/TKDE.2012.153.",
 "pudo": "Alonso-Mora J, Samaranayake S, Wallar A, Frazzoli E, Rus D. On-demand high-capacity ride-sharing via dynamic trip-vehicle assignment. Proc Natl Acad Sci USA. 2017;114(3):462-467. doi:10.1073/pnas.1611675114.",
 "osm": "OpenStreetMap contributors. Planet dump and Overpass API. https://www.openstreetmap.org (ODbL; accessed 2026-09-29 via OSMnx 2.0.7).",
 "nlni": "Ministry of Land, Infrastructure, Transport and Tourism (Japan). National Land Numerical Information, N02 railway dataset (FY2023). https://nlftp.mlit.go.jp/ksj/ (accessed 2026-09-29).",
 "monitor": "Tokyo Taxi Center. Taxi user monitor survey, FY2023 tabulation report. https://www.tokyo-tc.or.jp/center/uploads/monitor_2024.pdf (accessed 2026-09-29).",
}
for i, rid in enumerate(REFS):
    p = doc.add_paragraph(); p.add_run(f"{i+1}. ").bold = True; p.add_run(BIB[rid])

H("Table 1. Public data sources")
t = doc.add_table(rows=5, cols=4); t.style = "Table Grid"
for j, h in enumerate(["Source", "Provider/License", "Scope", "Role"]):
    t.rows[0].cells[j].text = h
for i, r in enumerate([
    ["OSM road network + POIs", "OSM contributors / ODbL", "5 central wards", "segments, context, walk network"],
    ["NLNI N02 station locations", "MLIT / NLNI terms", "FY2023", "station-presence attractor"],
    ["Tokyo Taxi Center monitor survey", "Tokyo Taxi Center", "FY2023, n=2,662", "temporal profile"],
    ["THTA yearbook 2025", "THTA", "FY2024", "background"],
]):
    for j, v in enumerate(r): t.rows[i+1].cells[j].text = v

H("Table 2. Self-optimization outcomes by radius (combined specification)")
sub = abl[abl.spec == "COMB"]
t = doc.add_table(rows=len(sub)+1, cols=7); t.style = "Table Grid"
for j, h in enumerate(["Radius m", "origins", "improved", ">0.1 SD", "mean gain (SD)", "beats nearest major", "gain CI"]):
    t.rows[0].cells[j].text = h
for i, (_, r) in enumerate(sub.iterrows()):
    for j, v in enumerate([str(int(r.radius)), f"{int(r.n_origins)}", pc(r.frac_pos),
            pc(r.frac_gt_01), f2(r.mean_G), pc(r.gt_nearmaj), str(r.ci_G)]):
        t.rows[i+1].cells[j].text = v

H("Table 3. Ablation summary (300 m)")
sub = abl[abl.radius == 300]
t = doc.add_table(rows=len(sub)+1, cols=6); t.style = "Table Grid"
for j, h in enumerate(["Specification", "improved", ">0.1 SD", "beats nearest major", "beats random", "best is major road"]):
    t.rows[0].cells[j].text = h
name = {"ROAD": "Road-only", "ATTR": "Attractor-only", "PROXY": "Circulation proxy", "COMB": "Combined"}
for i, (_, r) in enumerate(sub.iterrows()):
    for j, v in enumerate([name[r.spec], pc(r.frac_pos), pc(r.frac_gt_01),
                           pc(r.gt_nearmaj), pc(r.gt_rand), pc(r.best_is_major)]):
        t.rows[i+1].cells[j].text = v

H("Table 4. Cross-specification transfer at 300 m (mean TG SD / % positive)")
t = doc.add_table(rows=5, cols=5); t.style = "Table Grid"
specs = ["ROAD", "ATTR", "PROXY", "COMB"]
for j, h in enumerate(["Selector \\ Evaluator", "Road-only", "Attractor-only", "Circulation proxy", "Combined"]):
    t.rows[0].cells[j].text = h
for i, s_ in enumerate(specs):
    t.rows[i+1].cells[0].text = name[s_]
    for j, e in enumerate(specs):
        if s_ == e:
            t.rows[i+1].cells[j+1].text = "(self)"
        else:
            row = ts[(ts.selector == s_) & (ts.evaluator == e) & (ts.radius == 300)]
            t.rows[i+1].cells[j+1].text = (f"{row.mean_TG.iloc[0]:.2f} / "
                                          f"{100*row.frac_pos.iloc[0]:.0f}%") if len(row) else "-"

H("Table 5. Spatial permutation null (combined specification, weekday 17:00)")
t = doc.add_table(rows=5, cols=6); t.style = "Table Grid"
for j, h in enumerate(["Radius m", "obs frac>0", "null frac>0", "empirical p", "obs mean G", "null mean G"]):
    t.rows[0].cells[j].text = h
for i, r in enumerate([100, 200, 300, 500]):
    nf = np.array([x[0] for x in nullarr[f"weekday_17_{r}"]])
    ng = np.array([x[1] for x in nullarr[f"weekday_17_{r}"]])
    pf = (1 + (nf >= po[str(r)][0]).sum()) / (1 + len(nf))
    for j, v in enumerate([str(r), f"{po[str(r)][0]:.3f}", f"{nf.mean():.3f}", f"{pf:.3f}",
                           f"{po[str(r)][1]:.2f}", f"{ng.mean():.2f}"]):
        t.rows[i+1].cells[j].text = v

doc.save(f"{OUT}/CEUS_STRESS_TEST_MAIN_SCIENCE_FINAL_inline.docx")
print("stress-test manuscript saved")

hl = Document(); hl.add_heading("Highlights", 0)
for b in [
    "Self-optimized urban proxies can yield large apparent local gains",
    "Cross-specification transfer can reveal weakly transferable structure",
    "Spatial permutation quantifies gains caused by generic heterogeneity",
    "Internal stress tests help audit urban proxies without outcome labels",
    "Street-hail relocation shows the framework without fleet telemetry",
]:
    hl.add_paragraph(b, style="List Bullet")
hl.save(f"{OUT}/CEUS_STRESS_TEST_HIGHLIGHTS_SCIENCE_FINAL.docx")

c = Document()
c.add_paragraph("Dear Editors,")
c.add_paragraph(
    "This manuscript addresses a methodological problem in urban spatial "
    "optimization: large gains obtained by optimizing a constructed proxy "
    "under its own definition need not indicate transferable or externally "
    "meaningful spatial structure. We submit 'Stress-testing public-data "
    "urban accessibility proxies: street-hail taxi relocation without "
    "fleet telemetry', which quantifies this issue in a street-hail case "
    "by comparing self-gain with cross-specification transfer, "
    "benchmarking against spatial permutation nulls, and deriving a "
    "practical internal stress-test framework.")
c.add_paragraph(
    "The methodological point will matter to CEUS readers: a heterogeneous "
    "constructed surface yields local maxima almost mechanically, so "
    "within-score optimization gains are not external validation. We "
    "propose a reusable internal stress test — component ablation, "
    "cross-specification transfer, and spatial permutation nulls — and "
    "report its outcome honestly, including the negative findings, on a "
    "directed road-network representation built entirely from public data "
    "and no proprietary fleet telemetry. The framework is also relevant to "
    "prospective urban-infrastructure planning where operational outcome "
    "labels do not yet exist.")
c.add_paragraph(
    "The manuscript is original, involves no human subjects, uses only "
    "legally accessible public data, and is not under consideration "
    "elsewhere.")
c.add_paragraph("Sincerely,\nThe Authors")
c.save(f"{OUT}/CEUS_STRESS_TEST_COVER_LETTER_SCIENCE_FINAL.docx")
print("cover letter + highlights saved")
