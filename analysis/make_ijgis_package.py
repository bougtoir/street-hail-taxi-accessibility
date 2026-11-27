#!/usr/bin/env python3
"""Build IJGIS submission ZIP and anonymized review reproduction bundle with
exact manifests; verify ZIP contents == manifest and scan the anonymized
bundle for identifying strings."""
import csv, glob, hashlib, io, os, re, sys, zipfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/output"
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

SUBMISSION = (
    ["output/IJGIS_MAIN_MANUSCRIPT_BLINDED.docx", "output/IJGIS_MAIN_MANUSCRIPT_BLINDED.pdf",
     "output/IJGIS_TITLE_PAGE.docx", "output/IJGIS_COVER_LETTER.docx",
     "output/IJGIS_MANUSCRIPT_STATS.json", "output/IJGIS_QC_RESULTS.json",
     "PRE_IJGIS_FREEZE.md", "IJGIS_CURRENT_REQUIREMENTS.md", "IJGIS_ARTICLE_TYPE_DECISION.md",
     "IJGIS_ANONYMITY_RISK_AUDIT.md", "IJGIS_PREPRINT_POLICY_AUDIT.md", "IJGIS_OPEN_DATA_FAIR_AUDIT.md",
     "IJGIS_CITATION_ECOLOGY_AUDIT.md", "IJGIS_CITATION_ECOLOGY_FINAL.md", "IJGIS_NOVELTY_AUDIT.md",
     "HOSTILE_REVIEW_IJGIS_FINAL.md", "IJGIS_REFERENCE_AUDIT.md", "IJGIS_FIGURE_TABLE_AUDIT.md",
     "IJGIS_FINAL_QC_REPORT.md", "FINAL_HANDOFF_IJGIS.txt",
     "analysis/canonical_results.json", "analysis/_lit_builder_head.py", "analysis/_lit_body.py",
     "analysis/concat_builder.py", "analysis/build_manuscript_ijgis.py", "analysis/make_ijgis_bib.py",
     "analysis/ijgis_bib.json", "analysis/qc_ijgis.py", "analysis/make_ijgis_package.py",
     "data/raw/journal/ACQUISITION_LEDGER.csv", "data/raw/crossref_ijgis/ACQUISITION_LEDGER.csv"]
    + sorted(os.path.relpath(p, ROOT) for p in glob.glob(f"{ROOT}/figures/fig*.p*"))
    + [f"tables/{t}" for t in ["ablation_summary_clustered.csv", "transfer_summary.csv",
                               "permutation_null.json", "strategy_comparison.csv",
                               "temporal_heterogeneity.csv", "ward_heterogeneity.csv",
                               "sigma_sensitivity.json", "ablation_rank_agreement.csv"]])

PIPE = ["download_data.py", "build_segments.py", "run_relocation.py", "analyze_stats.py",
        "run_ablation.py", "run_ceus_analyses.py", "make_figures.py", "make_ceus_figures.py",
        "make_framework_figure.py", "build_canonical_results.py"]
ANON = ([f"analysis/{p}" for p in PIPE] + ["analysis/canonical_results.json", "REPRO_README.md", "LICENSE"]
        + sorted(os.path.relpath(p, ROOT) for p in glob.glob(f"{ROOT}/tables/*"))
        + sorted(os.path.relpath(p, ROOT) for p in glob.glob(f"{ROOT}/figures/fig*.p*"))
        + sorted(os.path.relpath(p, ROOT) for p in glob.glob(f"{ROOT}/data/processed/*") if not p.endswith(".log"))
        + sorted(os.path.relpath(p, ROOT) for p in glob.glob(f"{ROOT}/cache/*.json")))
ANON_EXTRA = {"REPRO_README.md": f"{ROOT}/analysis/anon_bundle/REPRO_README.md",
              "LICENSE": f"{ROOT}/analysis/anon_bundle/LICENSE"}
IDENT = re.compile(rb"bougtoir|onishi|tatsuki|/home/ubuntu|street-hail-taxi-accessibility|devin/17", re.I)

def build(name, files, extra=None, scan=False):
    extra = extra or {}
    rows, zp = [], f"{OUT}/{name}.zip"
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in files:
            src = extra.get(rel, f"{ROOT}/{rel}")
            if not os.path.exists(src): sys.exit(f"FAIL-LOUD: missing {rel}")
            data = open(src, "rb").read()
            if scan and IDENT.search(data) and not rel.startswith("cache/"):
                sys.exit(f"FAIL-LOUD: identifying string in {rel}: {IDENT.search(data).group()}")
            z.writestr(rel, data)
            rows.append([rel, len(data), hashlib.sha256(data).hexdigest()])
    man = f"{OUT}/{name}_MANIFEST.csv"
    with open(man, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["path", "bytes", "sha256"]); w.writerows(rows)
    with zipfile.ZipFile(zp) as z:
        got = sorted(i.filename for i in z.infolist())
        for i in z.infolist():
            if hashlib.sha256(z.read(i)).hexdigest() != dict((r[0], r[2]) for r in rows)[i.filename]:
                sys.exit(f"FAIL-LOUD: hash mismatch {i.filename}")
    assert got == sorted(r[0] for r in rows), "ZIP != manifest"
    stale = [g for g in got if re.search(r"CEUS|LITERATURE_FINAL|_revised|STRESS_TEST|scratch|~\$", g)]
    assert not stale, stale
    print(f"{name}.zip: {len(got)} files == manifest; sha256 {sha(zp)}")

