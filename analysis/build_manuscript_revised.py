#!/usr/bin/env python3
"""Revision: MANUSCRIPT_inline_revised.docx (+clean PDF), COVER_LETTER_revised.docx,
STREET_HAIL_TAXI_submission_revised.zip. Recalibrated claims + ablation results."""
import os, sys, json, zipfile
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAB, FIG, OUT = (f"{ROOT}/{d}" for d in ["tables", "figures", "output"])
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
def m_frac(n_, d_):
    f = m_el("f"); n = m_el("num"); dd = m_el("den")
    for x in n_: n.append(m_run(x))
    for x in d_: dd.append(m_run(x))
    f.extend([n, dd]); return f
def add_omml(p, els):
    om = m_el("oMath")
    for e in els: om.append(e if not isinstance(e, str) else m_run(e))
    p._p.append(om); return p

comp = pd.read_csv(f"{TAB}/strategy_comparison.csv")
abl = pd.read_csv(f"{TAB}/ablation_summary.csv")
agr = pd.read_csv(f"{TAB}/ablation_rank_agreement.csv")
sigma = json.load(open(f"{TAB}/sigma_sensitivity.json"))
agree = json.load(open(f"{TAB}/model_agreement.json"))

def cv(m, r, c):
    x = comp[(comp.model == m) & (comp.radius == r)][c].iloc[0]
    return eval(x) if isinstance(x, str) and x.startswith("[") else x
def ab(spec, r, c): return abl[(abl.spec == spec) & (abl.radius == r)][c].iloc[0]
def pc(x): return f"{100*x:.0f}%"
def f2(x): return f"{x:.2f}"
def f1(x): return f"{x:.1f}"

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
tr = tp.add_run("Public-Data Ranking of Street-Hail Taxi Opportunity and "
                "Pedestrian Relocation Candidates Without Fleet Telemetry")
tr.bold = True; tr.font.size = Pt(16)
doc.add_paragraph("A computational feasibility study in central Tokyo",
                  ).alignment = WD_ALIGN_PARAGRAPH.CENTER

H("Abstract")
P("Background: Street-hail taxi opportunity varies block by block, but the "
  "data that would measure it — vacant-taxi telemetry — are proprietary. This "
  "study asks whether public urban data alone can generate a defensible "
  "relative ranking of modeled street-hail opportunity and non-trivial "
  "pedestrian relocation candidates. No proprietary fleet data, roadside "
  "observation, or waiting-time measurements are used; all scores are "
  "proxy-based and uncalibrated.")
P("Methods: A directed road-segment map of the five central wards of Tokyo "
  "(27,887 hail-feasible segments) was combined with a public-data-derived "
  "circulation-potential proxy (road hierarchy, FY2023 railway-station "
  "passenger volumes, mapped attractors, and a published hourly taxi-use "
  "profile). Four opportunity specifications — road-only, attractor-only, "
  "circulation proxy, and combined — were evaluated ablatively. For 2,000 "
  "sampled origins across ten day-type-hour periods, relocation within "
  "100-500 m network distance was compared against staying, random "
  "relocation, and the nearest major road.")
P(f"Results: {pc(ab('COMB',200,'frac_pos'))}-{pc(ab('COMB',500,'frac_pos'))} "
  f"of origins had a higher-scoring reachable segment at 200-500 m. The "
  f"combined optimizer exceeded random relocation in ~{pc(ab('COMB',300,'gt_rand'))} "
  f"of origins and the nearest-major-road heuristic in {pc(ab('COMB',200,'gt_nearmaj'))}-"
  f"{pc(ab('COMB',500,'gt_nearmaj'))} of origins (paired Wilcoxon p<0.001). "
  "Relocation opportunity persisted under every ablation: road-only and "
  f"attractor-only constructions yielded {pc(ab('ROAD',300,'frac_pos'))} and "
  f"{pc(ab('ATTR',300,'frac_pos'))} improved origins at 300 m, with segment "
  "rank correlations to the combined model of 0.52-0.93.")
P("Conclusions: Public urban data can generate robust relative rankings of "
  "modeled street-hail opportunity and identify candidate pedestrian "
  "relocation contrasts without proprietary fleet telemetry. The scores "
  "carry no calibrated waiting-time meaning; they define candidate spatial "
  "contrasts for the field-validation study that must follow.")
P("Keywords: street-hail taxi; public data; pedestrian relocation; "
  "accessibility proxy; OpenStreetMap; Tokyo; feasibility study")

