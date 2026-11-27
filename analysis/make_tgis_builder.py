#!/usr/bin/env python3
"""Derive build_manuscript_tgis.py from the frozen IJGIS builder sources
(_lit_builder_head.py + _lit_body.py) by explicit, fail-loud text edits,
then append _tgis_tail.py. Scientific content and canonical lookups are
unchanged; edits concern journal format and framing only."""
import os, re
A = os.path.dirname(os.path.abspath(__file__))
head = open(f"{A}/_lit_builder_head.py").read()
body = open(f"{A}/_lit_body.py").read()
def sub(src, old, new, n=1):
    c = src.count(old)
    if c != n:
        raise SystemExit(f"FAIL-LOUD: expected {n} occurrence(s), found {c}: {old[:70]!r}")
    return src.replace(old, new)

# ---- head: bibliography, APA 7 citations, figures separate, equations numbered
head = sub(head, 'analysis/ijgis_bib.json', 'analysis/tgis_bib.json')
i0 = head.index("def cite(*ids):"); i1 = head.index('for r in ordered) + ")"') + len('for r in ordered) + ")"')
head = head[:i0] + '''def cite(*ids):
    """APA 7 parenthetical citation: (Author, Year; Author, Year), works
    ordered alphabetically by first author, then year."""
    for r in ids:
        if r not in BIB:
            raise SystemExit(f"FAIL-LOUD: unknown reference id {r}")
        if r not in REFS: REFS.append(r)
    key = lambda r: (re.sub(r"^([A-Z]\\. )+", "", BIB[r]["cite"]).lower(), BIB[r]["year"])
    return "(" + "; ".join(f"{BIB[r]['cite']}, {BIB[r]['year']}" for r in sorted(ids, key=key)) + ")"''' + head[i1:]
head = sub(head, '''    doc.add_picture(fn, width=Inches(w))
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(cap); r.italic = True; r.font.size = Pt(10)''', '''    FIGS.append((name, cap))''')
head = sub(head, '''def EQ(els):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p._p.append(om(els))''', '''EQN = [0]
def EQ(els):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p._p.append(om(els))
    EQN[0] += 1
    p.add_run(f"    ({EQN[0]})")''')
head = sub(head, 'st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12)',
           'st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12)\n'
           'st.paragraph_format.line_spacing = 2.0\nFIGS, TABLES = [], []\nimport re')
body = sub(body, "the author(s) used", "the author used")
body = sub(body, "the author(s)' own; the author(s) reviewed", "the author's own; the author reviewed")

# ---- body: tables deferred after references
for k in range(1, 6):
    body = sub(body, f"\nTABLE{k}()\n", f"\nTABLES.append(TABLE{k})\n")

# ---- title block: author line, running title
body = sub(body, 'tr = tp.add_run(TITLE); tr.bold = True; tr.font.size = Pt(16)\n',
  'tr = tp.add_run(TITLE); tr.bold = True; tr.font.size = Pt(16)\n'
  'RUNNING = "Optimization gain is not proxy validity"\n'
  '_AM = json.load(open(f"{ROOT}/analysis/author_meta.json"))\n'
  'for _l in [_AM["author"], _AM["affiliation"], "Correspondence: " + _AM["email"] + "; ORCID: https://orcid.org/" + _AM["orcid"], "Running title: " + RUNNING]:\n'
  '    _ap = doc.add_paragraph(_l); _ap.alignment = WD_ALIGN_PARAGRAPH.CENTER\n')

# ---- abstract (<=150 words) and keywords (6)
a0 = body.index("ABSTRACT = ("); a1 = body.index('"is not validated merely because it can be optimized.")') + len('"is not validated merely because it can be optimized.")')
body = body[:a0] + '''ABSTRACT = (
  "Constructed spatial representations, such as accessibility indices and "
  "opportunity surfaces, are often optimized where outcome labels are "
  "unavailable. Because heterogeneous surfaces contain local maxima, "
  "self-optimization produces apparent gains by construction. We ask what "
  "internal evidence such gains require. Using street-hail taxi relocation "
  "in central Tokyo, we built four public-data opportunity surfaces on a "
  f"directed road network ({NSEG} segments) and audited local optimization "
  f"for {NOR} origins at 100-500 m walking radii with component ablation, "
  "cross-specification transfer, a road-hierarchy heuristic, and spatial "
  f"permutation nulls. At 300 m, {pc(AB('COMB',300,'frac_pos'))} of origins "
  f"improved (mean {f2(AB('COMB',300,'mean_G'))} SD) and "
  f"{pc(AB('COMB',300,'gt_nearmaj'))} beat the nearest-major-road "
  "heuristic, but transfer between distinct component families was weak "
  f"({pc(TF('ROAD','ATTR','frac_pos'))} and {pc(TF('ATTR','ROAD','frac_pos'))} "
  "positive). Permuted surfaces reproduced most of the improvement "
  "prevalence and produced larger mean gains. A geographic proxy is not "
  "validated merely because it can be optimized.")''' + body[a1:]
