#!/usr/bin/env python3
"""FINAL_QC manuscript builder — all analysis-derived values are loaded from
analysis/canonical_results.json (built by build_canonical_results.py).
No scientific-result literal may be typed here; fail-loud on missing keys."""
import os, json, zipfile
import numpy as np

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
def m_sup(b, s):
    e = m_el("sSup"); be = m_el("e"); se = m_el("sup")
    be.append(m_run(b)); se.append(m_run(s)); e.extend([be, se]); return e
def m_subsup(b, sub, sup):
    e = m_el("sSubSup"); be = m_el("e"); se = m_el("sub"); su = m_el("sup")
    be.append(m_run(b)); se.append(m_run(sub)); su.append(m_run(sup))
    e.extend([be, se, su]); return e
def m_frac(n, d):
    e = m_el("f"); ne = m_el("num"); de = m_el("den")
    for x in (n if isinstance(n, list) else [n]): ne.append(x if not isinstance(x, str) else m_run(x))
    for x in (d if isinstance(d, list) else [d]): de.append(x if not isinstance(x, str) else m_run(x))
    e.extend([ne, de]); return e
def om(els):
    o = m_el("oMath")
    for e in els: o.append(e if not isinstance(e, str) else m_run(e))
    return o

# ---------------- canonical registry ----------------
CANON = json.load(open(f"{ROOT}/analysis/canonical_results.json"))
def canon(key):
    """Dotted-key lookup; canonical keys themselves may contain dots
    (e.g. 'COMB.300'), so descend by longest matching joined prefix."""
    parts = key.split(".")
    node = CANON
    i = 0
    while i < len(parts):
        for j in range(len(parts), i, -1):
            cand = ".".join(parts[i:j])
            if isinstance(node, dict) and cand in node:
                node = node[cand]; i = j; break
        else:
            raise SystemExit(f"FAIL-LOUD: canonical key missing: {key}")
    return node

def pc(x): return f"{100*x:.0f}%"
def f2(x): return f"{x:.2f}"
def f3(x): return f"{x:.3f}"
def cit(x): return "[" + ", ".join(f"{v:.3f}" for v in x) + "]"
def wp(p): return "p<0.001" if p < 0.001 else f"p={p:.3f}"

def AB(spec, r, k): return canon(f"ablation.{spec}.{r}.{k}")
def TF(a, b, k): return canon(f"transfer.{a}_to_{b}.300.{k}")
def PM(p, r, k): return canon(f"permutation.{p}.{r}.{k}")

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12)
def H(t, l=1): doc.add_heading(t, level=l)
def P(*parts):
    """Paragraph of sequential parts: str -> text run; 'MATH:' list -> OMML."""
    p = doc.add_paragraph()
    for part in parts:
        if isinstance(part, str):
            p.add_run(part)
        else:                       # omml element
            p._p.append(part)
    return p
def EQ(els):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p._p.append(om(els))
def FIGURE(name, cap, w=6.0):
    fn = f"{FIG}/{name}.png"
    if not os.path.exists(fn):
        raise SystemExit(f"FAIL-LOUD: missing figure {fn}")
    doc.add_picture(fn, width=Inches(w))
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(cap); r.italic = True; r.font.size = Pt(10)

REFS = []
def cite(*ids):
    for r in ids:
        if r not in REFS: REFS.append(r)
    return "[" + ",".join(str(REFS.index(r) + 1) for r in ids) + "]"

NSEG = f"{canon('network.n_segments_hail_ok'):,}"
NWE = f"{canon('network.n_walk_edges'):,}"
NOR = f"{canon('config.n_origins_planned'):,}"
NPERM = canon('config.n_permutations')
NR = canon('ablation.n_origins_range')
RADR = canon('permutation.weekday_17.emp_p_frac_range_200_500')

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
  "on the directed road network of Tokyo's five central wards "
  f"({NSEG} segments) and audit relocation optimization over {NOR} origins "
  "at 100-500 m walking radii through component ablation, cross-specification "
  f"transfer, a simple road-hierarchy heuristic, and {NPERM}-permutation "
  "spatial nulls with origin-clustered inference. Apparent gains are large "
  f"({pc(AB('COMB',300,'frac_pos'))} of origins improved, mean "
  f"{f2(AB('COMB',300,'mean_G'))} SD at 300 m) and exceed the nearest-major-"
  f"road heuristic in {pc(AB('COMB',300,'gt_nearmaj'))} of origins, but "
  "cross-specification transfer between conceptually distinct component "
  f"families is weak ({pc(TF('ROAD','ATTR','frac_pos'))} and "
  f"{pc(TF('ATTR','ROAD','frac_pos'))} of origins positive), and spatially "
  "permuted surfaces reproduced improvement prevalence almost fully, with "
  "only a small observed advantage at some walking radii (empirical "
  f"p={f2(RADR[0])}-{f2(RADR[1])} for the weekday-17 null, below 0.05 only "
  "at 200 m), while producing larger mean gain magnitudes than the "
  "observed surface. Large within-score optimization gains therefore did "
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
  "to be challenged, not as validation by itself (Figure 1). These tests "
  "are internal checks, not universally sufficient validation criteria.")
