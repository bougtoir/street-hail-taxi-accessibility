#!/usr/bin/env python3
"""CEUS final: CEUS_MAIN_MANUSCRIPT_inline.docx, CEUS_COVER_LETTER.docx,
CEUS_HIGHLIGHTS.docx, CEUS_submission_FINAL.zip."""
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

def ab(spec, r, c): return abl[(abl.spec == spec) & (abl.radius == r)][c].iloc[0]
def tf(a, b, c): return ts[(ts.selector == a) & (ts.evaluator == b) & (ts.radius == 300)][c].iloc[0]
def pc(x): return f"{100*x:.0f}%"
def f2(x): return f"{x:.2f}"
def ci(r): return eval(r) if isinstance(r, str) else r

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
tr = tp.add_run("Mapping street-hail opportunity without fleet telemetry: "
                "a geospatial framework for pedestrian relocation in urban taxi access")
tr.bold = True; tr.font.size = Pt(16)

H("Abstract")
P("Background: Street-hail taxi access in dense cities depends on fine-scale "
  "street-level opportunity structure that passengers cannot observe and "
  "researchers cannot measure without proprietary fleet telemetry. "
  "Methods: We construct a public-data-derived, relative street-hail "
  "opportunity score on the directed road network of Tokyo's five central "
  "wards (27,887 hail-feasible segments), combining road hierarchy, railway "
  "station locations, mapped attractors, and a published hourly taxi-use "
  "profile. For 2,000 sampled origins we optimize pedestrian relocation "
  "within 100-500 m walking distance and audit the result with component "
  "ablation (road-only vs attractor-only vs proxy vs combined), "
  "cross-specification transfer, and a 500-permutation spatial null with a "
  "within-district constrained variant, using origin-clustered bootstrap "
  "inference (5,000 replicates). "
  f"Results: {pc(ab('COMB',200,'frac_pos'))}-{pc(ab('COMB',500,'frac_pos'))} "
  "of origins have a higher-scoring segment within walking range, and the "
  f"optimizer exceeds the nearest-major-road heuristic in "
  f"{pc(ab('COMB',300,'gt_nearmaj'))} of origins at 300 m (paired Wilcoxon "
  "p<0.001). Transfer between road-only and attractor-only selections is "
  "positive but weak (53% and 44% of origins), indicating partially "
  "independent information layers. Against the permutation null, the "
  "reliability of finding an improvement marginally exceeds chance "
  "(empirical p=0.02-0.09 at 200-500 m) but the gain magnitude does not — a "
  "generic heterogeneous surface produces larger local contrasts. "
  "Conclusions: Public urban data contain non-trivial spatial structure that "
  "can generate candidate street-hail relocation contrasts without "
  "proprietary fleet telemetry, providing a testable basis for subsequent "
  "empirical validation; the scores carry no waiting-time meaning.")
P("Keywords: geospatial analysis; urban mobility; public data; street-hail "
  "taxi; pedestrian relocation; spatial opportunity structure")

H("1. Introduction")
P("Street-hail taxi access is an urban mobility problem of information "
  "asymmetry: the fine-scale geography of where a vacant taxi is likely to "
  "pass is invisible to the pedestrian deciding where to stand. The data "
  "that could resolve it — vacant-taxi GPS trajectories — are proprietary "
  "operational telemetry held by fleet operators.")
P("Most computational mobility systems assume that barrier away. Taxi-demand "
  "prediction " + cite("taxi_demand") + ", stand siting " + cite("taxi_stand") +
  ", cruising-area recommendation " + cite("taxi_demand2") + ", search "
  "equilibrium models " + cite("yang2010") + ", and passenger-side "
  "recommenders such as T-Finder " + cite("tfinder") + " are all trained on "
  "fleet trajectories; pickup-point assignment in on-demand ride-sharing "
  + cite("pudo") + " likewise presumes observed demand. The unresolved "
  "methodological question is whether useful passenger-side spatial "
  "opportunity structure can be extracted when those data are unavailable.")