k0 = body.index("KEYWORDS = ("); k1 = body.index(")", body.index('"geographic information validity"')) + 1
body = body[:k0] + '''KEYWORDS = ("geocomputation; geographic representation; spatial data "
            "uncertainty; spatial decision support; spatial null models; "
            "spatial optimization")''' + body[k1:]

# ---- introduction: spatial data quality / representation uncertainty framing
body = sub(body, 'FIGURE("fig1_framework",', '''P("The question sits within the spatial data quality and uncertainty "
  "tradition of geographic information science. Uncertainty arises not "
  "only from measurement error in spatial data but also from the "
  "representational choices through which geographic knowledge is "
  "constructed " + cite("couclelis2003", "devillers2010") + "; variable "
  "choice, weighting, aggregation, scale and network or location encoding "
  "can each change a constructed result "
  + cite("fotheringham1991", "greco2019", "kim2024", "almusidi2025") + ". "
  "In spatial decision support, uncertainty in input data propagates into "
  "the solutions of optimization models " + cite("aerts2003") + ", and "
  "spatial optimization is increasingly embedded in GIS-based planning "
  "workflows " + cite("murray2023") + ". The case examined here is "
  "complementary: when a constructed representation is optimized under "
  "its own scoring rule, an improvement measured by that same score is not "
  "independent evidence that the representation is valid. We therefore "
  "treat representation and specification uncertainty as part of spatial "
  "data quality and ask what internal evidence is required before an "
  "optimization gain is read as informative geographic structure.")
FIGURE("fig1_framework",''')

# ---- AI use in Methods (Wiley AI guidelines) and statement names
body = sub(body, "AI_STATEMENT = (", "AI_STATEMENT = (")
body = sub(body, '"codes availability statement).")', '''"Availability Statement). Data-processing, analysis and "
  "document-generation code was written and run with the assistance of "
  "an AI software-engineering agent under the author's direction and "
  "review (see Acknowledgments).")''')
body = sub(body, '" (see Data and "\n  "Availability Statement)', '" (see Data "\n  "Availability Statement)')
body = sub(body, '"not at 100 m (p=1.0). Mean gain magnitude does not exceed the "', 'f"not at 100 m (p={PM(\'weekday_17\',\'100\',\'emp_p_frac\'):.1f}). Mean gain magnitude does not exceed the "')

# ---- five-level evidence hierarchy (wording only; results unchanged)
e0 = body.index('P("Level 1 (self-optimization)'); e1 = body.index('"this study.")', e0) + len('"this study.")')
body = body[:e0] + '''P("Level 1 (computational correctness): every reported value is "
  "generated from a canonical numerical registry with fixed seeds. "
  "Level 2 (within-proxy optimization): large apparent gains — achieved. "
  "Level 3 (cross-representation internal transfer): ablation passed; "
  "transfer between distinct component families weak; heuristic contrast "
  "retained. Level 4 (spatial-null discrimination): improvement "
  "prevalence marginally above, but mean gain magnitude below, the "
  "permutation null. Level 5 (external empirical validation): not "
  "available in this study.")''' + body[e1:]

# ---- discussion: spatial decision support
body = sub(body, 'H("4.6 Implications for GIScience and accessibility analysis", 2)\n',
  '''H("4.6 Implications for spatial data quality and spatial decision support", 2)
P("Optimization-based spatial decision support already recognizes that "
  "uncertainty in input data propagates into optimized solutions "
  + cite("aerts2003") + ". The stress tests used here extend that concern "
  "from input error to representation choice: an output computed on a "
  "constructed surface should be reported together with its transfer to "
  "defensible alternative representations and its contrast with a spatial "
  "null, so that users can separate informative structure from "
  "optimization-induced apparent performance.")
''')

# ---- cut IJGIS statements/outputs; append TGIS tail
body = body[:body.index('H("Data and codes availability statement")')]
src = head + body + open(f"{A}/_tgis_tail.py").read()
for bad in ["IJGIS", "BLINDED", "anonymi", "International Journal of Geographical Information Science\")"]:
    if bad in src.split("# ---------------- TGIS tail")[0][-200000:] and bad != "International Journal of Geographical Information Science\")":
        raise SystemExit(f"FAIL-LOUD: residual {bad}")
open(f"{A}/build_manuscript_tgis.py", "w").write(src)
print("wrote build_manuscript_tgis.py", src.count("\n"), "lines")
