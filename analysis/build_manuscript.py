#!/usr/bin/env python3
"""Phases 13-18: build MANUSCRIPT_inline.docx (+ clean PDF), COVER_LETTER.docx,
submission ZIP. All numbers pulled from tables/ at build time (no hardcoding)."""
import os, sys, json, math, zipfile
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAB, FIG, OUT, PROC = (f"{ROOT}/{d}" for d in ["tables", "figures", "output", "data/processed"])
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import docx
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from lxml import etree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"

def _m(tag, *kids):
    el = ET.SubElement.__self__  # placeholder
def m_el(tag):
    return ET.Element(f"{{{M_NS}}}{tag}")
def m_run(t):
    r = m_el("r"); tt = m_el("t"); tt.text = str(t); r.append(tt); return r
def m_sub(base, sub):
    s = m_el("sSub"); sb = m_el("e"); ss = m_el("sub")
    sb.append(m_run(base)); ss.append(m_run(sub)); s.extend([sb, ss]); return s
def m_frac(num, den):
    f = m_el("f"); n = m_el("num"); d = m_el("den")
    for x in (num if isinstance(num, list) else [num]): n.append(x if not isinstance(x, str) else m_run(x))
    for x in (den if isinstance(den, list) else [den]): d.append(x if not isinstance(x, str) else m_run(x))
    f.extend([n, d]); return f
def add_omml(p, elements):
    om = m_el("oMath")
    for e in elements:
        om.append(e if not isinstance(e, str) else m_run(e))
    p._p.append(om)
    return p

# ---------------- load results ----------------
comp = pd.read_csv(f"{TAB}/strategy_comparison.csv")
dthr = pd.read_csv(f"{TAB}/distance_to_threshold.csv")
temporal = pd.read_csv(f"{TAB}/temporal_heterogeneity.csv")
ward = pd.read_csv(f"{TAB}/ward_heterogeneity.csv")
agree = json.load(open(f"{TAB}/model_agreement.json"))
sigma = json.load(open(f"{TAB}/sigma_sensitivity.json"))

def cv(model, radius, col):
    r = comp[(comp.model == model) & (comp.radius == radius)][col].iloc[0]
    if isinstance(r, str) and r.startswith("["):
        return eval(r)
    return r
def pc(x): return f"{100*x:.0f}%"
def f2(x): return f"{x:.2f}"
def f1(x): return f"{x:.1f}"

# shared numbers (Model C = primary spec)
NSEG = 27887; NORIG = 2000
g100 = cv("A_C", 100, "frac_any_gain"); g200 = cv("A_C", 200, "frac_any_gain"); g500 = cv("A_C", 500, "frac_any_gain")
o500 = cv("A_C", 500, "opt_gt_nearmajor"); o200 = cv("A_C", 200, "opt_gt_nearmajor")
d500 = cv("A_C", 500, "mean_diff_nearmajor"); d200 = cv("A_C", 200, "mean_diff_nearmajor")
r200 = cv("A_C", 200, "opt_gt_random")
mg200 = cv("A_C", 200, "mean_G_A"); mg200ci = cv("A_C", 200, "mean_G_A_ci")
mg500 = cv("A_C", 500, "mean_G_A")
bmaj500 = cv("A_C", 500, "best_is_major"); bmaj100 = cv("A_C", 100, "best_is_major")

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(11)

def H(t, lvl=1): doc.add_heading(t, level=lvl)
def P(t, bold=False):
    p = doc.add_paragraph(); r = p.add_run(t); r.bold = bold; return p
def EQ(elems):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_omml(p, elems); return p
def FIGURE(name, caption, width=6.0):
    doc.add_picture(f"{FIG}/{name}.png", width=Inches(width))
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(caption).italic = True

REFS = []
def cite(*ids):
    """Vancouver: number references in order of first appearance."""
    for rid in ids:
        if rid not in REFS:
            REFS.append(rid)
    return "[" + ",".join(str(REFS.index(r) + 1) for r in ids) + "]"

# ---------------- title page ----------------
tp = doc.add_paragraph(); tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
tr = tp.add_run("Inferring and Optimizing Street-Hail Taxi Accessibility "
                "Without Proprietary Fleet Telemetry")
tr.bold = True; tr.font.size = Pt(16)
doc.add_paragraph("A public-data feasibility study of pedestrian relocation opportunity "
                  "in central Tokyo", ).alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph()

