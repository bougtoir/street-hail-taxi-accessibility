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

BIB = json.load(open(f"{ROOT}/analysis/new_bib.json"))
tp = doc.add_paragraph(); tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
tr = tp.add_run("Stress-testing public-data urban accessibility proxies: "
                "street-hail taxi relocation without fleet telemetry")
tr.bold = True; tr.font.size = Pt(16)

H("Abstract")
P("Constructed spatial proxies — accessibility indices, amenity scores, "
  "availability surfaces — are widely optimized in urban-computing "
  "research wherever direct operational ground truth is unavailable. "
  "Because a heterogeneous surface contains local maxima, optimizing a "
  "proxy under its own score mechanically produces apparent gains, and "
  "self-optimization is not external validation. Using street-hail taxi "
  "relocation as a motivating case study, we construct four "
  "public-data-derived opportunity surfaces on the directed road network "
  f"of Tokyo's five central wards ({NSEG} segments) and audit relocation "
  f"optimization over {NOR} origins at 100-500 m walking radii through "
  f"component ablation, cross-specification transfer, a simple "
  f"road-hierarchy heuristic, and {NPERM}-permutation spatial nulls with "
  "origin-clustered inference. Apparent gains are large "
  f"({pc(AB('COMB',300,'frac_pos'))} of origins improved, mean "
  f"{f2(AB('COMB',300,'mean_G'))} SD at 300 m) and exceed the "
  "nearest-major-road heuristic in "
  f"{pc(AB('COMB',300,'gt_nearmaj'))} of origins, but "
  "cross-specification transfer between conceptually distinct component "
  f"families is weak ({pc(TF('ROAD','ATTR','frac_pos'))} and "
  f"{pc(TF('ATTR','ROAD','frac_pos'))} of origins positive), and "
  "spatially permuted surfaces reproduced improvement prevalence almost "
  "fully, with only a small observed advantage at some walking radii "
  f"(empirical p={f2(RADR[0])}-{f2(RADR[1])} for the weekday-17 null, "
  "below 0.05 only at 200 m), while producing larger mean gain "
  "magnitudes than the observed surface. Large within-score optimization "
  "gains therefore did not translate into equally strong "
  "cross-specification evidence and were partly reproducible under "
  "spatial nulls: self-optimization alone is insufficient validation of "
  "a constructed urban spatial proxy. We therefore propose "
  "cross-specification transfer, component ablation, spatial-null "
  "comparison, and simple heuristic benchmarking as complementary "
  "internal stress tests when external outcome labels are unavailable.")
P("Keywords: urban accessibility; geocomputation; spatial optimization; "
  "mobility proxy; permutation test; public urban data")

H("1. Introduction")
P("Urban planning and mobility research increasingly relies on "
  "constructed spatial proxies: accessibility indices that summarize "
  "the spatial distribution of opportunities " +
  cite("hansen1959", "handy1997") + ", cumulative-opportunity and "
  "gravity-type measures " + cite("geurs2004") + ", amenity and "
  "composite urban scores " + cite("oecd2008", "greco2019") + ", and "
  "availability or demand surfaces built from open spatial data. These "
  "constructions sit at the core of the geocomputational research "
  "programme that Computers, Environment and Urban Systems has long "
  "housed: spatial decision support built on assembled geodata "
  "rather than on measured outcomes " + cite("longley2015") +
  ". Such constructions are not conveniences of last resort: they exist "
  "because the outcomes planners care about — realized access, "
  "successful encounters, used services — are routinely proprietary, "
  "expensive, or not yet observable. Accessibility itself has a long "
  "theoretical lineage as a determinant of land use and travel "
  "behaviour " + cite("hansen1959", "miller1999") + ", and its "
  "measurement has been shown to depend materially on specification "
  "choices " + cite("handy1997", "kwan1998") + ".")
P("A first methodological difficulty is therefore that accessibility "
  "and opportunity surfaces are not uniquely defined. The measure "
  "chosen (cumulative opportunity, gravity, space-time, "
  "place-rank), the distance decay assumed, the scale of aggregation, "
  "the weighting of components, and the spatial representation all "
  "change the resulting surface and, with it, any downstream "
  "conclusion " + cite("handy1997", "geurs2004", "shen1998") +
  ". Composite indicators inherit a parallel sensitivity: weighting, "
  "normalization, and aggregation choices are consequential and partly "
  "arbitrary, which is why construction handbooks recommend robustness "
  "checks over single headline values " + cite("oecd2008",
  "freudenberg2003", "greco2019") + ". Spatial representation adds a "
  "further, well-documented layer of fragility: results depend on the "
  "zoning system and scale of analysis — the modifiable areal unit "
  "problem " + cite("openshaw1984", "fotheringham1991") + " — and on "
  "how networks and boundaries are operationalized " +
  cite("longley2015", "jelinski1996") + ".")
P("Optimization adds a second, less often examined inferential "
  "problem. If the same constructed score is used both to select the "
  "optimum and to judge it, a positive gain is partly structural: a "
  "heterogeneous surface contains local maxima, and choosing the best "
  "candidate in a neighbourhood mechanically outperforms the baseline. "
  "This is a circular-validation risk — the instrument that proposes "
  "the answer also grades it. Sensitivity analysis in the "
  "specification sense " + cite("saltelli2008") + " asks whether "
  "answers change when assumptions change, but it does not ask the "
  "harder questions: does the selected location remain preferable "
  "under another plausible proxy, does the gain exceed what a "
  "spatially unstructured surface of identical marginals would yield, "
  "and does a simple domain heuristic recover most of the apparent "
  "benefit? Recent methodological work on multiverse and "
  "specification-curve analysis " + cite("steegen2016",
  "simonsohn2020") + " and on undisclosed analytic flexibility " +
  cite("simmons2011", "gelman2014") + " has made a similar point in "
  "statistical settings; the spatial-optimization analogue is less "
  "developed.")