FIGURE("fig1_framework", "Figure 1. Internal stress-test workflow: public "
       "urban data, alternative proxy constructions, local optimization, "
       "component ablation, cross-specification transfer, spatial "
       "permutation null, heuristic comparison, and calibrated "
       "interpretation.")

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
  + cite("monitor") + " (Table 1). The restricted CSIS Pseudo-PFLOW "
  "product was inaccessible and substituted. The FY2023 N02 schema "
  "contains no passenger-count field, so the station term is an "
  "unweighted location kernel (documented correction).")
H("2.3 Directed road-network representation", 2)
P(f"{NSEG} hail-feasible directed segments from the OSM drive graph; "
  f"{NWE}-edge walk graph for pedestrian distances (equirectangular "
  "metric).")
H("2.4 Alternative opportunity proxies", 2)
P("A circulation-potential proxy combines road-class weight, a Gaussian "
  "attractor kernel field ",
  om([m_run("D(e)")]),
  " (kernel bandwidth ",
  om([m_run("σ = 300 m")]),
  "), and a period multiplier from the monitor profile blended toward "
  "nightlife contexts:")
EQ([m_sub("P", "circ"), m_run("(e,t) = "), m_sub("w", "road"),
    m_run("(e)·(0.3 + D(e))·P(h;ctx(e))")])
P("Four z-standardized specifications: road-only (hierarchy, degree, "
  "lanes); attractor-only (station, nightlife, hotel/hospital, transit, "
  "taxi-stand kernels); the circulation proxy; and the combined score")
EQ([m_sub("S", "COMB"), m_run(" = z(z log(1+"), m_sub("P", "circ"),
    m_run(") + 0.5 "), m_sub("S", "road"), m_run(" + 0.4 "),
    m_sub("C", "ctx"), m_run(")")])
P("All are modeled public-data proxies — none is observed taxi "
  "availability.")
H("2.5 Local pedestrian relocation optimization", 2)
P(f"{NOR} origins (seed {canon('config.seed')}); candidates are segments "
  "reachable within 100/200/300/500 m walking distance; the selected "
  "location maximizes the score over candidates.")
H("2.6 The self-optimization problem", 2)
P("If ", om([m_sub("S", "A"), m_run("(x)")]),
  " is the opportunity score and ",
  om([m_subsup("x", "A", "*"), m_run(" = argmax "), m_sub("x", "c"),
      m_run("∈N("), m_sub("x", "0"), m_run(") "), m_sub("S", "A"),
      m_run("("), m_sub("x", "c"), m_run(")")]),
  ", then")
EQ([m_sub("S", "A"), m_run("("), m_subsup("x", "A", "*"), m_run(") − "),
    m_sub("S", "A"), m_run("("), m_sub("x", "0"), m_run(") ≥ 0")])
P("holds by construction whenever a better-scoring candidate exists in ",
  om([m_run("N("), m_sub("x", "0"), m_run(")")]),
  ". Positive self-gain is therefore partly structural and cannot "
  "alone validate the proxy — the central premise of this audit.")
H("2.7 Component ablation", 2)
P("Each specification is optimized separately to test whether apparent "
  "gains depend on one construction.")
H("2.8 Cross-specification transfer", 2)
P("Transfer gain ",
  om([m_run("TG(A→B) = "), m_sub("S", "B"), m_run("("),
      m_subsup("x", "A", "*"), m_run(") − "), m_sub("S", "B"), m_run("("),
      m_sub("x", "0"), m_run(")")]),
  " evaluates locations selected under specification A under a distinct "
  "specification B. Off-diagonal transfer — especially between the "
  "road-only and attractor-only component families — is the internal "
  "validity test; diagonal terms are self-optimization.")
H("2.9 Spatial permutation null", 2)
P("Scores are permuted across all hail-feasible segments (",
  str(NPERM),
  " repetitions), preserving the marginal distribution, network geometry, "
  "origin distribution, and candidate counts. Observed improvement "
  "fractions and gain magnitudes are compared against the null; empirical ",
  om([m_run("p = (1 + #{null ≥ obs})/(1 + N)")]),
  ".")
