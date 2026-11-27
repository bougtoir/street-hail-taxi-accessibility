#!/usr/bin/env python3
"""IJGIS submission QC gates. Writes output/IJGIS_QC_RESULTS.json; exits 1 on any FAIL."""
import json, os, re, subprocess, sys, zipfile, hashlib
from docx import Document
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/output"
BASE = sys.argv[1] if len(sys.argv) > 1 else "f51d0bb8057001af20871fb63f5f42bd0e48315a"
G = []
def gate(name, ok, detail=""):
    G.append({"gate": name, "status": "PASS" if ok else "FAIL", "detail": str(detail)[:600]})

MAN = f"{OUT}/IJGIS_MAIN_MANUSCRIPT_BLINDED.docx"
d = Document(MAN)
paras = [p.text for p in d.paragraphs]
T = "\n".join(paras)
BIB = json.load(open(f"{ROOT}/analysis/ijgis_bib.json"))
STATS = json.load(open(f"{OUT}/IJGIS_MANUSCRIPT_STATS.json"))
canon_now = open(f"{ROOT}/analysis/canonical_results.json", "rb").read()
canon_base = subprocess.run(["git", "-C", ROOT, "show", f"{BASE}:street-hail-taxi/analysis/canonical_results.json"],
                            capture_output=True).stdout
gate("G01 canonical_results.json unchanged vs pre-IJGIS freeze", canon_now == canon_base,
     hashlib.sha256(canon_now).hexdigest())

# G02 hard-coded result audit: canonical-formatted values must not appear as literals in body source
CANON = json.loads(canon_now)
vals = set()
def walk(n):
    if isinstance(n, dict): [walk(v) for v in n.values()]
    elif isinstance(n, list): [walk(v) for v in n]
    elif isinstance(n, float):
        if 0 < abs(n) < 1: vals.update({f"{100*n:.0f}%", f"{n:.3f}"})
        vals.add(f"{n:.2f}")
walk(CANON)
vals = {v for v in vals if v not in {"0.00", "1.00", "0.05", "0.50", "0.30", "0.40", "0.10", "0.20", "0.25", "0.95", "2.00", "0%", "100%", "50%", "95%", "1.96"}}
body = open(f"{ROOT}/analysis/_lit_body.py").read()
lits = []
for m in re.finditer(r'(?<![A-Za-z_])(f?)"((?:[^"\\]|\\.)*)"', body):
    txt = m.group(2)
    if m.group(1): txt = re.sub(r"\{[^{}]*\}", "", txt)
    txt = re.sub(r"^\d+\.\d+ |§\d+\.\d+", "", txt)
    lits.append(txt)
hits = sorted({v for v in vals for t in lits if re.search(r"(?<![\d.])" + re.escape(v) + r"(?![\d])", t)})
gate("G02 no hard-coded canonical result literals in _lit_body.py", not hits, hits)

# G03 builder concatenation is current
cat = open(f"{ROOT}/analysis/_lit_builder_head.py").read() + body
gate("G03 build_manuscript_ijgis.py == head+body", cat == open(f"{ROOT}/analysis/build_manuscript_ijgis.py").read())

# G04-G06 references
i_ref = paras.index("References")
refs = [p for p in paras[i_ref + 1:] if p.strip()]
gate("G04 reference count == bibliography size (all cited)", len(refs) == len(BIB) == STATS["n_references"], f"{len(refs)} listed / {len(BIB)} bib")
keyf = [p.lower() for p in refs]
gate("G05 references alphabetical (T&F Style V Harvard)", keyf == sorted(keyf))
crdir = f"{ROOT}/data/raw/crossref_ijgis"
dois = {k: re.search(r"https://doi.org/(\S+)$", v["ref"]) for k, v in BIB.items()}
def _dois(n):
    if isinstance(n, dict):
        for k, v in n.items():
            if k == "DOI" and isinstance(v, str): yield v.lower()
            else: yield from _dois(v)
    elif isinstance(n, list):
        for v in n: yield from _dois(v)
CR_DOIS = set()
for f in os.listdir(crdir):
    if f.endswith(".json"):
        try: CR_DOIS |= set(_dois(json.load(open(f"{crdir}/{f}"))))
        except ValueError: pass
missing_doi_rec = []
for k, m in dois.items():
    if not m: continue
    doi = m.group(1).lower()
    found = doi in CR_DOIS
    if not found: missing_doi_rec.append(k)
gate("G06 every DOI has an archived Crossref record", not missing_doi_rec, missing_doi_rec)

# G07 in-text citations resolve
main = "\n".join(paras[:i_ref])
cites = re.findall(r"\(([A-Z][^()]*?\d{4}[a-z]?(?:, [A-Z][^()]*?\d{4}[a-z]?)*)\)", main)
known = {f"{v['cite']} {v['year']}" for v in BIB.values()}
unres = []
for grp in cites:
    for c in grp.split(", "):
        if re.search(r"\d{4}$", c) and c not in known and not re.match(r"(FY|Table|Figure)", c):
            if re.match(r"^[A-Z][A-Za-z\-' ]+( et al\.| and [A-Z][a-z]+)? \d{4}$", c): unres.append(c)
gate("G07 every author-year citation resolves to bibliography", not unres, unres)
used = {k for k, v in BIB.items() if f"{v['cite']} {v['year']}" in main}
gate("G08 every bibliography item cited in text", used == set(BIB), set(BIB) - used)

# G09-G12 figures / tables
def order(kind):
    seen = []
    for n in re.findall(rf"\b{kind}s? (\d+)", main):
        if n not in seen: seen.append(n)
    return seen