P("Robustness practice in the applied spatial literatures has "
  "largely converged on parameter sensitivity: vary the distance "
  "decay, vary the weights, vary the scale, and check that rankings "
  "survive " + cite("saltelli2008", "greco2019") + ". This is "
  "necessary but addresses a different question than the one "
  "optimization raises. Specification-curve and multiverse analyses "
  "have shown, in statistical settings, that conclusions robust to "
  "perturbation can still be artefacts of analytic choice when the "
  "selection criterion is correlated with the outcome " +
  cite("steegen2016", "simonsohn2020", "simmons2011") + ". The "
  "spatial-proxy analogue is sharper: the 'perturbations' are "
  "alternative plausible surfaces, and the 'selection' is literal "
  "argmax over a spatial neighbourhood. What is missing in the "
  "accessibility and geocomputation literature is a habit of "
  "asking whether a proxy-optimized location still looks good under "
  "another defensible surface, and whether the gain exceeds what a "
  "spatially meaningless surface would deliver.")
P("Street-hail taxi relocation is an instructive case study for this "
  "problem. The operational data that could measure vacant-taxi "
  "opportunity are proprietary — recommender systems like T-Finder " +
  cite("tfinder") + " and trajectory-based demand models " +
  cite("taxi_demand", "taxi_demand2", "yuan2011", "zheng2010") +
  " all presuppose fleet telemetry. The passenger's problem is "
  "concretely spatial: where to stand or walk in order to encounter a "
  "cruising taxi, a question the bilateral search-and-meeting "
  "literature has formalized " + cite("yang2010", "yang2002",
  "wong2008") + ". Street-hail remains a substantial market in dense "
  "cities " + cite("hakusyo2025") + ", public spatial data are "
  "tempting substitutes for the missing telemetry, and taxi-stand and "
  "dispatch siting work shows the practical appetite for such "
  "proxies " + cite("taxi_stand") + ". The strand of work on "
  "demand prediction and recommendation " + cite("taxi_demand",
  "taxi_demand2", "yuan2011") + " and on equilibrium analysis of "
  "the hail market " + cite("yang2002", "wong2008") + " presumes "
  "exactly the kind of observed demand or trajectories that are "
  "unavailable here — which is what makes the case clean: it "
  "isolates the proxy-validity question from any claim of "
  "operational improvement. Prior taxi work has pursued "
  "operational effectiveness given demand data; the contribution here "
  "is not a recommendation system but a methodological audit of what "
  "proxy optimization can and cannot establish when those data are "
  "absent.")
P("Two points of scope follow. First, the passenger-side "
  "relocation question — where to stand to maximize encounter "
  "probability — is well motivated practically " +
  cite("yang2010", "yuan2011") + ", but this paper deliberately "
  "does not deliver a relocation system; it uses the problem to "
  "examine what public-data optimization can establish. Second, "
  "the methodological gap identified above is not hypothetical: "
  "optimization of constructed surfaces is standard practice in "
  "accessibility-based planning, facility siting, and mobility "
  "availability analysis, and the validation habits carried over "
  "from descriptive index work (sensitivity of the measure) do "
  "not cover the inferential step from measure to optimum.")
P("The street-hail instance is deliberately simple — one city, "
  "one decision type, one family of public data — because the "
  "inferential point is easier to see without operational "
  "machinery around it, and the same construction applies "
  "wherever a planner- or analyst-built surface is optimized "
  "against itself.")
P("The contribution is methodological. The paper (1) formalizes the "
  "distinction between within-proxy optimization gain and evidence of "
  "transferable spatial structure — a location selected under score A "
  "may score higher under A (apparent gain), may or may not improve a "
  "distinct plausible score B (transferable internal structure), and "
  "neither is evidence of a real-world outcome (external validity); "
  "(2) operationalizes cross-specification transfer as an internal "
  "validity stress test; (3) uses spatial permutation nulls " +
  cite("besag1977", "manly2007") + " to quantify how much apparent "
  "gain can arise from a heterogeneous surface without meaningful "
  "observed spatial organization, in the spirit of spatial-pattern "
  "inference under autocorrelation " + cite("moran1950",
  "getis1992", "anselin1995") + "; (4) combines ablation, transfer, "
  "null comparison, and simple heuristic benchmarking into a "
  "practical falsification-oriented stress-test framework; and (5) "
  "demonstrates the framework on street-hail taxi relocation, where "
  "no proprietary fleet telemetry exists (Figure 1). These tests are "
  "internal checks, not universally sufficient validation criteria. "
  "They complement, rather than replace, conventional sensitivity "
  "analysis and conventional validation — they exist for the "
  "regime where external labels cannot be obtained at all; "
  "their role is analogous to robustness and falsification practices "
  "in the specification-uncertainty literature " + cite("steegen2016",
  "simonsohn2020") + ".")
FIGURE("fig1_framework", "Figure 1. Internal stress-test workflow: "
       "public urban data, alternative proxy constructions, local "
       "optimization, component ablation, cross-specification "
       "transfer, spatial permutation null, heuristic comparison, and "
       "calibrated interpretation.")

H("1.1 Research questions", 2)
P("RQ1: How large are apparent relocation gains under "
  "self-optimization? RQ2: Do gains persist across alternative "
  "component specifications? RQ3: Do locations selected under one "
  "specification improve another specification's score? RQ4: Do "
  "observed gains exceed those of spatially permuted surfaces with "
  "identical marginals? RQ5: How much of the gain does the "
  "nearest-major-road heuristic explain?")

H("2. Materials and Methods")
H("2.1 Study area and case-study rationale", 2)
P("Five contiguous central wards of Tokyo (Chiyoda, Chuo, Minato, "
  "Shinjuku, Shibuya) form the study area — a canonical high-density "
  "street-hail environment " + cite("hakusyo2025") + " where fleet "
  "telemetry is inaccessible but public spatial data are rich. The "
  "area contains the city's principal nightlife and business "
  "districts, so the constructed proxies face a genuinely hard test.")