P("We address that question as an urban-computation problem. The scientific "
  "object is fine-scale urban opportunity structure for street-hail access "
  "under incomplete mobility information; the taxi use case is the empirical "
  "application. Because a constructed score can be trivially self-maximized "
  "by optimization, we additionally audit whether the apparent relocation "
  "signal is genuine urban structure — through component ablation, "
  "cross-specification transfer, and spatial permutation — rather than an "
  "optimization tautology.")
P("The novelty is the combination, not any single element: a telemetry-free "
  "public-data construction on a directed road-segment representation, a "
  "passenger-side relocation formulation, and a validation architecture "
  "(ablation, transfer, permutation) designed to separate structured urban "
  "signal from generic maximum-selection.")

H("2. Materials and Methods")
H("2.1 Study area", 2)
P("Chiyoda, Chuo, Minato, Shinjuku, and Shibuya — the five contiguous "
  "central wards of Tokyo and a canonical street-hail environment "
  + cite("hakusyo2025") + ".")
H("2.2 Public data sources", 2)
P("OpenStreetMap road network and points of interest via Overpass "
  + cite("osm") + "; FY2023 railway-station locations (MLIT National Land "
  "Numerical Information N02) " + cite("nlni") + "; the hourly taxi-use "
  "distribution from the Tokyo Taxi Center user-monitor survey "
  + cite("monitor") + ". The restricted CSIS Pseudo-PFLOW trajectory product "
  "was inaccessible and substituted (DATA_SOURCE_AUDIT). During revision we "
  "found the FY2023 N02 schema carries no passenger-count field, so the "
  "station term is an unweighted location kernel; the pipeline was rebuilt "
  "accordingly.")
H("2.3 Directed road-network construction", 2)
P("The OSM driving graph was reduced to 27,887 hail-feasible directed "
  "segments (motorway, trunk, pedestrian classes excluded). The OSM walk "
  "graph (182,538 edges) supplies pedestrian distances (equirectangular "
  "metric at 35.68N).")
H("2.4 Public-data-derived opportunity score", 2)
P("A circulation-potential proxy combines road-class weight w_road, a "
  "Gaussian demand-attractor kernel field D(e) (sigma=300 m), and a period "
  "multiplier P(h;ctx) from the monitor-survey profile blended toward a "
  "night-shifted variant in nightlife contexts:")
EQ([m_sub("P", "circ"), m_run("(e,t) = w_road(e)·(0.3 + D(e))·P(h;ctx(e))")])
P("This is a modeled proxy, not observed taxi flow; the temporal structure "
  "is partly assumed.")
H("2.5 Component specifications", 2)
P("Four specifications define the ablation family. Road-only uses hierarchy, "
  "degree, and lanes; attractor-only uses station, nightlife, hotel/hospital, "
  "transit, and taxi-stand kernels; the proxy uses the circulation potential "
  "above; the combined specification is")
EQ([m_sub("S", "COMB"), m_run("(e,t) = z(z log(1+P_circ) + 0.5·S_road + 0.4·C_ctx)")])
P("All scores are z-standardized; weights are transparent and untuned.")
H("2.6 Origins and walking neighborhoods", 2)
P("2,000 origins sampled uniformly from hail-feasible segments (seed 42). "
  "Reachable candidates are segments whose midpoint is within 25 m of a walk "
  "node reachable within 100/200/300/500 m.")
H("2.7 Relocation formulation and metrics", 2)
P("The selected location maximizes the specification score over reachable "
  "candidates. The primary metric is the absolute gain")
EQ([m_sub("G", "S"), m_run(" = S(x*) - S0")])
P("in standardized units, with the fraction of origins improved as "
  "co-primary. Relative percentage gain is reported only secondarily: "
  "z-scores cross zero, making percentage denominators unstable.")
H("2.8 Baseline heuristics", 2)
P("Stay; random relocation (10 seeded draws); nearest major-class road "
  "segment; per-specification optima.")
