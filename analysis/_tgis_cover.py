# ---------------- TGIS cover letter (single author: I / my) -------------
c = Document()
c.styles["Normal"].font.name = "Times New Roman"; c.styles["Normal"].font.size = Pt(12)
COVER = [
  "Dear Editors,",
  f"I submit the manuscript \u201c{TITLE}\u201d for consideration as a Research "
  "Article in Transactions in GIS.",
  "The manuscript asks a question that arises whenever a constructed spatial "
  "representation is used for decision support: when an accessibility index "
  "or opportunity surface is optimized using its own scoring rule, what "
  "internal evidence is required before the resulting gain is treated as "
  "informative geographic structure? Because any heterogeneous surface "
  "contains local maxima, optimizing it under its own score produces "
  "apparent improvement by construction. Such improvement is therefore not, "
  "by itself, evidence that the representation is valid, yet constructed "
  "surfaces are routinely optimized in settings where outcome labels cannot "
  "be obtained.",
  "I study this problem with street-hail taxi relocation in central Tokyo, "
  "where operational vacant-taxi telemetry is unavailable. Four public-data "
  f"opportunity surfaces are built on a directed road network ({NSEG} "
  f"hail-feasible segments) and local optimization is audited for {NOR} "
  "origins at 100-500 m walking radii. Apparent gains are large: at 300 m, "
  f"{pc(AB('COMB',300,'frac_pos'))} of origins improve (mean "
  f"{f2(AB('COMB',300,'mean_G'))} SD), and the optimized locations beat a "
  "nearest-major-road heuristic for "
  f"{pc(AB('COMB',300,'gt_nearmaj'))} of origins. The internal stress tests "
  "tell a more cautious story. Transfer between distinct component families "
  f"is weak ({pc(TF('ROAD','ATTR','frac_pos'))} and "
  f"{pc(TF('ATTR','ROAD','frac_pos'))} of origins positive), and spatially "
  "permuted surfaces with identical value distributions reproduce most of "
  "the improvement prevalence while producing larger mean gains. I report "
  "these unfavourable results in full because they are the substance of the "
  "argument: a geographic proxy is not validated merely because it can be "
  "optimized.",
  "The contribution is not a new individual diagnostic. Component ablation, "
  "cross-specification transfer, spatial permutation nulls, heuristic "
  "benchmarks and cluster-aware bootstrap inference are each established. "
  "The contribution is their integration into an internal, "
  "falsification-oriented audit of optimization on a constructed geographic "
  "representation, reported against an explicit evidence hierarchy that "
  "separates computational correctness, within-proxy optimization, "
  "cross-representation transfer and spatial-null discrimination from "
  "external empirical validation, which this study does not provide. The "
  "manuscript makes no claim about real waiting times, hail success, "
  "operational benefit or causal improvement.",
  "I believe the manuscript fits the scope of Transactions in GIS in several "
  "ways. It is a geocomputational study on a directed network representation; "
  "it treats representation and specification uncertainty as part of spatial "
  "data quality; it uses spatial null models and spatial analysis to test "
  "optimized outputs; and it addresses how spatial decision-support outputs "
  "built on constructed surfaces should be reported when labels are "
  "unavailable. The framework is intended to transfer to other constructed "
  "spatial products, such as accessibility indices and siting surfaces.",
  "All inputs are public (OpenStreetMap and National Land Numerical "
  "Information). The analysis code, derived data, canonical numerical "
  "registry from which every reported value is generated, machine-readable "
  f"tables and the raw-data acquisition ledger are openly available at {REPO_URL}. "
  "The Data Availability Statement states the limits of raw-stage recreation.",
  "This manuscript is original, has not been published, and is not under "
  "consideration by any other journal. I am the sole author. I declare no "
  "conflict of interest, and the research received no external funding. "
  "The use of an AI software-engineering agent for code, document generation "
  "and language editing is disclosed in the manuscript; the design, "
  "interpretation and conclusions are my own, and I take full responsibility "
  "for the content. I am submitting under the journal's standard "
  "(subscription) publication route.",
  "Thank you for considering this submission.",
  "Sincerely,", AUTHOR, AMETA["affiliation"], AMETA["email"],
  f"ORCID: https://orcid.org/{AMETA['orcid']}",
]
for t in COVER:
    c.add_paragraph(t)
COVER_WC = sum(_wc(t) for t in COVER)
_meta(c, TITLE + " - cover letter")
c.save(f"{OUT}/TGIS_COVER_LETTER_FINAL.docx")
_st = json.load(open(f"{OUT}/TGIS_MANUSCRIPT_STATS.json")); _st["cover_letter_words"] = COVER_WC
json.dump(_st, open(f"{OUT}/TGIS_MANUSCRIPT_STATS.json", "w"), indent=1)
print("cover letter words", COVER_WC)
