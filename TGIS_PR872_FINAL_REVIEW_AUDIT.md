# PR #872 final review audit (2026-11-27 02:32 UTC)

| Item | State |
|---|---|
| PR | https://github.com/bougtoir/wip/pull/872, open, not merged |
| Head before this round | 93f62dbdcd09ebef5de4199f4f9b19b16bd3c615 (devin/1795503313-tgis) |
| Mergeability | GitHub: mergeable, no conflicts. Base master is 15 commits ahead; local `git merge-tree` with origin/master is clean, keeps the sync EXCLUDE_MAP line and the frozen canonical registry (SHA ee1ce5bb…). No branch update needed |
| CI | Devin Review check: passed. No other required checks; GitHub Actions in wip refused for billing on 2026-11-24 |
| Review threads | Devin Review summary (2026-11-24 07:33 UTC): 4 findings fixed. One open item (legacy IJGIS builder needs `download_url`) was rejected as intended (superseded and locked IJGIS package; the builder fails loudly). Security finding (Zenodo preview link) resolved in this round, see TGIS_ZENODO_PREVIEW_REVOCATION_AUDIT.md |

## Earlier findings, re-tested now (not taken from old comments)

| Finding | Re-test | Result |
|---|---|---|
| ZIP verification without archive | ZIP moved away, `qc_tgis.py --zip`: gate 35 FAIL, exit 1; ZIP restored: 35/35, exit 0 | resolved |
| Stale QC after rebuild | One input hash in TGIS_QC_RESULTS.json tampered: `make_tgis_package.py` exits 1 (FAIL-LOUD), and the existing ZIP stays byte-identical | resolved |
| Default QC (no --zip) | gate 35 SKIP, exit 0 | resolved |
| Hard-coded p-value | builder line `p={PM('weekday_17','100','emp_p_frac'):.1f}`; rendered "not at 100 m (p=1.0)"; gate 7 PASS with literal p-value scan | resolved |