H("2.9 Cross-specification transfer", 2)
P("For each origin, radius, and period, the location x* selected under "
  "specification A is evaluated under a distinct specification B:")
EQ([m_run("TG(A→B) = "), m_sub("S", "B"), m_run("(x*"), m_sub("", "A"),
    m_run(") - "), m_sub("S", "B"), m_run("(x0)")])
P("We compute all six directed transfers among road-only, attractor-only, "
  "and the proxy, plus three transfers into the combined specification. "
  "Off-diagonal transfer between conceptually distinct component families "
  "(road-only and attractor-only) is the primary independence test; "
  "transfers into the combined score are weaker evidence because it embeds "
  "the constituents.")
H("2.10 Spatial permutation null", 2)
P("To test whether observed gains reflect spatial structure rather than the "
  "generic property that a maximum over more candidates tends to exceed the "
  "origin value, we permute the combined score across all hail-feasible "
  "segments 500 times — preserving the marginal score distribution, network "
  "geometry, origin distribution, and candidate counts — and recompute the "
  "fraction improved and mean gain at each radius. A within-ward constrained "
  "permutation preserves coarse geographic structure. Empirical p-values "
  "use (1 + #{null >= obs})/(1 + N).")
H("2.11 Cluster-aware statistical inference", 2)
P("Origin-period rows are repeated measurements, not independent "
  "observations. For period-invariant specifications (road-only, "
  "attractor-only) inference uses unique origins (n = 1,961-1,999 with "
  "nonempty reachable sets). For period-varying specifications, bootstrap "
  "resampling (5,000 replicates) resamples origins and pools their period "
  "rows; paired tests use origin-mean differences. We report the clustering "
  "unit, replicate count, effect estimates, CIs, and p-values together "
  "rather than significance alone.")
H("2.12 Reproducibility", 2)
P("Fixed seeds, raw-data snapshots with a SHA-256 acquisition ledger, all "
  "code and machine-readable tables provided.")

H("3. Results")
H("3.1 Spatial opportunity structure", 2)
P("The modeled opportunity score forms continuous ridges along arterial "
  "corridors and station fronts with troughs in interior blocks (Figure 2). "
  "These are modeled contrasts, not observed taxi density.")
FIGURE("fig2_map", "Figure 2. Modeled street-hail opportunity (combined "
       "specification, SD units), weekday 17:00 and weekend 23:00.")
H("3.2 Within-walking-radius heterogeneity", 2)
P(f"Under the combined specification, {pc(ab('COMB',100,'frac_pos'))}-"
  f"{pc(ab('COMB',500,'frac_pos'))} of origins have a higher-scoring segment "
  "within 100-500 m, mean absolute gain "
  f"{f2(ab('COMB',100,'mean_G'))}-{f2(ab('COMB',500,'mean_G'))} SD "
  "(origin-clustered bootstrap CIs exclude zero; Table 2, Figure 4).")
FIGURE("fig4_gain_by_radius", "Figure 4. Distribution of absolute "
       "opportunity-score gain (SD units) by walking radius.")
H("3.3 Baseline relocation contrasts", 2)
P(f"The optimizer exceeds random relocation in ~{pc(ab('COMB',300,'gt_rand'))} "
  "of origins across radii (Figure 5).")
FIGURE("fig5_strategies", "Figure 5. Mean modeled opportunity score by "
       "strategy (combined specification, all radii pooled). Error bars = SEM.")
H("3.4 Component ablation", 2)
P(f"Every construction yields positive gains for most origins at 300 m "
  f"(road-only {pc(ab('ROAD',300,'frac_pos'))}, attractor-only "
  f"{pc(ab('ATTR',300,'frac_pos'))}, proxy {pc(ab('PROXY',300,'frac_pos'))}, "
  f"combined {pc(ab('COMB',300,'frac_pos'))}; Figure 7, Table 3). Segment "
  "rankings agree only moderately across specifications (mean Spearman "
  "0.52-0.93): the constructions are genuinely distinct.")