H("2.2 Public urban data", 2)
P("OpenStreetMap road network and points of interest via the "
  "Overpass API " + cite("osm") + "; FY2023 railway-station "
  "locations from the MLIT National Land Numerical Information N02 "
  "dataset " + cite("nlni") + "; and the hourly taxi-use "
  "distribution from the Tokyo Taxi Center monitor survey " +
  cite("monitor") + " (Table 1). The restricted CSIS Pseudo-PFLOW "
  "product was inaccessible and substituted with the monitor "
  "profile. The FY2023 N02 schema contains no passenger-count "
  "field, so the station term is an unweighted location kernel — a "
  "documented simplification whose effect is bounded by the ablation "
  "and transfer tests. Each source is also a proxy-construction "
  "choice: station presence is not station usage, monitor-period "
  "profiles are not vacant-supply profiles, and OSM hierarchy is "
  "not cruising demand — the audit's job is to make those gaps "
  "visible rather than to close them by assumption.")
H("2.3 Directed road-network representation", 2)
P(f"The street-hail decision is made on streets, not in zones: "
  f"direction matters because a passenger can hail only the "
  f"travelling side of a divided road, and one-way structure changes "
  f"which segments carry cruising flow. A directed segment graph "
  f"({NSEG} hail-feasible segments) therefore replaces areal cells, "
  f"avoiding the aggregation ambiguity of zonal representations " +
  cite("fotheringham1991") + "; a {NWE}-edge pedestrian walk graph "
  f"underlies the equirectangular walking distances. The choice "
  f"matters for the audit itself: a zonal accessibility grid would "
  f"smooth the very local maxima that self-optimization exploits, "
  f"so the network representation keeps the inferential problem "
  f"visible rather than averaged away.")
H("2.4 Alternative opportunity proxies", 2)
P("The four specifications are deliberately alternative plausible "
  "readings of 'opportunity', not competing predictive models. A "
  "circulation-potential proxy combines road-class weight, a "
  "Gaussian attractor kernel field ",
  om([m_run("D(e)")]),
  " (kernel bandwidth ",
  om([m_run("σ = 300 m")]),
  "), and a period multiplier from the monitor profile blended "
  "toward nightlife contexts:")
EQ([m_sub("P", "circ"), m_run("(e,t) = "), m_sub("w", "road"),
    m_run("(e)·(0.3 + D(e))·P(h;ctx(e))")])
P("Four z-standardized specifications follow: road-only (hierarchy, "
  "degree, lanes); attractor-only (station, nightlife, "
  "hotel/hospital, transit, taxi-stand kernels); the circulation "
  "proxy; and the combined score")
EQ([m_sub("S", "COMB"), m_run(" = z(z log(1+"), m_sub("P", "circ"),
    m_run(") + 0.5 "), m_sub("S", "road"), m_run(" + 0.4 "),
    m_sub("C", "ctx"), m_run(")")])
P("Each construction encodes a different theory of where a "
  "cruising taxi is likely to pass: the road-only specification "
  "treats hierarchy, connectivity, and capacity as sufficient "
  "information — the 'knowledgeable local' reading; the "
  "attractor-only specification treats origins and destinations "
  "— stations, nightlife, hotels and hospitals, transit nodes, "
  "existing stands — as sufficient; the circulation proxy couples "
  "the two through the kernel field and a period-weighted "
  "profile; and the combined score averages the three readings "
  "after z-standardization. None is privileged a priori, which "
  "is the point: they are alternative plausible readings of "
  "opportunity rather than competing predictive models, and the "
  "audit asks whether the locations they privilege agree. All "
  "are modeled public-data proxies — none is observed taxi "
  "availability — and their construction inherits the "
  "composite-index sensitivities documented elsewhere " +
  cite("oecd2008", "freudenberg2003") + ".")
H("2.5 Local pedestrian relocation optimization", 2)
P(f"{NOR} origins (seed {canon('config.seed')}); candidates are "
  "segments reachable within 100/200/300/500 m walking distance; "
  "the selected location maximizes the score over candidates, "
  "mirroring the marginal repositioning a passenger would "
  "actually perform. The 100-500 m radius range brackets the "
  "walk a hail passenger plausibly makes — short enough that "
  "most origins have many candidates, long enough that the "
  "candidate set grows superlinearly in dense networks. Because "
  "every radius re-optimizes, the radius sweep also functions "
  "as a dose-response check: a genuine structural advantage "
  "should grow smoothly with candidate-set size, whereas "
  "generic maximum-selection grows mechanically as well — "
  "which is why radii alone cannot separate the two.")
H("2.6 The self-optimization problem", 2)
P("If ", om([m_sub("S", "A"), m_run("(x)")]),
  " is the opportunity score and ",
  om([m_subsup("x", "A", "*"), m_run(" = argmax "), m_sub("x", "c"),
      m_run("∈N("), m_sub("x", "0"), m_run(") "), m_sub("S", "A"),
      m_run("("), m_sub("x", "c"), m_run(")")]),
  ", then")
EQ([m_sub("S", "A"), m_run("("), m_subsup("x", "A", "*"),
    m_run(") − "), m_sub("S", "A"), m_run("("), m_sub("x", "0"),
    m_run(") ≥ 0")])
P("holds by construction whenever a better-scoring candidate exists "
  "in ", om([m_run("N("), m_sub("x", "0"), m_run(")")]),
  ". Positive self-gain is therefore partly structural — an "
  "order-statistical property of optimizing a heterogeneous surface "
  "— and cannot alone validate the proxy. This is the central "
  "premise of the audit.")
H("2.7 Component ablation", 2)
P("Each specification is optimized separately. Ablation addresses "
  "whether apparent gains hinge on one particular construction "
  "choice (weights, kernels, components) — the same question "
  "specification-sensitivity work poses for composite indices " +
  cite("greco2019") + ", here asked of spatial scores. If apparent "
  "gains appeared only under the combined score, the composite "
  "weighting would be the suspect; if they appear under every "
  "construction, the phenomenon lies in optimization on "
  "heterogeneous surfaces itself rather than in any single design "
  "decision. The four specifications deliberately span two "
  "different information families — network hierarchy and "
  "destination kernels — so the ablation also feeds the transfer "
  "test of §2.8.")