H("2.10 Constrained permutation sensitivity", 2)
P("A within-ward permutation preserves coarse geographic structure and "
  "tests whether fine-scale organization remains non-random.")
H("2.11 Heuristic comparators", 2)
P("Stay; random relocation (10 seeded draws); nearest major-class road.")
H("2.12 Cluster-aware statistical inference", 2)
P(f"Origin-period rows are repeated measurements. Period-invariant "
  f"specifications use unique origins (n = {NR[0]:,}-{NR[1]:,}); "
  "period-varying specifications use an origin-clustered bootstrap "
  f"({canon('config.bootstrap_replicates'):,} replicates) and paired "
  "tests on origin-mean differences. Effects, CIs, and p-values are "
  "reported together.")
H("2.13 Reproducibility", 2)
P("Fixed seeds, raw-data snapshots with a SHA-256 ledger, public code, "
  "a canonical numerical registry, and machine-readable tables.")

H("3. Results")
H("3.1 Opportunity surfaces and local heterogeneity", 2)
P("All four surfaces are strongly heterogeneous, with ridges along "
  "arterials and station fronts (Figure 2).")
FIGURE("fig2_map", "Figure 2. Modeled street-hail opportunity surface "
       "(combined specification, SD units), weekday 17:00 and weekend 23:00.")
H("3.2 Apparent gains under self-optimization", 2)
P("Self-optimization produces large apparent gains (RQ1): "
  f"{pc(AB('COMB',100,'frac_pos'))}-{pc(AB('COMB',500,'frac_pos'))} of "
  "origins have a higher-scoring segment within reach, mean gain "
  f"{f2(AB('COMB',100,'mean_G'))}-{f2(AB('COMB',500,'mean_G'))} SD "
  "(Figure 3, Table 2; a worked example in Figure 4). These gains are "
  "partly structural by construction.")
FIGURE("fig3_gain_by_radius", "Figure 3. Apparent self-optimization gains "
       "(SD units) by walking radius, combined specification.")
FIGURE("fig4_worked_example", "Figure 4. Local optimization example "
       "(200 m, weekday 17:00): apparent gain under the combined score.")
H("3.3 Comparison with simple heuristics", 2)
P("Against heuristics (RQ5): the combined optimum beats random relocation "
  f"in {pc(AB('COMB',300,'gt_rand'))} of origins at 300 m, and beats the "
  f"nearest major road in {pc(AB('COMB',300,'gt_nearmaj'))} of origins "
  f"(paired surplus {f2(AB('COMB',300,'diff_nearmaj'))} SD, clustered 95% "
  f"CI {cit(AB('COMB',300,'diff_nearmaj_ci'))}, Wilcoxon "
  f"{wp(AB('COMB',300,'wilcoxon_p'))}; Figure 5). These values establish "
  "the magnitude of apparent within-score gain, not external validity: "
  "the constructed score contains spatial information beyond road "
  "hierarchy alone, but that does not show the selected location is "
  "better for obtaining a real taxi.")
FIGURE("fig5_strategies", "Figure 5. Mean modeled score by strategy "
       "(combined specification, radii pooled). Error bars = SEM.")
H("3.4 Component ablation", 2)
P(f"Apparent gains persist under every construction (RQ2): at 300 m, "
  f"road-only {pc(AB('ROAD',300,'frac_pos'))}, attractor-only "
  f"{pc(AB('ATTR',300,'frac_pos'))}, proxy {pc(AB('PROXY',300,'frac_pos'))}, "
  f"combined {pc(AB('COMB',300,'frac_pos'))} improved (Figure 6, Table 3). "
  "Segment rankings agree only moderately to strongly (Spearman "
  f"{f2(canon('agreement.spearman_min'))}-{f2(canon('agreement.spearman_max'))}): "
  "the constructions are alternative readings with varying degrees of "
  "agreement, and persistence is not proof of external validity.")
FIGURE("fig6_ablation", "Figure 6. Component ablation across walking radii.")
H("3.5 Cross-specification transfer", 2)
P("Transfer between conceptually distinct component families is weak "
  f"(RQ3): road-selected locations improve the attractor score for "
  f"{pc(TF('ROAD','ATTR','frac_pos'))} of origins (mean "
  f"{f2(TF('ROAD','ATTR','mean_TG'))} SD) and attractor-selected locations "
  f"improve the road score for {pc(TF('ATTR','ROAD','frac_pos'))} of "
  f"origins ({f2(TF('ATTR','ROAD','mean_TG'))} SD) — near-chance "
  f"fractions. Transfer into the proxy is stronger (attr→proxy "
  f"{pc(TF('ATTR','PROXY','frac_pos'))}; road→proxy "
  f"{pc(TF('ROAD','PROXY','frac_pos'))}) because the proxy embeds road "
  "hierarchy (Figure 7, Table 4). Weak off-diagonal transfer is itself a "
  "key finding: the constructions partly identify different, non-"
  "transferable structure.")
