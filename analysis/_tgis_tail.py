# ---------------- TGIS tail: statements, references, deferred tables,
# figure captions, separate figure files, title page, cover letter -------
REVIEW = json.load(open(f"{ROOT}/analysis/review_access.json"))
if REVIEW.get("mode") != "public_github":
    raise SystemExit("FAIL-LOUD: TGIS build requires public_github review mode")
REPO_URL = REVIEW["public_url"]
AMETA = json.load(open(f"{ROOT}/analysis/author_meta.json"))
AUTHOR = AMETA["author"]
COI = "The author declares no conflict of interest."
FUNDING = "This research received no external funding."
ACK = FUNDING + " " + AI_STATEMENT
DAS = (
  "The data that support the findings of this study are openly available. "
  "Public source data: OpenStreetMap road, pedestrian and point-of-interest "
  "data (ODbL) retrieved through the Overpass API with OSMnx 2.0.7 "
  + cite("osm") + ", and National Land Numerical Information railway data "
  "(N02, FY2023; MLIT terms of use) " + cite("nlni") + " (Table 1). "
  "Derived study data, the canonical numerical registry from which every "
  "reported analysis value is generated, machine-readable result tables, "
  "the raw-data acquisition ledger with SHA-256 checksums, and the "
  "analysis and document-generation code are openly available in a public "
  "GitHub repository " + cite("repo2026") + " at " + REPO_URL + " (code: "
  "MIT licence; derived tables: CC BY 4.0). Third-party inputs remain "
  "under their original terms. The cached Overpass responses in the "
  "repository rebuild the pedestrian network identically, but the "
  "original point-of-interest responses were not retained and re-querying "
  "OpenStreetMap returns its current state; full raw-stage recreation is "
  "therefore not claimed, and all reported analyses are reproducible from "
  "the archived derived data.")

H("Acknowledgments")
P(ACK)
H("Conflict of Interest Statement")
P(COI)
H("Data Availability Statement")
P(DAS)

def RP(text, para):
    """Render *...* spans in italics (APA 7); no literal asterisks."""
    parts = text.split("*")
    if len(parts) % 2 == 0:
        raise SystemExit(f"FAIL-LOUD: unbalanced italics in {text[:60]}")
    for i, s in enumerate(parts):
        if s:
            para.add_run(s).italic = (i % 2 == 1)

H("References")
if set(REFS) != set(BIB):
    raise SystemExit(f"FAIL-LOUD: uncited/unknown refs {set(BIB) ^ set(REFS)}")
def _apa_key(r):
    return (re.sub(r"[^a-z0-9 ]", "", BIB[r]["ref"].lower().replace("*", "")), BIB[r]["year"])
for rid in sorted(REFS, key=_apa_key):
    rp = doc.add_paragraph()
    RP(BIB[rid]["ref"], rp)
    rp.paragraph_format.left_indent = Inches(0.5)
    rp.paragraph_format.first_line_indent = Inches(-0.5)

from docx.enum.text import WD_BREAK
for T in TABLES:
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    T()
doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
H("Figure captions")
for _n, _c in FIGS:
    P(_c)

def _wc(txt): return len(re.findall(r"\S+", txt))
_names = [p.text for p in doc.paragraphs]
_i0 = _names.index("1. Introduction")
_i1 = _names.index("Acknowledgments")
MAIN_WC = sum(_wc(p.text) for p in doc.paragraphs[_i0:_i1])
ABS_WC = _wc(ABSTRACT)
_r = WC_PARA.add_run(f"Word count: {MAIN_WC:,} words (Introduction to "
                     f"Conclusion); abstract {ABS_WC} words.")
_r.font.size = Pt(10)
WC_PARA.alignment = WD_ALIGN_PARAGRAPH.CENTER
if ABS_WC > 150:
    raise SystemExit(f"FAIL-LOUD: abstract {ABS_WC} words > 150")

from docx.shared import RGBColor
def _black(d):
    for _s in d.styles:
        if _s.type == 1 and (_s.name.startswith("Heading") or _s.name == "Title"):
            _s.font.color.rgb = RGBColor(0, 0, 0)
            _s.font.name = "Times New Roman"

def _meta(d, title):
    _black(d)
    cp = d.core_properties
    cp.author = AUTHOR; cp.last_modified_by = AUTHOR; cp.title = title
    cp.comments = ""; cp.subject = ""; cp.keywords = ""; cp.category = ""
    cp.revision = 1

_meta(doc, TITLE)
doc.save(f"{OUT}/TGIS_MAIN_MANUSCRIPT_FINAL.docx")

import shutil
FIGOUT = f"{OUT}/tgis_figures"
shutil.rmtree(FIGOUT, ignore_errors=True); os.makedirs(FIGOUT)
for k, (_n, _c) in enumerate(FIGS, 1):
    if not _c.startswith(f"Figure {k}. "):
        raise SystemExit(f"FAIL-LOUD: figure order {_n} vs {k}")
    shutil.copyfile(f"{FIG}/{_n}.png", f"{FIGOUT}/Figure_{k}.png")

tdoc = Document()
tdoc.styles["Normal"].font.name = "Times New Roman"; tdoc.styles["Normal"].font.size = Pt(12)
_main_doc = doc; doc = tdoc
for k, T in enumerate(TABLES):
    if k: doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    T()
doc = _main_doc
_meta(tdoc, TITLE + " - tables")
tdoc.save(f"{OUT}/TGIS_TABLES_EDITABLE.docx")

json.dump({"title": TITLE, "title_chars": len(TITLE), "running_title": RUNNING,
           "running_title_chars": len(RUNNING), "main_text_words": MAIN_WC,
           "abstract_words": ABS_WC, "keywords": [k.strip() for k in KEYWORDS.split(";")],
           "n_references": len(REFS), "n_tables": len(TABLES), "n_figures": len(FIGS),
           "n_equations": EQN[0], "review_mode": REVIEW["mode"], "repo_url": REPO_URL},
          open(f"{OUT}/TGIS_MANUSCRIPT_STATS.json", "w"), indent=1)
print("TGIS manuscript saved;", len(REFS), "references;", MAIN_WC, "words; abstract", ABS_WC)

tpg = Document()
tpg.styles["Normal"].font.name = "Times New Roman"; tpg.styles["Normal"].font.size = Pt(12)
tpg.styles["Normal"].paragraph_format.line_spacing = 2.0
tpg.add_heading("Title page", 1)
_p = tpg.add_paragraph(); _p.add_run(TITLE).bold = True
for line in [
    f"Running title: {RUNNING}",
    f"Author: {AUTHOR}",
    f"Affiliation: {AMETA['affiliation']}",
    f"Correspondence: {AUTHOR}, {AMETA['affiliation']}; email: {AMETA['email']}",
    f"ORCID: https://orcid.org/{AMETA['orcid']}",
    f"Article type: Research Article",
    f"Word count: {MAIN_WC:,} words (Introduction to Conclusion); abstract {ABS_WC} words; "
    f"{len(TABLES)} tables; {len(FIGS)} figures; {len(REFS)} references",
]:
    tpg.add_paragraph(line)
for h, t in [("Acknowledgments", ACK), ("Conflict of Interest Statement", COI),
             ("Funding", FUNDING), ("Data Availability Statement", DAS)]:
    tpg.add_heading(h, 2); tpg.add_paragraph(t)
_meta(tpg, TITLE + " - title page")
tpg.save(f"{OUT}/TGIS_TITLE_PAGE_FINAL.docx")

exec(open(f"{ROOT}/analysis/_tgis_cover.py").read())