FIGURE("fig7_ablation", "Figure 7. Component ablation: origins improved by "
       "radius (left), fraction beating nearest-major-road (middle), rank "
       "agreement with combined specification (right).")
H("3.5 Cross-specification transfer", 2)
P("Locations selected under one construction retain benefit under another, "
  "but asymmetrically (Figure 8, Table 4): road-selected locations improve "
  f"the attractor score for {pc(tf('ROAD','ATTR','frac_pos'))} of origins "
  f"(mean {f2(tf('ROAD','ATTR','mean_TG'))} SD), and attractor-selected "
  f"locations improve the road score for {pc(tf('ATTR','ROAD','frac_pos'))} "
  f"({f2(tf('ATTR','ROAD','mean_TG'))} SD). Transfers toward the proxy are "
  f"stronger (attr -> proxy {pc(tf('ATTR','PROXY','frac_pos'))}, mean "
  f"{f2(tf('ATTR','PROXY','mean_TG'))} SD; road -> proxy "
  f"{pc(tf('ROAD','PROXY','frac_pos'))}). Off-diagonal transfer between the "
  "two conceptually distinct component families is real but weak.")
FIGURE("fig8_transfer_matrix", "Figure 8. Cross-specification transfer "
       "matrix at 300 m: mean transfer gain in SD units (left) and fraction "
       "of origins with positive transfer (right). Diagonal would show "
       "self-optimization; off-diagonal entries show transfer.")
H("3.6 Spatial permutation null", 2)
po = perm["weekday_17"]["obs"]; pn = perm["weekday_17"]["null_mean"]
P(f"Against 500 unconstrained permutations (weekday 17:00), the fraction of "
  f"origins with any improvement marginally exceeds the null at 200-500 m "
  f"(observed {po['300'][0]:.3f} vs null {pn['300'][0]:.3f} at 300 m, "
  "empirical p=0.02-0.09) but is indistinguishable at 100 m (p=1.0). "
  f"Critically, the mean gain does not exceed the null (observed "
  f"{po['300'][1]:.2f} SD vs null {pn['300'][1]:.2f} SD at 300 m): a "
  "spatially unstructured surface with the same marginal distribution "
  "produces larger local max-min contrasts. The within-ward constrained "
  "null gives the same pattern. What the real surface buys is reliability — "
  "a marginally higher chance that some improvement exists nearby — not "
  "larger gains (Figure 9).")
FIGURE("fig9_permutation_null", "Figure 9. Observed statistics (red) against "
       "the 500-permutation null distribution (gray), combined "
       "specification, 300 m, weekday 17:00.")
H("3.7 Nearest-major-road comparison", 2)
P(f"The combined optimum exceeds the nearest major-road segment in "
  f"{pc(ab('COMB',300,'gt_nearmaj'))} of origins at 300 m (paired mean "
  f"surplus {f2(ab('COMB',300,'diff_nearmaj'))} SD, clustered 95% CI "
  f"{ci(abl[(abl.spec=='COMB')&(abl.radius==300)].diff_nearmaj_ci.iloc[0])}, "
  "Wilcoxon p<0.001). We describe this as additional modeled opportunity "
  "contrast beyond a simple road-hierarchy heuristic — not predictive "
  "superiority.")
H("3.8 Temporal and district model behavior", 2)
P("Under the modeled temporal specifications, computed gains are largest in "
  "the weekday-morning period and the weekend specification shifts modeled "
  "opportunity toward nightlife contexts — input-profile consequences, not "
  "observed urban patterns (Figure 6).")
FIGURE("fig6_heterogeneity", "Figure 6. Modeled mean relocation gain by "
       "hour/day-type (left) and ward/radius (right).")
H("3.9 Sensitivity analyses", 2)
P(f"Kernel bandwidth 150/500 m leaves per-origin gains nearly unchanged "
  f"(rho {sigma['rho_150']:.2f}/{sigma['rho_500']:.2f}).")