H("2.8 Cross-specification transfer", 2)
P("The transfer gain ",
  om([m_run("TG(A→B) = "), m_sub("S", "B"), m_run("("),
      m_subsup("x", "A", "*"), m_run(") − "), m_sub("S", "B"),
      m_run("("), m_sub("x", "0"), m_run(")")]),
  " evaluates locations selected under specification A (selector) "
  "under a distinct specification B (evaluator). Off-diagonal "
  "transfer — especially between the road-only and attractor-only "
  "component families, which encode different information "
  "structures — is stronger internal evidence than self-gain, "
  "because it cannot be manufactured by the selection rule itself. "
  "Diagonal entries remain self-optimization. The distinction mirrors "
  "the difference between re-fitting under perturbed assumptions and "
  "transporting a conclusion to a different reasonable analysis "
  "pipeline " + cite("steegen2016") + ": a gain that exists only "
  "inside the family that produced it is evidence about that "
  "family, not about the city.")
H("2.9 Spatial permutation null", 2)
P("Scores are permuted across all hail-feasible segments (" +
  str(NPERM) +
  " repetitions). The null preserves the marginal score "
  "distribution, the network geometry, the origin distribution, and "
  "the candidate counts, while destroying the observed spatial "
  "arrangement " + cite("besag1977", "manly2007") + ". Because "
  "optimization rewards local variance, a scrambled surface with "
  "the same value distribution is not a straw man but a sharp "
  "benchmark: anything optimization does to it is attributable to "
  "generic heterogeneity plus selection, not to urban structure. "
  "It answers a specific question: how much improvement would "
  "optimization deliver on a surface with identical values but "
  "random placement? "
  "Observed improvement fractions and gain magnitudes are compared "
  "against the null with empirical ",
  om([m_run("p = (1 + #{null ≥ obs})/(1 + N)")]),
  ".")
P("Three outcomes are distinguishable. If observed statistics "
  "exceed the null on both prevalence and magnitude, the spatial "
  "arrangement carries exploitable information; if prevalence "
  "but not magnitude exceeds it, the arrangement adds a "
  "reliability edge but not larger wins; and if neither exceeds "
  "the null, the apparent gain is generic maximum-selection on a "
  "heterogeneous surface. The comparison is run per period and "
  "per radius because the answer need not be uniform across "
  "either.")
H("2.10 Constrained permutation sensitivity", 2)
P("A within-ward permutation preserves coarse geographic structure "
  "— the district-level organization a sceptic might credit with "
  "the gains — and tests whether the remaining fine-scale "
  "arrangement is still distinguishable from random. It is the "
  "more conservative of the two nulls.")
H("2.11 Heuristic comparators", 2)
P("Stay; random relocation (10 seeded draws); and the nearest "
  "major-class road, a meaningful domain heuristic because "
  "cruising taxis concentrate on arterials and a literate local "
  "needs no model to walk to one " + cite("yang2010") + ". "
  "Heuristics serve two audit roles: they bound how much added "
  "value the constructed score plausibly contributes beyond "
  "common knowledge, and they guard against the 'complexity "
  "premium' — the tendency to credit elaborate constructions "
  "for gains a trivial rule would have delivered.")
H("2.12 Cluster-aware statistical inference", 2)
P(f"Origin-period rows are repeated measurements, so naive "
  f"independence would overstate precision. Period-invariant "
  f"specifications use unique origins (n = {NR[0]:,}-{NR[1]:,}); "
  f"period-varying specifications use an origin-clustered "
  f"bootstrap ({canon('config.bootstrap_replicates'):,} "
  "replicates) and paired tests on origin-mean differences. "
  "Effects, confidence intervals, and p-values are reported "
  "together rather than p alone. The clustering matters "
  "practically: origins that start near high-opportunity areas "
  "improve less under any specification, so treating each "
  "origin-period row as independent would inflate effective "
  "sample size by roughly an order of magnitude.")
H("2.13 Reproducibility", 2)
P("Fixed seeds, raw-data snapshots with a SHA-256 ledger, public "
  "code, a canonical numerical registry that generates every "
  "printed analysis value, and machine-readable tables.")

H("3. Results")
H("3.1 Opportunity surfaces and local heterogeneity", 2)
P("All four surfaces are strongly heterogeneous, with ridges along "
  "arterials and station fronts (Figure 2). Heterogeneity is "
  "expected — and is precisely what makes local maxima easy to "
  "find.")
FIGURE("fig2_map", "Figure 2. Modeled street-hail opportunity "
       "surface (combined specification, SD units), weekday 17:00 "
       "and weekend 23:00.")
H("3.2 Apparent gains under self-optimization", 2)
P("Self-optimization produces large apparent gains (RQ1): "
  f"{pc(AB('COMB',100,'frac_pos'))}-{pc(AB('COMB',500,'frac_pos'))} "
  "of origins have a higher-scoring segment within reach, mean "
  f"gain {f2(AB('COMB',100,'mean_G'))}-{f2(AB('COMB',500,'mean_G'))} "
  "SD (Figure 3, Table 2; a worked example in Figure 4). These "
  "gains are partly structural by construction (§2.6).")
FIGURE("fig3_gain_by_radius", "Figure 3. Apparent self-optimization "
       "gains (SD units) by walking radius, combined specification.")
FIGURE("fig4_worked_example", "Figure 4. Local optimization "
       "example (200 m, weekday 17:00): apparent gain under the "
       "combined score.")