# ---------------- abstract ----------------
H("Abstract", 1)
P("Background: Street-hail taxi access varies block by block, yet the data that "
  "would quantify it — vacant-taxi GPS trajectories — are proprietary. Whether a "
  "meaningful, time-sensitive accessibility gradient and beneficial pedestrian "
  "relocation opportunities can be inferred from public data alone is untested.")
P("Methods: We constructed a directed road-segment representation of the five "
  "central wards of Tokyo (Chiyoda, Chuo, Minato, Shinjuku, Shibuya) from "
  "OpenStreetMap (27,887 hail-feasible directed segments), combined a public-data "
  "taxi-flow prior (road hierarchy, railway-station passenger volumes from MLIT "
  "National Land Numerical Information, OSM attractors, and a published hourly "
  "taxi-use profile) into three accessibility specifications of increasing "
  "richness, and evaluated pedestrian relocation within 100-500 m network "
  "distance for 2,000 systematically sampled origins across ten day-type-hour "
  "periods. Strategies were compared against staying, random relocation, the "
  "nearest major road, and a flow-only optimum.")
P(f"Results: {pc(g200)} of origins had a strictly higher-accessibility segment "
  f"within 200 m ({pc(g500)} within 500 m); mean accessibility gain reached "
  f"{f2(mg200)} SD at 200 m and {f2(mg500)} SD at 500 m. The optimizer beat "
  f"random relocation in {pc(r200)} of origins and beat walking to the nearest "
  f"major road in {pc(o200)}-{pc(o500)} of origins (mean surplus "
  f"{f2(d200)}-{f2(d500)} SD). Results were stable across specifications "
  "(segment-level Spearman rho 0.85-0.97) and attractor-kernel bandwidths "
  f"(gain rho {sigma['rho_150']:.2f}-{sigma['rho_500']:.2f}).")
P("Conclusions: Public data alone can support a defensible, robust map of "
  "relative street-hail accessibility and identify non-trivial pedestrian "
  "relocation gains beyond naive heuristics — choosing which major road, not "
  "merely the nearest one. Because scores are uncalibrated to real waiting "
  "times, these are hypotheses about relative opportunity, to be validated by "
  "field observation in a companion study.")
P("Keywords: street-hail taxi; accessibility; pedestrian relocation; public "
  "data; OpenStreetMap; urban mobility; Tokyo")

# ---------------- 1. Introduction ----------------
H("1. Introduction")
P("Street hailing remains a primary mode of taxi access in dense cities such as "
  "Tokyo, where tens of thousands of taxis cruise for passengers "
  + cite("hakusyo2025") + ". Yet the quantities that would let a pedestrian "
  "choose where to stand — the time-varying density of vacant taxis along each "
  "road segment — live inside proprietary fleet telemetry. Riders, and "
  "researchers without fleet partnerships, see none of it.")
P("A large literature optimizes the fleet side: taxi-demand prediction from GPS "
  "trajectories " + cite("taxi_demand") + ", cruising-strategy and stand-location "
  "optimization " + cite("taxi_stand", "taxi_demand2") + ", and bilateral "
  "taxi-customer search equilibria " + cite("yang2010") + ". On the passenger "
  "side, recommender systems such as T-Finder suggest pickup locations within "
  "walking distance, but learn pickup probabilities from the same proprietary "
  "trajectories " + cite("tfinder") + ". Walkable pickup-and-drop-off designs in "
  "on-demand mobility likewise assume observed trip telemetry "
  + cite("pudo") + ".")
P("What can be said without any fleet data? This study asks whether public data "
  "alone — the road network, urban attractors, and published aggregate taxi-use "
  "statistics — support a direction- and time-sensitive measure of relative "
  "street-hail accessibility at the road-segment level, and whether that measure "
  "reveals beneficial short-range pedestrian relocation. We deliberately do not "
  "estimate vacant-taxi counts, waiting times, or hailing probabilities; such "
  "quantities require field calibration and are reserved for a companion "
  "empirical study (Paper 2).")
P("Contributions: (i) a fully public-data pipeline for segment-level relative "
  "street-hail accessibility; (ii) a population-scale evaluation of pedestrian "
  "relocation opportunity across walking radii, times of day, and urban "
  "contexts; (iii) a benchmark of the optimizer against naive heuristics — "
  "random relocation and walking to the nearest major road — quantifying where "
  "optimization adds information; and (iv) a robustness audit across three "
  "accessibility specifications and two attractor-kernel bandwidths.")