FINAL_COPIES = {"IJGIS_MAIN_MANUSCRIPT_BLINDED.docx": "IJGIS_MAIN_MANUSCRIPT_BLINDED_FINAL.docx",
                "IJGIS_MAIN_MANUSCRIPT_BLINDED.pdf": "IJGIS_MAIN_MANUSCRIPT_BLINDED_FINAL.pdf",
                "IJGIS_TITLE_PAGE.docx": "IJGIS_TITLE_PAGE_FINAL.docx",
                "IJGIS_COVER_LETTER.docx": "IJGIS_COVER_LETTER_FINAL.docx"}
SUBMISSION_V2 = ([f"output/{v}" for v in FINAL_COPIES.values()]
    + [f for f in SUBMISSION if f.startswith(("output/IJGIS_MANUSCRIPT_STATS", "output/IJGIS_QC_RESULTS"))]
    + ["output/IJGIS_ANON_REVIEW_REPRO_BUNDLE_MANIFEST.csv"]
    + [f for f in SUBMISSION if not f.startswith("output/") and f != "FINAL_HANDOFF_IJGIS.txt"]
    + ["IJGIS_ANON_BUNDLE_PREUPLOAD_AUDIT.md", "IJGIS_FIGSHARE_PRIVATE_LINK_AUDIT.md",
       "IJGIS_GITHUB_PRIVACY_ACTION.md", "IJGIS_DATA_CODE_AVAILABILITY_PLAN.md",
       "IJGIS_FINAL_ANONYMITY_AUDIT.md", "IJGIS_FINAL_QC_REPORT_v2.md", "FINAL_HANDOFF_IJGIS_FINAL.txt",
       "analysis/review_access.json", "analysis/author_meta.json"])

FINAL_COPIES_V2 = {"IJGIS_MAIN_MANUSCRIPT_BLINDED.docx": "IJGIS_MAIN_MANUSCRIPT_BLINDED_FINAL_v2.docx",
                   "IJGIS_MAIN_MANUSCRIPT_BLINDED.pdf": "IJGIS_MAIN_MANUSCRIPT_BLINDED_FINAL_v2.pdf",
                   "IJGIS_TITLE_PAGE.docx": "IJGIS_TITLE_PAGE_FINAL_v2.docx",
                   "IJGIS_COVER_LETTER.docx": "IJGIS_COVER_LETTER_FINAL_v2.docx"}
SUBMISSION_V3 = ([f"output/{v}" for v in FINAL_COPIES_V2.values()]
    + [f for f in SUBMISSION_V2 if f.startswith(("output/IJGIS_MANUSCRIPT_STATS", "output/IJGIS_QC_RESULTS"))]
    + [f for f in SUBMISSION_V2 if not f.startswith("output/")
       and f not in ("IJGIS_FINAL_QC_REPORT_v2.md", "FINAL_HANDOFF_IJGIS_FINAL.txt", "IJGIS_FINAL_ANONYMITY_AUDIT.md")]
    + ["data/raw/anon_github/03_review_repo_MANIFEST.csv", "data/raw/anon_github/acquisition_ledger.jsonl",
       "IJGIS_ANON_GITHUB_FEASIBILITY.md", "IJGIS_ANON_GITHUB_CONTENT_AUDIT.md", "IJGIS_ANON_GIT_METADATA_AUDIT.md",
       "IJGIS_ANON_GITHUB_EXTERNAL_VIEW_AUDIT.md", "IJGIS_ANON_REPO_FRESH_CLONE_REPRODUCTION.md",
       "IJGIS_FINAL_ANONYMITY_AUDIT_v2.md", "IJGIS_FINAL_QC_REPORT_v3.md", "FINAL_HANDOFF_IJGIS_FINAL_v2.txt"])

if __name__ == "__main__":
    which = sys.argv[1:] or ["anon", "submission"]
    if "anon" in which:
        build("IJGIS_ANON_REVIEW_REPRO_BUNDLE", ANON, ANON_EXTRA, scan=True)
    if "submission" in which:
        build("IJGIS_submission_FINAL_LOCKED", SUBMISSION)
    if "final" in which:
        import shutil
        for a, b in FINAL_COPIES.items():
            shutil.copyfile(f"{OUT}/{a}", f"{OUT}/{b}")
            if sha(f"{OUT}/{a}") != sha(f"{OUT}/{b}"): sys.exit(f"FAIL-LOUD: copy {b}")
        build("IJGIS_submission_FINAL_LOCKED_v2", SUBMISSION_V2)
    if "final_v3" in which:
        import shutil
        for a, b in FINAL_COPIES_V2.items():
            shutil.copyfile(f"{OUT}/{a}", f"{OUT}/{b}")
            if sha(f"{OUT}/{a}") != sha(f"{OUT}/{b}"): sys.exit(f"FAIL-LOUD: copy {b}")
        if "zenodo" in open(f"{ROOT}/analysis/review_access.json").read().split('"superseded"')[0].lower():
            sys.exit("FAIL-LOUD: review access not in Anonymous GitHub mode")
        build("IJGIS_submission_FINAL_LOCKED_v3", SUBMISSION_V3)