H("3.3 Comparison with simple heuristics", 2)
P("Large self-gains invite a sceptical first question: would "
  "any trivial spatial rule do the same? The heuristic "
  "comparison answers it. Against heuristics (RQ5): the combined optimum beats random "
  f"relocation in {pc(AB('COMB',300,'gt_rand'))} of origins at "
  f"300 m, and beats the nearest major road in "
  f"{pc(AB('COMB',300,'gt_nearmaj'))} of origins (paired surplus "
  f"{f2(AB('COMB',300,'diff_nearmaj'))} SD, clustered 95% CI "
  f"{cit(AB('COMB',300,'diff_nearmaj_ci'))}, Wilcoxon "
  f"{wp(AB('COMB',300,'wilcoxon_p'))}; Figure 5). The constructed "
  "score therefore contains spatial information beyond road "
  "hierarchy alone — an internal result that says nothing yet "
  "about real taxi encounters.")
FIGURE("fig5_strategies", "Figure 5. Mean modeled score by "
       "strategy (combined specification, radii pooled). Error "
       "bars = SEM.")
H("3.4 Component ablation", 2)
P(f"Apparent gains persist under every construction (RQ2): at "
  f"300 m, road-only {pc(AB('ROAD',300,'frac_pos'))}, "
  f"attractor-only {pc(AB('ATTR',300,'frac_pos'))}, proxy "
  f"{pc(AB('PROXY',300,'frac_pos'))}, combined "
  f"{pc(AB('COMB',300,'frac_pos'))} improved (Figure 6, Table 3). "
  "Segment rankings agree only moderately to strongly (Spearman "
  f"{f2(canon('agreement.spearman_min'))}-{f2(canon('agreement.spearman_max'))}): "
  "the constructions are alternative readings with varying degrees "
  "of agreement, and persistence is not proof of external "
  "validity.")
FIGURE("fig6_ablation", "Figure 6. Component ablation across "
       "walking radii.")
H("3.5 Cross-specification transfer", 2)
P("The ablation establishes that apparent gains are not an "
  "artefact of one construction; the transfer test asks the "
  "harder question of whether different constructions identify "
  "the same places. Transfer between conceptually distinct component families is "
  f"weak (RQ3): road-selected locations improve the attractor "
  f"score for {pc(TF('ROAD','ATTR','frac_pos'))} of origins "
  f"(mean {f2(TF('ROAD','ATTR','mean_TG'))} SD) and "
  "attractor-selected locations improve the road score for "
  f"{pc(TF('ATTR','ROAD','frac_pos'))} of origins "
  f"({f2(TF('ATTR','ROAD','mean_TG'))} SD) — showing "
  "weak directional consistency. Transfer into the proxy is stronger (attr→proxy "
  f"{pc(TF('ATTR','PROXY','frac_pos'))}; road→proxy "
  f"{pc(TF('ROAD','PROXY','frac_pos'))}) because the proxy embeds "
  "road hierarchy (Figure 7, Table 4). Weak off-diagonal transfer "
  "is itself a key finding: the constructions partly identify "
  "different, non-transferable structure.")
FIGURE("fig7_transfer_matrix", "Figure 7. Transfer matrix at "
       "300 m. Diagonal would be self-optimization; off-diagonal "
       "entries are internal transfer evidence.")
H("3.6 Spatial permutation null", 2)
P("The decisive test is whether the observed surface's spatial "
  "arrangement adds anything beyond generic heterogeneity. "
  "Against the unrestricted null (RQ4): improvement prevalence "
  "marginally exceeds permutation at 200-500 m (observed "
  f"{f3(PM('weekday_17','300','obs_frac'))} vs null "
  f"{f3(PM('weekday_17','300','null_frac'))} at 300 m; empirical "
  f"p={f2(RADR[0])}-{f2(RADR[1])} for the weekday-17 null) but "
  "not at 100 m (p=1.0). Mean gain magnitude does not exceed the "
  f"null at any radius (observed "
  f"{f2(PM('weekday_17','300','obs_gain'))} vs null "
  f"{f2(PM('weekday_17','300','null_gain'))} SD at 300 m; "
  "Figure 8, Table 5). A spatially unstructured surface with "
  "identical marginals produces larger local contrasts: most of "
  "the apparent gain is generic maximum-selection, while the "
  "observed surface's spatial autocorrelation " +
  cite("moran1950") + " actually compresses local maxima.")
FIGURE("fig8_permutation_null", "Figure 8. Observed statistics "
       f"(red) vs {NPERM}-permutation null (gray), 300 m, "
       "weekday 17:00.")
H("3.7 Constrained-null sensitivity", 2)
P("One possible rescue is that the important organization lives "
  "at district rather than segment scale. The within-ward and weekend-23 nulls reproduce the same "
  "pattern (marginal prevalence advantage at 200-500 m; observed "
  "magnitude below the null), so coarse district structure does "
  "not rescue the gain-magnitude claim.")
H("3.8 Temporal and district secondary analyses", 2)
P("Under the modeled temporal specifications, gains are largest "
  "in the weekday-morning period; the weekend specification "
  "shifts modeled opportunity toward nightlife contexts — "
  "input-profile consequences (Figure 9). Kernel bandwidth "
  "150/500 m leaves gains nearly unchanged "
  f"(rho {f2(canon('sigma.rho_150'))}/{f2(canon('sigma.rho_500'))}).")
FIGURE("fig9_heterogeneity", "Figure 9. Modeled gain by "
       "hour/day-type and ward/radius — model behavior, not "
       "observed patterns.")
H("3.9 Summary of evidence levels", 2)
P("Level 1 (self-optimization): large apparent gains — achieved. "
  "Level 2 (internal stress tests): ablation passed; transfer "
  "weak; heuristic contrast retained; permutation shows "
  "prevalence marginally above but magnitude below null. "
  "Level 3 (external empirical validation): not available in "
  "this study.")

