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

