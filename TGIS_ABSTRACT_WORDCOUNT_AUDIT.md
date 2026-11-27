# Abstract word-count audit

Rule: ≤150 words (TGIS_CURRENT_REQUIREMENTS.md row 4); target 135–145.
Counting rule: whitespace-delimited tokens of the rendered abstract (the same function the builder uses, `len(re.findall(r"\S+", text))`); numbers, "100-500", "(27,887" and "SD)" each count as one token.

Result: **135 words** (`output/TGIS_MANUSCRIPT_STATS.json` → `abstract_words`; the build fails loudly above 150).

Retained elements: (1) general proxy-optimization validity problem; (2) street-hail case, central Tokyo; (3) 27,887 segments / 2,000 origins; (4) 300 m result (98% improved, mean 1.50 SD; 81% beat nearest-major-road heuristic); (5) weak cross-specification transfer (53% and 43% positive); (6) permutation nulls reproduce most improvement prevalence with larger mean gains; (7) "A geographic proxy is not validated merely because it can be optimized."

Removed relative to the previous 169-word version: the per-radius permutation p-value range (kept in Results, §3.6 and Table 5) and "permutation count" (kept in Methods). All values remain canonical lookups.