H("4. Discussion")
H("4.1 Apparent optimization gain is not validation", 2)
P("The self-optimization inequality is structural: with ~hundreds "
  "of reachable candidates, a local maximum almost surely exceeds "
  "the origin. This is the spatial analogue of the statistical "
  "observation that selecting on the measured outcome inflates "
  "it " + cite("simmons2011", "gelman2014") + ". Composite-index "
  "research long ago documented that constructed scores encode "
  "their constructors' choices " + cite("freudenberg2003",
  "oecd2008", "greco2019") + "; the results here show the "
  "corresponding trap on the optimization side: large gains "
  "persist under every alternative construction we tested, yet "
  "persistence across constructions is not evidence that any of "
  "them describes the world. The practical lesson is not that "
  "gains exist — it is that their size carries almost no "
  "validating information. The same logic explains why "
  "optimization results are so persuasive in practice: the "
  "numbers are real, correctly computed, and often large — "
  "what they lack is a baseline of what optimization "
  "delivers by construction. A useful analogy is the distinction "
  "between internal and external validity in the causal-inference "
  "literature: a pipeline can be internally consistent — correctly "
  "optimized, correctly measured — while telling us nothing about "
  "the target domain, because the criterion by which success is "
  "judged is a construction, not an observation.")
H("4.2 Cross-specification transfer as a stronger internal test", 2)
P("The road-only and attractor-only specifications encode "
  "different information structures — network hierarchy versus "
  "destination kernels — so transfer between them tests whether a "
  "selected location is preferable under a genuinely different "
  "plausible reading of opportunity. Positive but limited "
  "transfer means the two families partly identify different "
  "places: an improvement under one public-data reading of "
  "'opportunity' shows weak cross-specification consistency under "
  "the other. This is "
  "distinct from parameter sensitivity " + cite("saltelli2008") +
  ": a spec curve perturbs coefficients within one family, "
  "whereas transfer asks whether the answer generalizes across "
  "families — closer in spirit to the multiverse question of "
  "whether conclusions survive reasonable analyst variation " +
  cite("steegen2016", "simonsohn2020") + ". Transfer alone does "
  "not prove validity; weak transfer does, however, falsify the "
  "strong claim that the proxy identifies structure all "
  "reasonable constructions share.")
H("4.3 Spatial nulls and generic heterogeneity", 2)
P("The decisive result is comparative: a shuffled surface "
  f"reproduces ≈{pc(canon('permutation.null_reproduces_frac_mean'))} "
  "of the observed improvement prevalence on average across the "
  "examined radii (null/observed ratio "
  f"{f2(canon('permutation.null_reproduces_frac_range')[0])}-"
  f"{f2(canon('permutation.null_reproduces_frac_range')[1])}) and "
  "produced larger mean gain magnitudes. The mechanism is "
  "order-statistical: optimizing over many candidates rewards "
  "variance, and the real surface's positive spatial "
  "autocorrelation " + cite("moran1950", "getis1992") +
  " suppresses the local contrast a scrambled one enjoys. "
  "Monte-Carlo nulls have a long history in spatial-pattern "
  "inference " + cite("besag1977", "manly2007", "anselin1995") +
  "; using them here reframes 'how much did optimization gain?' "
  "into 'how much gain would any heterogeneous surface deliver?'. "
  "What the real urban surface contributes is a marginal "
  "reliability edge — not bigger wins — so its fine-scale "
  "arrangement adds little for relocation purposes. It is worth "
  "stressing what this is not: the null does not 'beat' the model "
  "in any operational sense, because neither surface is validated "
  "against encounters; the comparison instead locates where the "
  "apparent gain comes from. A prevalence edge of a few percentage "
  "points at mid-range radii is the entire observed margin — a "
  "finding that would be invisible if only the headline self-gain "
  "had been reported.")
P("The autocorrelation direction deserves emphasis because it "
  "cuts against intuition. Readers schooled on Moran's I or "
  "LISA " + cite("moran1950", "anselin1995") + " might expect "
  "spatial clustering to help local optimization — clusters "
  "mean predictable hot spots. For relocation the opposite "
  "holds locally: autocorrelation means an origin already sits "
  "on values similar to its neighbours, so the local maximum "
  "is only modestly higher; a scrambled surface places extreme "
  "values arbitrarily close. Optimization gain is therefore "
  "anti-correlated with the surface's own organization — an "
  "interpretation that could not have been made without the "
  "permutation comparison.")
H("4.4 Why heuristic superiority is insufficient", 2)
P("The combined optimum's surplus over the nearest major road "
  "shows the score encodes information beyond hierarchy — a real, "
  "if narrow, computational finding, since road-hierarchy "
  "knowledge is what an unaided user can deploy for free " +
  cite("yang2010") + ". But benchmark-beating is still internal "
  "evidence: decision-support evaluation normally requires "
  "comparison against realized outcomes, which do not exist "
  "here. The honest statement is that the model earns its "
  "complexity relative to the free heuristic without any "
  "demonstration that either achieves real encounters. The "
  "benchmark does set a useful calibration anchor: if a proposed "
  "proxy cannot beat the free heuristic, the case for its "
  "complexity collapses immediately — a cheap test that many "
  "index-optimization pipelines skip.")
H("4.5 From sensitivity analysis to falsification-oriented "
  "proxy auditing", 2)
P("Sensitivity analysis asks whether the answer changes when "
  "assumptions change " + cite("saltelli2008") + "; the framework "
  "here asks whether the apparent benefit survives tests "
  "designed to undermine the naive interpretation — a "
  "falsification orientation closer to the multiverse/" 
  "specification-curve programme " + cite("steegen2016",
  "simonsohn2020") + " and to randomization inference " +
  cite("manly2007") + " than to classical sensitivity analysis. "
  "The resulting workflow is compact (Figure 1): CONSTRUCT one "
  "or more plausible proxy surfaces; OPTIMIZE candidate "
  "locations; ABLATE components to test specification "
  "dependence; TRANSFER selected locations across alternative "
  "specifications; NULL-TEST against spatially permuted or "
  "otherwise structured nulls; BENCHMARK against simple domain "
  "heuristics; CALIBRATE claims to the evidence level that "
  "survives. It is an internal, falsification-oriented audit — "
  "a practical workflow, not a universal standard. Two design "
  "principles underlie it. First, tests should be destructive "
  "by intent: each stage is built to break the naive reading "
  "(that optimization gain implies spatial knowledge), not to "
  "corroborate it. Second, calibration is explicit: claims are "
  "stated at the level of evidence that survives (§3.9), so a "
  "pipeline that passes ablation but fails transfer and null "
  "tests licenses exactly the modest claim the residual "
  "evidence supports. Applied here, the workflow converted a "
  "superficially strong result — near-universal improvement "
  "with large effect sizes — into the accurate statement that "
  "the surface's fine-scale arrangement contributes little "
  "beyond generic heterogeneity.")
