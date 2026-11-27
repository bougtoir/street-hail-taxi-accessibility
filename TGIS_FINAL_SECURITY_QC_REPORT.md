# TGIS final security QC report (2026-11-27 02:32 UTC)

| Check | Result |
|---|---|
| Zenodo preview link | REVOKED (DELETE 204; links total 0) |
| Old leaked URL | UNUSABLE (page 404 "Draft not found"; download serves only the login page; incognito verified) |
| Draft 24106479 | still unpublished; draft JSON byte-identical before and after (SHA-256 84b9c581…) |
| Public mirror current tree | CLEAN: NO LIVE SECRET FOUND |
| Future sync | SAFE: EXCLUDE_MAP covers data/raw/zenodo_review and data/raw/journal |
| History purge | NOT REQUIRED (dead credential only) |
| Canonical registry SHA-256 | ee1ce5bb26df5605aec7b803c459056b525de133b7f1d9bf8e81d448e33a22ac, unchanged; registry, tables/, figures/, data/processed/ identical to freeze base f51d0bb |
| Manuscript, PDF, title page, cover, tables, figures | byte-identical before and after this round (no rebuild) |
| `qc_tgis.py --zip` | 35/35 PASS (see TGIS_FINAL_QC_REPORT.md) |
| Package refuses stale files | yes (tampered hash → exit 1) |
| Hardcode audit / p-values from registry | PASS (gate 7) |
| Review credential in submission ZIP | none (JWT/token/nonce/cookie scan) |

**SCIENTIFIC FREEZE PRESERVED**

The ZIP was rebuilt only because the audit and handoff documents it contains changed. Submission members are unchanged.