FIGURE("fig1_framework", "Figure 1. Analytical workflow: public data to "
       "modeled opportunity ranking to walkable relocation candidates, with "
       "ablation, transfer, and permutation audits.")
FIGURE("fig3_worked_example", "Figure 3. Worked example (200 m, weekday "
       "17:00): origin (star), reachable segments by modeled opportunity, "
       "nearest major road (blue square), optimizer choice (red circle).")

H("4. Discussion")
H("4.1 Three evidence levels", 2)
P("Street-hail relocation claims should be read on three levels. Level 1, "
  "self-optimization: a model finds nearby locations that score higher under "
  "itself — trivially achievable and not evidence alone. Level 2, "
  "cross-specification transfer: locations selected from one urban "
  "information layer retain benefit under a distinct layer. Level 3, "
  "empirical passenger benefit: actual vacant-taxi encounters and waiting "
  "times. This paper addresses Levels 1 and 2; Paper 2 must address Level 3.")
H("4.2 Interpretation of the audits", 2)
P("Component ablation shows the relocation signal is not an artifact of any "
  "single component family. Cross-specification transfer between road-only "
  "and attractor-only selections is positive but weak and asymmetric, "
  "indicating partially nested information layers rather than one dominant "
  "structure. The permutation analysis is the most sobering: the reliability "
  "of improvement marginally exceeds a spatially unstructured null, but gain "
  "magnitudes are fully consistent with generic maximum-selection. The "
  "defensible claim is therefore narrow: public data identify where "
  "opportunity is modeled to be locally higher, with a reliability slightly "
  "above chance — not that the modeled gains are spatially exceptional.")
H("4.3 CEUS-relevant contributions", 2)
P("(1) A geospatial framework representing street-hail opportunity on a "
  "directed road network without fleet telemetry. (2) A passenger-side "
  "relocation formulation over fine-scale urban opportunity gradients. "
  "(3) A validation architecture — ablation, transfer, permutation — that "
  "distinguishes structured urban signal from optimization tautology and "
  "is transferable to other data-constrained mobility settings. (4) The "
  "framework applies wherever proprietary operational data are unavailable.")
H("4.4 Limitations", 2)
P("No observed vacant-taxi ground truth; scores are uncalibrated proxies, "
  "not waiting-time estimates; taxi operational behavior is not directly "
  "observed; temporal structure partly reflects model inputs; the Tokyo "
  "context may limit transferability; roadside legal/physical hail "
  "feasibility is imperfectly represented; cross-specification transfer is "
  "not empirical validation; and the FY2023 station data lack passenger "
  "counts, so the station term is unweighted.")
H("4.5 Relationship to Paper 2", 2)
P("Paper 2 asks whether the public-data-derived relocation ranking "
  "corresponds to actual vacant-taxi passage and reduces observed "
  "street-hail waiting time, via roadside observation, waiting-time "
  "measurement, calibration, and prospective testing. This study supplies "
  "candidate spatial contrasts for that validation.")

H("5. Conclusion")
P("Public urban data contain non-trivial spatial structure that can generate "
  "candidate street-hail relocation contrasts without proprietary fleet "
  "telemetry — a reliability marginally above a spatial null, with weak but "
  "real transfer between distinct component constructions — providing a "
  "testable basis for subsequent empirical validation.")

H("Declarations")
P("Data availability: all inputs are public datasets listed in Table 1; "
  "code and derived tables are available in the project repository. "
  "Competing interests: none declared. Funding: none. Author contributions: "
  "single-author work (conceptualization, analysis, writing).")