H("4.6 Implications for urban accessibility research", 2)
P("The problem class is broad: accessibility indices " +
  cite("hansen1959", "handy1997", "geurs2004") + ", "
  "cumulative-opportunity and space-time measures " +
  cite("kwan1998", "miller1999") + ", composite urban scores " +
  cite("oecd2008", "greco2019") + ", transit and destination "
  "accessibility surfaces " + cite("mavoa2015", "shen1998") +
  ", and mobility-availability proxies all share the same "
  "inferential structure — a constructed score optimized where "
  "outcome labels are sparse. Nothing here invalidates "
  "proxy-based planning; the narrower claim is that proxy "
  "optimization requires stronger validation than within-score "
  "improvement, and that the three internal tests used here "
  "are cheap to add to such pipelines. For accessibility "
  "measurement in particular — where debates about metric and "
  "scale choice are long-running " + cite("handy1997", "kwan1998") +
  " — the transfer and null tests offer a way to ask whether a "
  "metric choice changes not just the estimated accessibility but "
  "the locations optimization would actually select.")
P("There is also a constructive implication. The tests are "
  "ordinal and comparative rather than calibrated, so they "
  "compose naturally with the existing accessibility toolkit: a "
  "cumulative-opportunity surface or a transit accessibility "
  "index " + cite("geurs2004", "mavoa2015") + " can be carried "
  "through the same audit, and a siting recommendation that "
  "survives transfer and null tests is materially stronger than "
  "one that only reports its own score improvement. Where the "
  "audit fails, the honest remedy is external data or "
  "explicitly discounted claims — not a more elaborate proxy.")
H("4.7 Prospective infrastructure siting under no-label "
  "conditions", 2)
P("The same constraint appears, sharper, when infrastructure is "
  "prospective and historical outcome labels cannot exist. "
  "Alternative-fuel station planning formalized this as "
  "flow-based siting on networks " + cite("kuby2009",
  "kuby2009b") + "; public charging-station deployment is "
  "optimized under demand uncertainty " + cite("he2013") + "; "
  "and hydrogen-refueling planning has long proceeded from "
  "modeled demand surfaces in the absence of any realized "
  "demand " + cite("nicholas2004") + ". In each "
  "case planners must optimize a constructed proxy for an "
  "outcome that has not yet been observed — precisely the "
  "setting in which internal stress tests of the kind "
  "demonstrated here can reduce overinterpretation until "
  "external outcomes become available. The present framework "
  "does not solve siting; it disciplines the claims a "
  "proxy-optimization pipeline can honestly make.")
H("4.8 Street-hail taxis as a motivating case", 2)
P("The taxi case is scientifically useful because it combines "
  "three features: a genuinely spatial passenger decision " +
  cite("yang2010", "wong2008") + ", proprietary operational "
  "data — the telemetry behind T-Finder and trajectory-demand "
  "systems " + cite("tfinder", "taxi_demand", "zheng2010",
  "yuan2011") + " — and a strong temptation to substitute "
  "public proxies for the missing observations " +
  cite("taxi_stand", "hakusyo2025") + ". The paper is therefore "
  "not an operational validation of a recommendation system; "
  "the case makes the proxy-optimization problem concrete.")
P("The bilateral-search tradition offers a complementary "
  "reading of the null result: search equilibrium models make "
  "encounter probability depend on both cruising supply and "
  "searching demand on the same network " + cite("yang2002",
  "wong2008") + ", and no static public-data surface can "
  "capture that two-sided dynamic. The stress tests here do "
  "not assume such a model; they ask only whether the static "
  "proxy's own structure does any work, and answer 'very "
  "little'.")
H("4.9 Limitations", 2)
P("No observed vacant-taxi ground truth; no actual waiting-time "
  "outcomes; scores are uncalibrated public-data proxies; "
  "temporal structure is partly modeled from the monitor "
  "profile; Tokyo specificity limits generalization; roadside "
  "hail feasibility is imperfectly represented; the station "
  "term is unweighted (FY2023 N02 lacks passenger counts); the "
  "proxy constructions share inputs and are not fully "
  "independent; cross-specification transfer is internal "
  "evidence only; and permutation conclusions depend on the "
  "null definition — the within-ward variant mitigates but "
  "does not eliminate this dependence. Two limitations cut "
  "deeper than the rest. First, all four specifications are "
  "built from the same underlying data universe — the same OSM "
  "network and POIs — so even 'distinct' constructions share "
  "errors the audit cannot see; cross-specification transfer "
  "tests construction-family dependence, not data-universe "
  "dependence. Second, the audit's nulls are value-permutations "
  "on a fixed network; richer constrained nulls (e.g. "
  "autocorrelation-preserving surrogates) could sharpen the "
  "prevalence comparison, and the choice of null remains a "
  "specification decision of its own — the same caveat the "
  "MAUP literature raises for representation choice " +
  cite("fotheringham1991", "jelinski1996") + ".")
H("4.10 Requirements for external empirical validation", 2)
P("Before any operational interpretation, external evidence "
  "would require observed vacant-taxi passage, actual waiting "
  "times, or prospective passenger outcomes.")