H("1. Introduction")
P("Street hailing remains a primary taxi-access mode in dense cities such as "
  "Tokyo " + cite("hakusyo2025") + ", but the data needed to quantify "
  "street-level opportunity — vacant-taxi trajectories — are proprietary. "
  "Passengers, and researchers without fleet access, cannot observe them.")
P("Prior work optimizes the fleet side: GPS-based taxi-demand prediction "
  + cite("taxi_demand") + ", stand siting " + cite("taxi_stand") + ", "
  "cruising-area recommendation " + cite("taxi_demand2") + ", and bilateral "
  "search equilibrium models " + cite("yang2010") + ". Passenger-side "
  "relocation toward better pickup spots is precedented (T-Finder "
  + cite("tfinder") + ", walkable pickup-and-drop-off designs "
  + cite("pudo") + ") but every such system is trained on telemetry. The "
  "open question is what survives when telemetry is removed entirely.")
P("This study is deliberately a dry, public-data feasibility analysis. It "
  "constructs a public-data-derived proxy for relative street-hail "
  "opportunity — not a measurement of vacant-taxi supply — and tests whether "
  "the resulting spatial rankings reveal meaningful pedestrian relocation "
  "contrasts. A component ablation asks whether the signal survives when the "
  "construct is decomposed into road-structure-only and attractor-only "
  "families, guarding against a tautological composite score.")
P("The intended contribution is the measurement/data architecture: "
  "telemetry-free, segment-level, passenger-side, and robustness-audited. "
  "Claims are restricted to modeled opportunity rankings; waiting times and "
  "vacant-taxi probabilities are reserved for empirical validation.")

H("2. Materials and Methods")
H("2.1 Study area", 2)
P("The five contiguous central wards of Tokyo (Chiyoda, Chuo, Minato, "
  "Shinjuku, Shibuya) — a canonical street-hail environment " + cite("hakusyo2025") + ".")
H("2.2 Public data sources", 2)
P("OpenStreetMap road network and POIs via Overpass " + cite("osm") + "; "
  "FY2023 railway-station passenger volumes (MLIT National Land Numerical "
  "Information) " + cite("nlni") + "; the hourly taxi-use distribution from "
  "the Tokyo Taxi Center user-monitor survey " + cite("monitor") + ". The "
  "restricted CSIS Pseudo-PFLOW business-traffic trajectories were "
  "inaccessible and substituted; see DATA_SOURCE_AUDIT.")
H("2.3 Directed road-network construction", 2)
P("The OSM driving graph was reduced to 27,887 hail-feasible directed "
  "segments (motorway, trunk and pedestrian classes excluded). The OSM walk "
  "graph (182,538 edges) supplies pedestrian distances.")
H("2.4 Circulation-potential proxy", 2)
P("The modeled proxy combines a road-class capacity weight, a Gaussian "
  "demand-attractor kernel field, and the monitor-survey hourly profile "
  "blended toward a night-shifted variant in nightlife contexts:")
EQ([m_run("P"), m_sub("circ", ""), m_run("(e,t) = w_road(e)·(0.3 + D(e))·P(h;ctx(e))")])
P("This is a modeled proxy, not observed taxi flow; the temporal structure "
  "is partly assumed (weekend/night behavior is a modeling input).")
H("2.5 Opportunity specifications and ablation", 2)
P("Four specifications define the ablation family: road-only (hierarchy, "
  "degree, lanes), attractor-only (station, nightlife, hotel/hospital, "
  "transit, taxi-stand kernels), the circulation-potential proxy, and a "
  "combined score:")
EQ([m_sub("S", "COMB"), m_run("(e,t) = z(z log(1+P_circ) + 0.5·S_road + 0.4·C_ctx)")])
P("All scores are z-standardized; weights are transparent and untuned. The "
  "ablation tests whether relocation signal persists under substantially "
  "different constructions rather than relying on the composite.")
H("2.6 Origin generation", 2)
P("2,000 origins sampled uniformly from hail-feasible segments (seed 42).")
H("2.7 Walking neighborhoods", 2)
P("Reachable drive segments = hail-feasible edges with midpoint within 25 m "
  "of a walk node reachable within radius 100/200/300/500 m.")
H("2.8 Relocation optimization and metrics", 2)
P("Primary metric: absolute gain in standardized score")
EQ([m_sub("G", "S"), m_run(" = S*(x0,t) − S0")])
P("Fraction of origins improved and distance to prespecified score "
  "improvement are co-primary. Relative percentage gain is secondary only: "
  "z-scores cross zero, making percentage gains near the mean denominator-"
  "unstable; no headline result uses them.")