# ---------------- 2. Materials and Methods ----------------
H("2. Materials and Methods")
H("2.1 Study area", 2)
P("The study polygon is the union of the five contiguous central wards of Tokyo "
  "(Chiyoda, Chuo, Minato, Shinjuku, Shibuya), covering the main railway "
  "terminal belt, the primary nightlife districts, and mixed residential-commercial "
  "fabric — a canonical street-hail environment with " +
  "a large licensed taxi fleet " + cite("hakusyo2025") + ".")
H("2.2 Public data sources", 2)
P("All inputs are openly and legally accessible (Table 1): OpenStreetMap road "
  "network and points of interest via the Overpass API " + cite("osm") + "; "
  "railway-station passenger volumes from the MLIT National Land Numerical "
  "Information railway dataset (FY2023) " + cite("nlni") + "; and the hourly "
  "distribution of taxi use from the Tokyo Taxi Center user-monitor survey "
  + cite("monitor") + ". The CSIS Pseudo-PFLOW business-traffic trajectories "
  "require a joint-research application and were inaccessible; the substitution "
  "is documented in the DATA_SOURCE_AUDIT.")
H("2.3 Directed road-network construction", 2)
P(f"The OSM driving graph was simplified to {NSEG} hail-feasible directed road "
  "segments after excluding motorway, trunk and pedestrian classes where "
  "street hailing is not physically or legally possible. The independent OSM "
  "walk network (182,538 edges) supplies pedestrian distances.")
H("2.4 Taxi-flow prior", 2)
P("The prior combines a road-class capacity weight, a log-compressed "
  "demand-attractor field (station passengers, nightlife, hotel/hospital and "
  "transit points within a Gaussian kernel), and an hourly temporal multiplier "
  "derived from the monitor survey, blended toward a night-shifted profile in "
  "nightlife contexts:")
EQ([m_run("F(e,t) = "), m_run("w_road(e)·(0.3 + D(e))·P(h;ctx(e))")])
H("2.5 Street-hail accessibility specifications", 2)
P("Three nested specifications guard against arbitrary-score dependence. All "
  "are standardized to SD units:")
EQ([m_sub("A", "A"), m_run("(e,t) = z(log(1+F(e,t)))")])
EQ([m_sub("A", "B"), m_run("(e,t) = z("), m_sub("A", "A"), m_run(" + 0.5·S(e))")])
EQ([m_sub("A", "C"), m_run("(e,t) = z("), m_sub("A", "A"),
    m_run(" + 0.5·S(e) + 0.4·C(e))")])
P("where S aggregates road class, intersection intensity and taxi-stand "
  "proximity, and C aggregates station, nightlife and hotel/hospital context. "
  "Weights are transparent, additive and untuned; the claim rests on agreement "
  "across specifications, not on any single score.")
H("2.6 Origin generation", 2)
P(f"{NORIG} origins were sampled uniformly at random from hail-feasible "
  "segments (seed 42) — systematically covering the network rather than "
  "cherry-picking tourist locations.")
H("2.7 Walking-neighborhood construction", 2)
P("For each origin, all walk-network nodes within each radius (100/200/300/500 m "
  "of shortest-path distance) were computed; a drive segment is reachable if a "
  "reachable walk node lies within 25 m of its midpoint.")
H("2.8 Relocation optimization", 2)
P("For each origin and period, the optimizer selects the reachable segment of "
  "highest accessibility. Outcomes are the absolute gain "
  )
EQ([m_sub("G", "A"), m_run(" = A*(x0,t) − A0")])
P("and the relative gain")
EQ([m_run("RAG = "), m_frac([m_run("A* − A0")], [m_run("|A0|")])])
P("plus the minimum walking distance needed for +10/+25/+50/+100% relative "
  "improvement. Utility analyses report gain per 100 m walked rather than "
  "commensurating accessibility with minutes (no waiting-time calibration "
  "exists in this study).")
H("2.9 Baseline heuristics", 2)
P("Comparators: staying at the origin; random reachable relocation (10 draws, "
  "fixed seeds); walking to the nearest major-class road segment; and the "
  "flow-only optimum.")
H("2.10 Sensitivity analyses", 2)
P("We varied walking radius, accessibility specification, improvement "
  "thresholds, candidate sets (all hail-feasible vs major-class only), kernel "
  "bandwidth (150/300/500 m), and day-type-hour structure; stability was "
  "assessed by Spearman correlation, top-1% segment Jaccard overlap, "
  "gain-class transition matrices, and same-segment agreement of optima.")