H("5. Conclusion")
P("Optimization performance and proxy validity are not "
  "equivalent. A constructed surface's susceptibility to "
  "optimization is a property of its heterogeneity and "
  "representation, not of its correspondence to the world. In a "
  "street-hail relocation audit built entirely "
  "on public data, large within-score optimization gains did not "
  "translate into equally strong cross-specification evidence "
  "and were partly reproducible under spatially permuted null "
  "surfaces: self-optimization alone is insufficient validation "
  "of a constructed urban opportunity proxy. Component "
  "ablation, cross-specification transfer, spatial-null "
  "comparison, and simple heuristic benchmarking together form "
  "a practical falsification-oriented stress-test framework for "
  "such studies — a checklist for what an apparent gain must "
  "survive before it is interpreted as structure rather than "
  "as selection. The caution applies beyond taxis: accessibility "
  "indices, amenity scores, and mobility proxies are routinely "
  "optimized wherever outcome labels are absent, and it becomes "
  "acute for prospective infrastructure whose outcomes cannot "
  "yet be observed. What remains unresolved — as it must be, "
  "here — is external validation against realized outcomes: "
  "observed encounters, waiting times, or prospective passenger "
  "results. Until then, the disciplined claim is the narrow but "
  "useful one — the audit framework exposes the distinction "
  "between apparent optimization gain and transferable spatial "
  "structure, and on this case it reports that apparent success can coexist with "
  "weak evidence of transferable spatial structure. For studies "
  "that build, rather than observe, their surfaces, that "
  "combination of ambition and restraint is the defensible "
  "default.")

H("Declarations")
P("Data availability: all inputs are public datasets (Table 1); "
  "preprocessing and analysis code, the canonical numerical "
  "registry, and machine-readable result tables are openly "
  "available at "
  "https://github.com/bougtoir/street-hail-taxi-accessibility. "
  "Competing interests: none declared. Funding: none.")

H("References")
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

doc.save(f"{OUT}/CEUS_MAIN_MANUSCRIPT_LITERATURE_FINAL_inline.docx")
print("LITERATURE_FINAL manuscript saved;", len(REFS), "references")

hl = Document(); hl.add_heading("Highlights", 0)
for b in [
    "Self-optimized urban proxies can yield large apparent local gains",
    "Cross-specification transfer can reveal weakly transferable structure",
    "Spatial permutation quantifies gains caused by generic heterogeneity",
    "Internal stress tests help audit urban proxies without outcome labels",
    "Street-hail relocation shows the framework without fleet telemetry",
]:
    hl.add_paragraph(b, style="List Bullet")
hl.save(f"{OUT}/CEUS_HIGHLIGHTS_LITERATURE_FINAL.docx")

c = Document()
c.add_paragraph("Dear Editors,")
c.add_paragraph(
    "I submit 'Stress-testing public-data urban accessibility proxies: "
    "street-hail taxi relocation without fleet telemetry' for "
    "consideration in Computers, Environment and Urban Systems.")
c.add_paragraph(
    "The paper addresses a methodological problem that is pervasive in "
    "urban-computing research. Constructed spatial proxies — "
    "accessibility indices, amenity and opportunity surfaces, "
    "availability maps — are routinely optimized wherever direct "
    "operational ground truth is proprietary, expensive, or not yet "
    "observable. Because a heterogeneous constructed surface contains "
    "local maxima almost mechanically, optimizing a proxy under its own "
    "score produces apparent gains that are partly structural. Within-"
    "score optimization gain is therefore not validation, yet it is "
    "frequently reported as if it were.")
c.add_paragraph(
    "I demonstrate this using street-hail taxi relocation as a "
    "motivating case in which the relevant ground truth — vacant-taxi "
    "telemetry — is genuinely unavailable. Four plausible public-data "
    "opportunity surfaces are constructed on the directed road network "
    "of Tokyo's five central wards, and relocation optimization is "
    "audited over 2,000 origins at 100-500 m walking radii. Apparent "
    "gains are large (98% of origins improved, mean 1.50 SD at 300 m) "
    "and exceed the nearest-major-road heuristic in 81% of origins. "
    "But the internal stress tests then overturn the naive reading: "
    "cross-specification transfer between the road-only and "
    "attractor-only component families is weak (53% and 43% of origins "
    "positive — weak cross-specification consistency), and spatially "
    "permuted surfaces with "
    "identical marginals reproduce improvement prevalence almost fully "
    "while producing larger gain magnitudes — the observed surface's "
    "spatial autocorrelation actually compresses local maxima.")
c.add_paragraph(
    "The contribution is a practical falsification-oriented workflow — "
    "construct, optimize, ablate, transfer, null-test, benchmark, "
    "calibrate the claim — that asks not whether a proxy answer "
    "changes under perturbation but whether it survives tests designed "
    "to undermine the naive interpretation. For CEUS readers working "
    "with accessibility indices, composite urban scores, and "
    "geospatial decision support, the results quantify why "
    "within-proxy gain is weak evidence and offer concrete internal "
    "tests that are cheap to add to existing pipelines. The argument "
    "is sharpest for prospective infrastructure siting — "
    "alternative-fuel and charging-station planning being the "
    "canonical cases — where realized outcome labels cannot yet exist "
    "and proxy optimization is unavoidable.")
c.add_paragraph(
    "The street-hail case is deliberately chosen: the passenger's "
    "problem is concretely spatial, fleet telemetry is proprietary, "
    "and public spatial data are a tempting substitute — exactly the "
    "conditions under which the circular-validation risk is easiest "
    "to overlook. All inputs are public datasets, and preprocessing "
    "and analysis code with machine-readable result tables are openly "
    "available at "
    "https://github.com/bougtoir/street-hail-taxi-accessibility.")
c.add_paragraph(
    "The manuscript is original, involves no human subjects, is not "
    "under consideration elsewhere, and reports its unfavorable "
    "internal-test findings without reservation. I declare no "
    "competing interests and received no funding for this work.")
c.add_paragraph("Sincerely,\nOnishi Tatsuki")
c.save(f"{OUT}/CEUS_COVER_LETTER_LITERATURE_FINAL.docx")
print("cover letter + highlights saved")