H("2.9 Baseline heuristics", 2)
P("Stay; random relocation (10 seeded draws); nearest major-class road "
  "segment; per-specification optima in the ablation.")
H("2.10 Sensitivity analyses", 2)
P("Radii, specification family, improvement thresholds, candidate sets, "
  "kernel bandwidth (150/300/500 m), and day-type-hour structure; stability "
  "via Spearman correlation, top-1% Jaccard, gain-class transitions, and "
  "same-segment optimum agreement.")
H("2.11 Reproducibility", 2)
P("Fixed seeds, raw-data snapshots with SHA-256 ledger, all code and "
  "result tables provided.")

H("3. Results")
H("3.1 Spatial structure of modeled opportunity", 2)
P("The modeled opportunity score shows continuous ridges along arterial "
  "corridors and station fronts and troughs in interior blocks (Figure 2). "
  "These are modeled contrasts, not observed taxi density.")
FIGURE("fig2_map", "Figure 2. Modeled street-hail opportunity (combined "
       "specification, SD units), weekday 17:00 and weekend 23:00. Values are "
       "proxy-based modeled scores, not observed taxi flow.")
H("3.2 Local heterogeneity and relocation gain", 2)
P(f"Under the combined specification, {pc(ab('COMB',100,'frac_pos'))}-"
  f"{pc(ab('COMB',500,'frac_pos'))} of origins have a higher-scoring segment "
  f"within 100-500 m; mean absolute gain ranges {f2(ab('COMB',100,'mean_G'))} "
  f"to {f2(ab('COMB',500,'mean_G'))} SD (bootstrap CIs exclude zero; Table 2, "
  "Figure 4).")
FIGURE("fig4_gain_by_radius", "Figure 4. Distribution of absolute "
       "opportunity-score gain (SD units) by walking radius; violins with "
       "medians.")
H("3.3 Comparison with random and major-road heuristics", 2)
P(f"The optimizer exceeds random relocation in ~{pc(ab('COMB',300,'gt_rand'))} "
  f"of origins and the nearest major road in {pc(ab('COMB',100,'gt_nearmaj'))}-"
  f"{pc(ab('COMB',500,'gt_nearmaj'))}, mean paired surplus "
  f"{f2(ab('COMB',100,'diff_nearmaj'))}-{f2(ab('COMB',500,'diff_nearmaj'))} SD "
  "(Wilcoxon p<0.001). The optimal segment is itself major-class in "
  f"{pc(ab('COMB',500,'best_is_major'))} of origins at 500 m: the added value "
  "is selecting which corridor, not walking toward any major street "
  "(Figure 5).")
FIGURE("fig5_strategies", "Figure 5. Mean modeled opportunity score by "
       "strategy (combined specification, all radii pooled). Error bars = SEM.")
H("3.4 Ablation: does the signal survive decomposition?", 2)
P(f"Relocation opportunity persists under every construction (Figure 7, "
  f"Table 3): at 300 m, road-only improves {pc(ab('ROAD',300,'frac_pos'))} of "
  f"origins and attractor-only {pc(ab('ATTR',300,'frac_pos'))}. Against the "
  f"nearest major road, the road-only optimum wins {pc(ab('ROAD',300,'gt_nearmaj'))} "
  f"of origins (its own input is hierarchy), while attractor-only wins "
  f"{pc(ab('ATTR',300,'gt_nearmaj'))} — the spatial contrast is not an "
  "artifact of any single component family. Segment rank correlations with "
  f"the combined model are {f2(agr.groupby('spec').spearman.mean()['PROXY'])} "
  f"(proxy), {f2(agr.groupby('spec').spearman.mean()['ROAD'])} (road-only), "
  f"{f2(agr.groupby('spec').spearman.mean()['ATTR'])} (attractor-only): "
  "moderate agreement, meaning the constructions are genuinely different "
  "yet consistently identify local gradients.")
FIGURE("fig7_ablation", "Figure 7. Ablation summary. Left: fraction of "
       "origins improved by radius. Middle: fraction beating the "
       "nearest-major-road heuristic. Right: mean Spearman rank correlation "
       "of each specification against the combined model.")
H("3.5 Temporal and district model behavior", 2)
P("Under the modeled temporal specifications, computed relocation gains are "
  "largest in the weekday-morning period, and the weekend specification "
  "shifts modeled opportunity toward nightlife contexts. These are "
  "input-profile consequences — descriptive model behavior, not observed "
  "urban patterns (Figure 6). Ward-level differences in mean gain are "
  "consistent with block-structure differences.")