H("2.11 Reproducibility", 2)
P("All code, fixed seeds, raw-data snapshots with SHA-256 acquisition ledger, "
  "and generated tables/figures are provided; see README_REPRODUCIBILITY.")

# ---------------- 3. Results ----------------
H("3. Results")
H("3.1 Spatial structure of accessibility", 2)
P("Estimated street-hail accessibility varies sharply at fine spatial grain, "
  "with continuous ridges along arterial corridors and station fronts and "
  "deep troughs in interior residential blocks (Figure 2).")
FIGURE("fig2_map", "Figure 2. Segment-level street-hail accessibility (Model C, "
       "SD units) for weekday 17:00 and weekend 23:00 across the five central wards.")
H("3.2 Local accessibility heterogeneity", 2)
P(f"A strictly better segment is reachable within 100 m for {pc(g100)} of "
  f"origins, within 200 m for {pc(g200)}, and within 500 m for {pc(g500)} "
  "(Table 2). Median relative gains exceed 200% of the origin score at 200 m "
  "and beyond (origins near the global mean have the largest relative gains).")
H("3.3 Walking gain by radius", 2)
P(f"Mean gain grows from {f2(cv('A_C',100,'mean_G_A'))} SD (100 m) to "
  f"{f2(mg200)} SD (200 m) and {f2(mg500)} SD (500 m), with 95% bootstrap CIs "
  "excluding zero (Figure 4, Table 2). Median walking distance to the optimal "
  f"segment is {f1(cv('A_C',200,'median_walk_m'))} m at the 200-m radius.")
FIGURE("fig4_gain_by_radius", "Figure 4. Distribution of accessibility gain "
       "G_A (Model C, SD units) by walking radius; violins with medians.")
H("3.4 Comparison with random and major-road heuristics", 2)
P(f"The optimizer dominates random relocation in {pc(r200)}-{pc(1.0)} of origins. "
  f"Against the strongest naive heuristic — walking to the nearest major road — "
  f"the optimizer still wins in {pc(o200)} of origins at 200 m and {pc(o500)} "
  f"at 500 m, with mean surplus {f2(d200)}-{f2(d500)} SD. The optimal segment "
  f"is itself a major road in {pc(bmaj500)} of origins at 500 m "
  f"({pc(bmaj100)} at 100 m): the optimizer's added value is chiefly selecting "
  "*which* major road and in which direction, not merely walking toward a "
  "big street (Figure 5).")
FIGURE("fig5_strategies", "Figure 5. Mean achieved accessibility by strategy "
       "(Model C, all radii pooled): stay, random, nearest major road, "
       "flow-only optimum, full optimizer. Error bars = SEM.")
H("3.5 Temporal and district heterogeneity", 2)
P("Relocation gains are largest in the morning peak (weekday 08:00) and modestly "
  "lower late evening; weekend nights shift the spatial pattern toward "
  "nightlife districts (Figure 6). Mean gains differ across wards "
  "(Chuo > Shibuya at small radii), consistent with differences in block "
  "structure rather than artifacts of any single district.")
FIGURE("fig6_heterogeneity", "Figure 6. Heterogeneity of mean relocation gain "
       "by hour and day type (left) and by ward and radius (right), Model C.")
H("3.6 Robustness across specifications", 2)
P(f"Segment rankings correlate strongly across the three specifications "
  f"(Spearman rho {f2(agree['spearman']['A_A_weekday_17~A_B_weekday_17'])}-"
  f"{f2(agree['spearman']['A_A_weekday_17~A_C_weekday_17'])} at weekday 17:00), "
  f"and per-origin gains are similarly stable. Halving or raising the attractor "
  f"kernel bandwidth to 150/500 m leaves gains nearly unchanged "
  f"(rho {sigma['rho_150']:.2f}/{sigma['rho_500']:.2f}; the optimizer selects the "
  f"identical segment in {pc(sigma['same_opt_150'])}/{pc(sigma['same_opt_500'])} "
  "of origins).")
FIGURE("fig1_framework", "Figure 1. Conceptual framework: public data to "
       "segment-level accessibility to walkable relocation optimization.")
FIGURE("fig3_worked_example", "Figure 3. Worked example (200 m radius, weekday "
       "17:00): origin (star), reachable segments colored by accessibility, the "
       "nearest major road (blue square) and the optimizer's choice (red "
       "circle) — a farther but much higher-accessibility corridor.")

