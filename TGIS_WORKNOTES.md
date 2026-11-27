# TGIS session work notes (internal; session devin-4cfa6bb76be647958cdba97b4026ca2a)
Branch devin/1795503313-tgis from wip master 12ed91971.
Mirror bougtoir/street-hail-taxi-accessibility PRIVATE; GITHUB_REPO_CREATE_TOKEN has admin (can PATCH private=false). Anon upstream private.
Live Wiley journal pages (onlinelibrary.wiley.com/page/journal/14679671/...) Cloudflare-blocked to curl, Playwright CDP and GUI Chrome (checkbox fails) on 2026-11-24.
Archived evidence data/raw/journal/tgis (ledger ACQUISITION_LEDGER.csv):
- 01 forauthors Wayback 2022-03-08 (latest snapshot): single-blind; Free Format (any ref style at initial submission; tables/figures inline or separate);
  abstract <=150 words, no citations; 5-6 keywords; 12-pt Times/Helvetica/Courier, double-spaced; tables on separate pages after refs; figures separate files;
  display equations numbered sequentially; refs APA (6th ed. in 2022 text; issue numbers omitted unless each issue starts p.1; DOI for all);
  title page: informative title without abbreviations, running title <40 chars, full names, affiliations, COI, acknowledgments; funding in Acknowledgments;
  data: expects public repository archiving + DAS with link & data citation; scripts publicly archived whenever possible; ORCID ID requested;
  submission portal Research Exchange wiley.atyponrex.com/journal/TGIS; optional OnlineOpen (CC) vs standard copyright.
- 02 journal home Wayback 2025-07-02: JIF 2.3, CiteScore 4.6, acceptance 34%; OA optional (hybrid; OA fee only if chosen).
- 05 Wiley data sharing policy (live): all articles need DAS.
- 08 Wiley Free Format (live).
Pending: AI guideline page (06 returned stub), preprint policy (03 stub, JS) -> try other URLs.
- 11 Wiley AI guidelines (live): AI disclosure in Acknowledgments (drafting/editing/formatting) AND in Methods (methodology/data/analysis/literature).
- 12 Wiley self-archiving (live): submitted preprint may be self-archived any time.
Plan: new files _tgis_builder_head.py/_tgis_body.py -> build_manuscript_tgis.py; make_tgis_bib.py -> tgis_bib.json (APA7); qc_tgis.py; make_tgis_package.py. IJGIS files untouched.