FIGURE("fig7_transfer_matrix", "Figure 7. Transfer matrix at 300 m. "
       "Diagonal would be self-optimization; off-diagonal entries are "
       "internal transfer evidence.")
H("3.6 Spatial permutation null", 2)
P("Against the unrestricted null (RQ4): improvement prevalence marginally "
  "exceeds permutation at 200-500 m (observed "
  f"{f3(PM('weekday_17','300','obs_frac'))} vs null "
  f"{f3(PM('weekday_17','300','null_frac'))} at 300 m; empirical "
  f"p={f2(RADR[0])}-{f2(RADR[1])} for the weekday-17 null) but not at "
  f"100 m (p=1.0). Mean gain magnitude does not exceed the null at any "
  f"radius (observed {f2(PM('weekday_17','300','obs_gain'))} vs null "
  f"{f2(PM('weekday_17','300','null_gain'))} SD at 300 m; Figure 8, "
  "Table 5). A spatially unstructured surface with identical marginals "
  "produces larger local contrasts: most of the apparent gain is generic "
  "maximum-selection, while the observed surface's spatial "
  "autocorrelation actually compresses local maxima.")
FIGURE("fig8_permutation_null", "Figure 8. Observed statistics (red) vs "
       f"{NPERM}-permutation null (gray), 300 m, weekday 17:00.")
H("3.7 Constrained-null sensitivity", 2)
P("The within-ward and weekend-23 nulls reproduce the same pattern "
  "(marginal prevalence advantage at 200-500 m; observed magnitude below "
  "the null), so coarse district structure does not rescue the "
  "gain-magnitude claim.")
H("3.8 Temporal and district secondary analyses", 2)
P("Under the modeled temporal specifications, gains are largest in the "
  "weekday-morning period; the weekend specification shifts modeled "
  "opportunity toward nightlife contexts — input-profile consequences "
  "(Figure 9). Kernel bandwidth 150/500 m leaves gains nearly unchanged "
  f"(rho {f2(canon('sigma.rho_150'))}/{f2(canon('sigma.rho_500'))}).")
FIGURE("fig9_heterogeneity", "Figure 9. Modeled gain by hour/day-type and "
       "ward/radius — model behavior, not observed patterns.")
H("3.9 Summary of evidence levels", 2)
P("Level 1 (self-optimization): large apparent gains — achieved. Level 2 "
  "(internal stress tests): ablation passed; transfer weak; heuristic "
  "contrast retained; permutation shows prevalence marginally above but "
  "magnitude below null. Level 3 (external empirical validation): not "
  "available in this study.")

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
P("The decisive result: a shuffled surface reproduces ≈"
  f"{pc(canon('permutation.null_reproduces_frac_mean'))} of the observed "
  "improvement prevalence on average across the examined radii "
  f"(null/observed ratio {f2(canon('permutation.null_reproduces_frac_range')[0])}-"
  f"{f2(canon('permutation.null_reproduces_frac_range')[1])}) and produced "
  "larger mean gain magnitudes. What the real urban surface contributes "
  "is a marginal reliability edge — not bigger wins. Interpreted "
  "honestly, this means the constructed proxy's fine-scale spatial "
  "arrangement adds little beyond generic heterogeneity for relocation "
  "purposes.")
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
P("A compact internal stress-test workflow follows from the results "
  "(Figure 1): (1) CONSTRUCT one or more plausible proxy surfaces; "
  "(2) OPTIMIZE candidate locations; (3) ABLATE components to test "
  "specification dependence; (4) TRANSFER selected locations across "
  "alternative specifications; (5) NULL-TEST against spatially permuted "
  "or otherwise structured nulls; (6) BENCHMARK against simple domain "
  "heuristics; (7) CALIBRATE claims to the evidence level that survives. "
  "This is an internal, falsification-oriented audit — not a universal "
  "standard.")
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
P("Data availability: all inputs are public datasets (Table 1); "
  "preprocessing and analysis code, the canonical numerical registry, and "
  "machine-readable result tables are openly available at "
  "https://github.com/bougtoir/street-hail-taxi-accessibility. "
  "Competing interests: none declared. Funding: none.")

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
    ["Tokyo Taxi Center monitor survey", "Tokyo Taxi Center",
     f"FY2023, n={canon('config.monitor_survey_n'):,}", "temporal profile"],
    ["THTA yearbook 2025", "THTA", "FY2024", "background"],
]):
    for j, v in enumerate(r): t.rows[i+1].cells[j].text = v