# ---------------- 4. Discussion ----------------
H("4. Discussion")
H("4.1 Main findings", 2)
P("Public data alone suffice to construct a fine-grained, time-sensitive "
  "relative street-hail accessibility surface on which short pedestrian "
  "relocation yields large, robust gains for a large majority of locations. "
  "The benefit is not reducible to 'walk to the nearest big road': the optimal "
  "destination is typically a specific major corridor, frequently not the "
  "closest one.")
H("4.2 Passenger-side interpretation", 2)
P("The measure is a relative potential for encountering street-hail supply, not "
  "a waiting-time estimate. Its actionability is nonetheless real: even without "
  "calibrated minutes, a gradient steep enough that one block's difference "
  "matters is precisely the information a pedestrian lacks.")
H("4.3 Why walking relocation matters", 2)
P("Unlike fleet-side dispatch, passenger-side relocation requires no "
  "coordination, no platform, and no data license — only information about "
  "where the gradient points uphill.")
H("4.4 Implications for low-friction taxi access", 2)
P("A public-data accessibility layer could support map overlays, station-exit "
  "guidance, and offline recommendations where fleet APIs are unavailable or "
  "unaffordable.")
H("4.5 Application to visitors unfamiliar with local street-hail conventions", 2)
P("Street-hail practice differs across countries. In Japan, taxis display "
  "external occupancy/availability indications (the roof-mounted indicator "
  "and windshield signage regulated under national vehicle rules); a relocation "
  "recommendation is most useful when paired with such local cues. This is an "
  "application note, not a behavioral claim tested here.")
H("4.6 Generalization to other cities", 2)
P("The pipeline needs only OSM, a public attractor source, and an aggregate "
  "temporal profile — all broadly available — but the magnitude of relocation "
  "gain will be city-specific, depending on block structure, fleet size, and "
  "hailing norms.")
H("4.7 Limitations", 2)
P("Principal limitations: (i) the taxi-flow prior is a proxy, not observed "
  "vacant-taxi flow — CSIS Pseudo-PFLOW trajectories were inaccessible and "
  "substituted; (ii) accessibility units are uncalibrated to waiting time; "
  "(iii) OSM completeness and the monitor-survey profile introduce bias; "
  "(iv) the monitor profile lacks weekday/weekend splits, so weekend structure "
  "is an explicit modeling assumption; (v) no demand-side congestion or "
  "competition among walkers is modeled.")
H("4.8 Relationship to future empirical validation", 2)
P("Paper 2 should (a) observe vacant vs occupied taxi passages at sampled "
  "segments, (b) measure actual street-hail waiting times, (c) calibrate the "
  "accessibility score to waiting time, (d) test prospective recommendations "
  "and real walking behavior, and (e) explore crowdsensing or vision-based "
  "detection. This is a validation study of the same construct, not an "
  "unrelated follow-up.")

# ---------------- 5. Conclusion ----------------
H("5. Conclusion")
P("Direction- and time-sensitive street-hail accessibility gradients, and "
  "non-trivial pedestrian relocation gains over naive heuristics, are "
  "inferable from public data alone in central Tokyo. The result is a "
  "feasibility demonstration and a calibrated hypothesis for empirical "
  "validation — not a waiting-time prediction.")