FIGURE("fig6_heterogeneity", "Figure 6. Modeled mean relocation gain by "
       "hour/day-type (left) and ward/radius (right) under the assumed "
       "temporal profile — model behavior, not observed patterns.")
H("3.6 Robustness", 2)
P(f"Halving/raising the attractor kernel bandwidth (150/500 m) leaves "
  f"per-origin gains nearly unchanged (rho {sigma['rho_150']:.2f}/"
  f"{sigma['rho_500']:.2f}; identical optimum in {pc(sigma['same_opt_150'])}/"
  f"{pc(sigma['same_opt_500'])} of origins).")
FIGURE("fig1_framework", "Figure 1. Conceptual framework: public data to "
       "modeled opportunity ranking to walkable relocation candidates.")
FIGURE("fig3_worked_example", "Figure 3. Worked example (200 m, weekday "
       "17:00): origin (star), reachable segments colored by modeled "
       "opportunity, nearest major road (blue square), optimizer's choice "
       "(red circle).")

H("4. Discussion")
H("4.1 Main findings", 2)
P("Public urban data generate spatially structured candidate rankings of "
  "modeled street-hail opportunity in which short pedestrian relocation "
  "yields non-trivial score gains for a large majority of origins — and the "
  "contrast persists under independent ablation constructions. Consistency "
  "across substantially different public-data constructions, not any single "
  "score, is the main result.")
H("4.2 Passenger-side interpretation", 2)
P("The score is a relative modeled opportunity, not waiting time. The "
  "resulting spatial contrasts are sufficiently large and structured to "
  "motivate prospective empirical validation — whether they translate into "
  "shorter waits is exactly what Paper 2 must measure.")
H("4.3 Why walking relocation matters", 2)
P("Passenger-side relocation needs no fleet coordination or data license. "
  "That the optimizer's added value is 'which corridor' rather than "
  "'walk toward a major street' is itself a useful finding for downstream "
  "study design.")
H("4.4 Implications for low-friction taxi access", 2)
P("A public-data opportunity layer could support map overlays and "
  "station-exit guidance where fleet APIs are unavailable — contingent on "
  "empirical calibration.")
H("4.5 Visitors unfamiliar with local conventions", 2)
P("Street-hail conventions differ internationally; Japanese taxis display "
  "external occupancy/availability indications. A relocation recommendation "
  "is most useful paired with such cues — an application note, not a tested "
  "claim.")
H("4.6 Generalization", 2)
P("The pipeline needs only OSM, public attractor data, and an aggregate "
  "temporal profile; magnitudes are city-specific.")
H("4.7 What this study does not establish", 2)
P("By design, Paper 1 establishes none of: actual vacant-taxi passage "
  "rates, real waiting-time reduction, probability of a successful street "
  "hail, or behavioral compliance with walking recommendations. These "
  "require Paper 2 field observation and calibration.")
H("4.8 Limitations", 2)
P("(i) The circulation-potential proxy is modeled, not observed — the "
  "Pseudo-PFLOW trajectories were access-restricted and substituted. "
  "(ii) Scores are uncalibrated to waiting time. (iii) Weekend and night "
  "temporal structure is assumed, not measured. (iv) OSM completeness and "
  "monitor-survey sampling introduce bias. (v) No demand-side competition "
  "is modeled.")
H("4.9 Relationship to Paper 2", 2)
P("Paper 2 provides empirical validation: roadside observation of "
  "vacant/occupied passage, waiting-time measurement, score-to-waiting-time "
  "calibration, and prospective recommendation testing. Paper 1 supplies "
  "candidate spatial contrasts for that validation.")

H("5. Conclusion")
P("Multiple independent public-data constructions identify consistent local "
  "gradients in modeled street-hail opportunity, and optimized pedestrian "
  "relocation over those rankings adds information beyond the nearest-major-"
  "road heuristic. The result is a validated computational precondition, not "
  "a validated passenger benefit.")