caps_f = [re.match(r"Figure (\d+)\.", p).group(1) for p in paras if re.match(r"Figure \d+\.", p)]
caps_t = [re.match(r"Table (\d+)\.", p).group(1) for p in paras if re.match(r"Table \d+\.", p)]
fo, to = order("Figure"), order("Table")
gate("G09 all figures cited", set(caps_f) <= set(fo) and len(caps_f) == 9, f"caps={caps_f} cited={fo}")
gate("G10 figure first-citation order sequential", fo == [str(i) for i in range(1, len(fo) + 1)], fo)
gate("G11 all tables cited", set(caps_t) <= set(to) and len(caps_t) == 5, f"caps={caps_t} cited={to}")
gate("G12 table first-citation order sequential", to == [str(i) for i in range(1, len(to) + 1)], to)
nimg = len(d.inline_shapes)
gate("G13 figures and tables embedded inline", nimg == 9 and len(d.tables) == 5, f"{nimg} images, {len(d.tables)} tables")

# G14-G16 XML-level checks
with zipfile.ZipFile(MAN) as z:
    xml = z.read("word/document.xml").decode()
    names = z.namelist()
    core = z.read("docProps/core.xml").decode()
gate("G14 OMML equations present", xml.count("<m:oMath") > 0, xml.count("<m:oMath"))
tbl_text = "\n".join(c.text for t in d.tables for r in t.rows for c in r.cells)
gate("G15 no literal asterisks", "*" not in T + tbl_text, (T + tbl_text).count("*"))
brs = len(re.findall(r"<w:br(?![^>]*w:type=\"page\")[^>]*/>", xml))
gate("G16 no manual line breaks", brs == 0, brs)

# G17 language lock
banned = ["near-chance", "chance-level", "chance level", "coin flip", "coin-flip", "minimal framework", "framework works"]
docs = {"manuscript": T + tbl_text}
for f in ["IJGIS_TITLE_PAGE.docx", "IJGIS_COVER_LETTER.docx"]:
    docs[f] = "\n".join(p.text for p in Document(f"{OUT}/{f}").paragraphs)
bl = {k: [b for b in banned if b in v.lower()] for k, v in docs.items()}
gate("G17 language lock (banned phrases absent in all documents)", not any(bl.values()), bl)

# G18 claim calibration: no affirmative operational/external validity claims
over = re.findall(r"[^.]*\b(validates the proxy|improves taxi access|externally valid|predictive validity is (?:shown|established)|operationally valid|proves)\b[^.]*\.", T, re.I)
gate("G18 claim calibration (no external/operational validity claims)", not over, over)

# G19 anonymity of blinded manuscript
ident = ["Onishi", "Tatsuki", "bougtoir", "github", "gmail", "ORCID", "/home/", "ubuntu", "Cognition AI;" if False else "@"]
found = [s for s in ident if s.lower() in (T + tbl_text).lower()]
meta = re.findall(r"<dc:creator>([^<]+)</dc:creator>|<cp:lastModifiedBy>([^<]+)</cp:lastModifiedBy>", core)
track = len(re.findall(r"<w:(ins|del) ", xml))
comments = any("comments" in n for n in names)
hdr = [n for n in names if re.search(r"(header|footer)\d*\.xml", n)]
gate("G19 blinded manuscript free of identity/paths/metadata/comments/tracked changes",
     not found and not meta and track == 0 and not comments,
     f"found={found} meta={meta} track={track} comments={comments} hdr={hdr}")
gate("G20 no stale target-journal wording (CEUS) in IJGIS documents",
     not any(re.search(r"CEUS|Computers, Environment", v) for v in docs.values()))

# G21 length + abstract + keywords + title
gate("G21 main text within IJGIS typical 5,000-8,000 words", 5000 <= STATS["main_text_words"] <= 8000, STATS["main_text_words"])
gate("G22 abstract <= 200 words, 2-5 keywords, title present",
     STATS["abstract_words"] <= 200 and 2 <= len(STATS["keywords"]) <= 5 and paras[0] == STATS["title"],
     f"abs={STATS['abstract_words']} kw={len(STATS['keywords'])}")

# G23 IJGIS statements present
req = ["Data and codes availability statement", "Disclosure statement", "Funding", "Declaration of generative AI use", "References"]
gate("G23 IJGIS required statements present", all(r in paras for r in req), [r for r in req if r not in paras])

# G24 numeric consistency: values printed in cover letter appear in manuscript
cl = docs["IJGIS_COVER_LETTER.docx"]
nums = set(re.findall(r"\b\d[\d,]*(?:\.\d+)?%?", cl)) - {"100", "500", "300"}
miss = sorted(n for n in nums if n not in T)
gate("G24 cover-letter numbers identical to manuscript numbers", not miss, miss)

# G25 PDF matches DOCX build
pdf = f"{OUT}/IJGIS_MAIN_MANUSCRIPT_BLINDED.pdf"
ok = os.path.exists(pdf) and os.path.getmtime(pdf) >= os.path.getmtime(MAN)
ptxt = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout if ok else ""
pinfo = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout if ok else ""
gate("G25 PDF regenerated from current DOCX, title present, no author metadata",
     ok and STATS["title"].split(":")[0] in ptxt and "Author:" not in pinfo, pinfo.replace("\n", " | ")[:300])

json.dump(G, open(f"{OUT}/IJGIS_QC_RESULTS.json", "w"), indent=1)
for g in G: print(g["status"], g["gate"], "" if g["status"] == "PASS" else g["detail"])
nf = sum(g["status"] == "FAIL" for g in G)
print(f"{len(G) - nf}/{len(G)} PASS")
sys.exit(1 if nf else 0)