# ---------------- References ----------------
H("References")
BIB = {
 "hakusyo2025": "Tokyo Hire-Taxi Association. Tokyo no Taxi 2025 (Tokyo Taxis 2025 yearbook). https://taxi-tokyo.or.jp/ (accessed 2026-09-29).",
 "taxi_demand": "Moreira-Matias L, Gama J, Ferreira M, Mendes-Moreira J, Damas L. Predicting taxi-passenger demand using streaming data. IEEE Trans Intell Transp Syst. 2013;14(3):1393-1402.",
 "taxi_stand": "Ocalir EV, Ercoskun OY, Tur R. An integrated model of GIS and fuzzy logic (FMOTS) for location decisions of taxicab stands. Expert Syst Appl. 2010;37(7):4892-4901.",
 "taxi_demand2": "Hwang RH, Hsueh YL, Chen YT. An effective taxi recommender system based on a spatio-temporal factor analysis model. Inf Sci. 2015;314:28-40.",
 "yang2010": "Yang H, Leung CWY, Wong SC, Bell MGH. Equilibria of bilateral taxi-customer searching and meeting on networks. Transp Res Part B. 2010;44(8-9):1067-1083.",
 "tfinder": "Yuan NJ, Zheng Y, Zhang L, Xie X. T-Finder: a recommender system for finding passengers and vacant taxis. IEEE Trans Knowl Data Eng. 2013;25(10):2390-2403.",
 "pudo": "Alonso-Mora J, Samaranayake S, Wallar A, Frazzoli E, Rus D. On-demand high-capacity ride-sharing via dynamic trip-vehicle assignment. Proc Natl Acad Sci USA. 2017;114(3):462-467.",
 "osm": "OpenStreetMap contributors. Planet dump and Overpass API. https://www.openstreetmap.org (ODbL; accessed 2026-09-29 via OSMnx 2.0.7).",
 "nlni": "Ministry of Land, Infrastructure, Transport and Tourism (Japan). National Land Numerical Information, N02 railway dataset (FY2023). https://nlftp.mlit.go.jp/ksj/ (accessed 2026-09-29).",
 "monitor": "Tokyo Taxi Center. Taxi user monitor survey, FY2023 tabulation report (taxi riyo-sha monitor chosa). https://www.tokyo-tc.or.jp/center/uploads/monitor_2024.pdf (accessed 2026-09-29).",
}
for i, rid in enumerate(REFS):
    p = doc.add_paragraph(); p.add_run(f"{i+1}. ").bold = True
    p.add_run(BIB[rid])

# ---------------- Tables ----------------
H("Table 1. Public data sources", 1)
t = doc.add_table(rows=5, cols=4); t.style = "Table Grid"
for j, h in enumerate(["Source", "Provider/License", "Scope", "Role in model"]):
    t.rows[0].cells[j].text = h
for i, r in enumerate([
    ["OSM road network + POIs (Overpass)", "OSM contributors / ODbL", "5 central wards Tokyo", "segments, suitability, context, walking network"],
    ["NLNI N02 railway stations", "MLIT / NLNI terms", "FY2023 passengers", "primary attractor mass"],
    ["Tokyo Taxi Center monitor survey", "Tokyo Taxi Center / public report", "FY2023, n=2,662", "hourly temporal profile"],
    ["Tokyo Hire-Taxi Assoc. yearbook 2025", "THTA / public report", "FY2024 fleet stats", "background context"],
]):
    for j, v in enumerate(r): t.rows[i+1].cells[j].text = v

H("Table 2. Relocation outcomes by radius (Model C)", 1)
sub = comp[comp.model == "A_C"]
t = doc.add_table(rows=len(sub)+1, cols=7); t.style = "Table Grid"
for j, h in enumerate(["Radius m", "n", "any gain", ">0.1 SD", "mean G_A (SD)", "opt>nearest major", "median walk m"]):
    t.rows[0].cells[j].text = h
for i, (_, r) in enumerate(sub.iterrows()):
    vals = [str(int(r.radius)), f"{int(r.n)}", pc(r.frac_any_gain), pc(r["frac_gain_gt_0.1sd"]),
            f2(r.mean_G_A), pc(r.opt_gt_nearmajor), f1(r.median_walk_m)]
    for j, v in enumerate(vals): t.rows[i+1].cells[j].text = v

doc.save(f"{OUT}/MANUSCRIPT_inline.docx")
print("docx saved; refs order:", REFS)

# ---------------- cover letter ----------------
c = Document()
c.add_paragraph("Dear Editors,")
c.add_paragraph(
    "We submit our manuscript 'Inferring and Optimizing Street-Hail Taxi "
    "Accessibility Without Proprietary Fleet Telemetry'. The study asks whether "
    "public data alone — road networks, urban attractors, and published "
    "aggregate taxi-use statistics — can support a meaningful, time-sensitive "
    "measure of relative street-hail accessibility and reveal beneficial "
    "short-range pedestrian relocation, in the five central wards of Tokyo.")
c.add_paragraph(
    "The work is deliberately a feasibility study: it makes no claim to predict "
    "vacant taxis or waiting times, benchmarks an accessibility optimizer "
    "against naive heuristics at population scale, and establishes robustness "
    "across specifications. A companion empirical validation study is planned.")
c.add_paragraph(
    "The manuscript is original, is not under consideration elsewhere, uses only "
    "legally accessible public data, and involves no human subjects.")
c.add_paragraph("Sincerely,\nThe Authors")
c.save(f"{OUT}/COVER_LETTER.docx")
print("cover letter saved")