H("References")
BIB = {
 "hakusyo2025": "Tokyo Hire-Taxi Association. Tokyo no Taxi 2025. https://taxi-tokyo.or.jp/ (accessed 2026-09-29).",
 "taxi_demand": "Moreira-Matias L, Gama J, Ferreira M, Mendes-Moreira J, Damas L. Predicting taxi-passenger demand using streaming data. IEEE Trans Intell Transp Syst. 2013;14(3):1393-1402. doi:10.1109/TITS.2013.2261624.",
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

H("Table 2. Relocation outcomes by radius (combined specification)")
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

H("Table 4. Cross-specification transfer at 300 m (selector -> evaluator)")
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
            t.rows[i+1].cells[j+1].text = (f"{row.mean_TG.iloc[0]:.2f} SD / "
                                          f"{100*row.frac_pos.iloc[0]:.0f}%") if len(row) else "-"

H("Table 5. Spatial permutation null (combined specification, weekday 17:00, 500 permutations)")
t = doc.add_table(rows=5, cols=6); t.style = "Table Grid"
for j, h in enumerate(["Radius m", "obs frac>0", "null frac>0", "empirical p", "obs mean G", "null mean G"]):
    t.rows[0].cells[j].text = h
nullarr = np.load(f"{ROOT}/data/processed/perm_null_arrays.npz")
for i, r in enumerate([100, 200, 300, 500]):
    nf = np.array([x[0] for x in nullarr[f"weekday_17_{r}"]])
    ng = np.array([x[1] for x in nullarr[f"weekday_17_{r}"]])
    pf = (1 + (nf >= po[str(r)][0]).sum()) / (1 + len(nf))
    for j, v in enumerate([str(r), f"{po[str(r)][0]:.3f}", f"{nf.mean():.3f}", f"{pf:.3f}",
                           f"{po[str(r)][1]:.2f}", f"{ng.mean():.2f}"]):
        t.rows[i+1].cells[j].text = v

doc.save(f"{OUT}/CEUS_MAIN_MANUSCRIPT_inline.docx")
print("CEUS manuscript saved")

# ---- highlights ----
hl = Document()
hl.add_heading("Highlights", 0)
for b in [
    "Street-hail opportunity mapped on a directed road network using only public data",
    "Pedestrian relocation within 100-500 m optimized over modeled opportunity scores",
    "Component ablation, cross-specification transfer, and permutation nulls audit validity",
    "Gain reliability marginally exceeds a spatial null; magnitudes do not",
    "Framework transfers to mobility settings lacking proprietary telemetry",
]:
    hl.add_paragraph(b, style="List Bullet")
hl.save(f"{OUT}/CEUS_HIGHLIGHTS.docx")

# ---- cover letter ----
c = Document()
c.add_paragraph("Dear Editors,")
c.add_paragraph(
    "We submit 'Mapping street-hail opportunity without fleet telemetry: a "
    "geospatial framework for pedestrian relocation in urban taxi access' for "
    "consideration in Computers, Environment and Urban Systems.")
c.add_paragraph(
    "The manuscript is an urban-computation study: it asks whether fine-scale "
    "spatial opportunity structure for street-hail access can be extracted "
    "from public data alone when proprietary fleet telemetry is unavailable. "
    "The contribution is geospatial and methodological — a directed "
    "road-network representation of modeled opportunity, a passenger-side "
    "pedestrian relocation formulation, and a validation architecture "
    "(component ablation, cross-specification transfer, spatial permutation "
    "nulls) that distinguishes structured urban signal from optimization "
    "tautology. It fits CEUS rather than a fleet-operations journal because "
    "the object of study is urban information structure and spatial "
    "computation, not taxi operations, dispatch, or fleet management.")
c.add_paragraph(
    "We report the audits honestly: transfer between distinct component "
    "constructions is real but weak, and gain magnitudes do not exceed a "
    "spatial permutation null. The framework is transferable to other "
    "data-constrained mobility systems. The manuscript is original, uses only "
    "legally accessible public data, involves no human subjects, and is not "
    "under consideration elsewhere.")
c.add_paragraph("Sincerely,\nThe Authors")
c.save(f"{OUT}/CEUS_COVER_LETTER.docx")
print("cover letter + highlights saved")