H("References")
BIB = {
 "hakusyo2025": "Tokyo Hire-Taxi Association. Tokyo no Taxi 2025. https://taxi-tokyo.or.jp/ (accessed 2026-09-29).",
 "taxi_demand": "Moreira-Matias L, Gama J, Ferreira M, Mendes-Moreira J, Damas L. Predicting taxi-passenger demand using streaming data. IEEE Trans Intell Transp Syst. 2013;14(3):1393-1402.",
 "taxi_stand": "Ocalir EV, Ercoskun OY, Tur R. An integrated model of GIS and fuzzy logic (FMOTS) for location decisions of taxicab stands. Expert Syst Appl. 2010;37(7):4892-4901.",
 "taxi_demand2": "Hwang RH, Hsueh YL, Chen YT. An effective taxi recommender system based on a spatio-temporal factor analysis model. Inf Sci. 2015;314:28-40.",
 "yang2010": "Yang H, Leung CWY, Wong SC, Bell MGH. Equilibria of bilateral taxi-customer searching and meeting on networks. Transp Res Part B. 2010;44(8-9):1067-1083.",
 "tfinder": "Yuan NJ, Zheng Y, Zhang L, Xie X. T-Finder: a recommender system for finding passengers and vacant taxis. IEEE Trans Knowl Data Eng. 2013;25(10):2390-2403.",
 "pudo": "Alonso-Mora J, Samaranayake S, Wallar A, Frazzoli E, Rus D. On-demand high-capacity ride-sharing via dynamic trip-vehicle assignment. Proc Natl Acad Sci USA. 2017;114(3):462-467.",
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
    ["NLNI N02 stations", "MLIT / NLNI terms", "FY2023", "attractor mass"],
    ["Tokyo Taxi Center monitor survey", "Tokyo Taxi Center", "FY2023, n=2,662", "temporal profile"],
    ["THTA yearbook 2025", "THTA", "FY2024", "background"],
]):
    for j, v in enumerate(r): t.rows[i+1].cells[j].text = v

H("Table 2. Relocation outcomes by radius (combined specification)")
sub = comp[comp.model == "A_C"]
t = doc.add_table(rows=len(sub)+1, cols=7); t.style = "Table Grid"
for j, h in enumerate(["Radius m", "n", "improved", ">0.1 SD", "mean gain (SD)", "beats nearest major", "median walk m"]):
    t.rows[0].cells[j].text = h
for i, (_, r) in enumerate(sub.iterrows()):
    for j, v in enumerate([str(int(r.radius)), f"{int(r.n)}", pc(r.frac_any_gain),
            pc(r["frac_gain_gt_0.1sd"]), f2(r.mean_G_A), pc(r.opt_gt_nearmajor), f1(r.median_walk_m)]):
        t.rows[i+1].cells[j].text = v

H("Table 3. Ablation summary (300 m radius)")
sub = abl[abl.radius == 300]
t = doc.add_table(rows=len(sub)+1, cols=6); t.style = "Table Grid"
for j, h in enumerate(["Specification", "improved", ">0.1 SD", "beats nearest major", "beats random", "best is major road"]):
    t.rows[0].cells[j].text = h
name = {"ROAD": "Road-only", "ATTR": "Attractor-only", "PROXY": "Circulation proxy", "COMB": "Combined"}
for i, (_, r) in enumerate(sub.iterrows()):
    for j, v in enumerate([name[r.spec], pc(r.frac_pos), pc(r.frac_gt_01),
                           pc(r.gt_nearmaj), pc(r.gt_rand), pc(r.best_is_major)]):
        t.rows[i+1].cells[j].text = v

doc.save(f"{OUT}/MANUSCRIPT_inline_revised.docx")
print("revised docx saved")

c = Document()
c.add_paragraph("Dear Editors,")
c.add_paragraph(
    "We submit 'Public-Data Ranking of Street-Hail Taxi Opportunity and "
    "Pedestrian Relocation Candidates Without Fleet Telemetry'. The study asks "
    "whether public urban data alone — road networks, station volumes, mapped "
    "attractors, published taxi-use statistics — can generate a defensible "
    "relative ranking of modeled street-hail opportunity and non-trivial "
    "pedestrian relocation candidates, in the five central wards of Tokyo.")
c.add_paragraph(
    "Unlike GPS-trajectory taxi recommenders, the framework uses no "
    "proprietary fleet data anywhere. A component ablation (road-only vs "
    "attractor-only vs proxy vs combined) demonstrates that the relocation "
    "signal is not a tautology of the composite score. The paper is "
    "methodological groundwork: it produces candidate spatial contrasts for "
    "empirical validation and makes no claim about actual waiting times, "
    "vacant-taxi availability, or behavioral outcomes.")
c.add_paragraph(
    "The manuscript is original, not under consideration elsewhere, uses only "
    "legally accessible public data, and involves no human subjects.")
c.add_paragraph("Sincerely,\nThe Authors")
c.save(f"{OUT}/COVER_LETTER_revised.docx")
print("cover letter saved")