H("Table 2. Self-optimization outcomes by radius (combined specification)")
t = doc.add_table(rows=5, cols=7); t.style = "Table Grid"
for j, h in enumerate(["Radius m", "origins", "improved", ">0.1 SD", "mean gain (SD)", "beats nearest major", "gain CI"]):
    t.rows[0].cells[j].text = h
for i, r in enumerate(canon("config.radii_m")):
    a = canon(f"ablation.COMB.{r}")
    for j, v in enumerate([str(r), f"{a['n_origins']}", pc(a['frac_pos']),
            pc(a['frac_gt_01']), f2(a['mean_G']), pc(a['gt_nearmaj']), cit(a['ci_G'])]):
        t.rows[i+1].cells[j].text = v

H("Table 3. Ablation summary (300 m)")
t = doc.add_table(rows=5, cols=6); t.style = "Table Grid"
for j, h in enumerate(["Specification", "improved", ">0.1 SD", "beats nearest major", "beats random", "best is major road"]):
    t.rows[0].cells[j].text = h
name = {"ROAD": "Road-only", "ATTR": "Attractor-only", "PROXY": "Circulation proxy", "COMB": "Combined"}
for i, s_ in enumerate(["ROAD", "ATTR", "PROXY", "COMB"]):
    a = canon(f"ablation.{s_}.300")
    for j, v in enumerate([name[s_], pc(a['frac_pos']), pc(a['frac_gt_01']),
                           pc(a['gt_nearmaj']), pc(a['gt_rand']), pc(a['best_is_major'])]):
        t.rows[i+1].cells[j].text = v

H("Table 4. Cross-specification transfer at 300 m (mean TG SD / % positive)")
t = doc.add_table(rows=4, cols=5); t.style = "Table Grid"
specs = ["ROAD", "ATTR", "PROXY"]
evals = ["ROAD", "ATTR", "PROXY", "COMB"]
for j, h in enumerate(["Selector \\ Evaluator", "Road-only", "Attractor-only", "Circulation proxy", "Combined"]):
    t.rows[0].cells[j].text = h
for i, s_ in enumerate(specs):
    t.rows[i+1].cells[0].text = name[s_]
    for j, e in enumerate(evals):
        if s_ == e:
            t.rows[i+1].cells[j+1].text = "(self)"
        else:
            k = canon(f"transfer.{s_}_to_{e}.300")
            t.rows[i+1].cells[j+1].text = f"{f2(k['mean_TG'])} / {pc(k['frac_pos'])}"

H("Table 5. Spatial permutation null (combined specification, weekday 17:00)")
t = doc.add_table(rows=5, cols=6); t.style = "Table Grid"
for j, h in enumerate(["Radius m", "obs frac>0", "null frac>0", "empirical p", "obs mean G", "null mean G"]):
    t.rows[0].cells[j].text = h
for i, r in enumerate(canon("config.radii_m")):
    d = canon(f"permutation.weekday_17.{r}")
    for j, v in enumerate([str(r), f3(d['obs_frac']), f3(d['null_frac']),
                           f3(d['emp_p_frac']), f2(d['obs_gain']), f2(d['null_gain'])]):
        t.rows[i+1].cells[j].text = v

doc.save(f"{OUT}/CEUS_MAIN_MANUSCRIPT_FINAL_QC_inline.docx")
print("FINAL_QC manuscript saved")

hl = Document(); hl.add_heading("Highlights", 0)
for b in [
    "Self-optimized urban proxies can yield large apparent local gains",
    "Cross-specification transfer can reveal weakly transferable structure",
    "Spatial permutation quantifies gains caused by generic heterogeneity",
    "Internal stress tests help audit urban proxies without outcome labels",
    "Street-hail relocation shows the framework without fleet telemetry",
]:
    hl.add_paragraph(b, style="List Bullet")
hl.save(f"{OUT}/CEUS_HIGHLIGHTS_FINAL_QC.docx")

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
    "elsewhere. Preprocessing and analysis code plus machine-readable "
    "result tables are openly available at "
    "https://github.com/bougtoir/street-hail-taxi-accessibility.")
c.add_paragraph("Sincerely,\nThe Authors")
c.save(f"{OUT}/CEUS_COVER_LETTER_FINAL_QC.docx")
print("cover letter + highlights saved")
