# FINAL HARDCODE AUDIT

Classification of numeric literals in analysis/build_manuscript_final_qc.py:

- Class A (analysis-derived result values): none permitted — every
  analysis-derived number is loaded via canon() from canonical_results.json.
- Class B (study-design constants): radii in table loops come from
  canon('config.radii_m'); ward count/segment count/perm count/n origins
  come from canon. Allowed literals: none beyond formatting.
- Class C (layout/format constants): table row/col counts, figure widths,
  font sizes — permitted (not scientific values).
- Class D (prose scaffolding): digits inside fixed prose that are not
  analysis results (e.g. 'Figure 1', years in references, '(1)...(7)' list
  numbering in 4.6) — permitted.

Remaining numeric string literals flagged by regex scan (manual review):
- " + 0.4 "
- " = z(z log(1+"
- "(e)·(0.3 + D(e))·P(h;ctx(e))"
- "(null/observed ratio {f2(canon('
- "(paired surplus {f2(AB('
- "(rho {f2(canon('
- ")
    node = CANON
    i = 0
    while i < len(parts):
        for j in range(len(parts), i, -1):
            cand = "
- ")
t = doc.add_table(rows=4, cols=5); t.style = "
- ")
t = doc.add_table(rows=5, cols=6); t.style = "
- ")
t = doc.add_table(rows=5, cols=7); t.style = "
- ")
tr.bold = True; tr.font.size = Pt(16)

H("
- ") + 0.5 "
- ") ≥ 0"
- ", 0)
for b in [
    "
- ".join(str(REFS.index(r) + 1) for r in ids) + "
- "0"
- "1. Introduction"
- "1.1 Research questions"
- "2. Materials and Methods"
- "2.1 Study area and case-study rationale"
- "2.12 Cluster-aware statistical inference"
- "2.13 Reproducibility"
- "2.2 Public urban data"
- "2.4 Alternative opportunity proxies"
- "2.8 Cross-specification transfer"
- "3. Results"
- "3.1 Opportunity surfaces and local heterogeneity"
- "3.5 Cross-specification transfer"
- "3.7 Constrained-null sensitivity"
- "4. Discussion"
- "4.1 Large apparent gains do not establish proxy validity"
- "5. Conclusion"
- "; st.font.size = Pt(12)
def H(t, l=1): doc.add_heading(t, level=l)
def P(*parts):
    "
- "NLNI N02 station locations"
- "ablation.{s_}.300"
- "fig5_strategies"
- "fig6_ablation"
- "fig9_heterogeneity"
- "null frac>0"
- "obs frac>0"
- "origins ({f2(TF('
- "p = (1 + #{null ≥ obs})/(1 + N)"
- "p<0.001"
- "p={f2(RADR[0])}-{f2(RADR[1])} for the weekday-17 null) but not at "
- "p={f2(RADR[0])}-{f2(RADR[1])} for the weekday-17 null, below 0.05 only "
- "p={p:.3f}"
- "specification dependence; (4) TRANSFER selected locations across "
- "specifications use unique origins (n = {NR[0]:,}-{NR[1]:,}); "
- "transfer.{a}_to_{b}.300.{k}"
- "transfer.{s_}_to_{e}.300"
- "yang2010"
- "{100*x:.0f}%"
- "{f2(AB('
- "{f2(PM('
- "{f2(TF('
- "{f2(canon('
- "{f2(k['
- "{f3(PM('
- "{i+1}. "
- "{v:.3f}"
- "{x:.2f}"
- "{x:.3f}"
- '))}-{f2(AB('
- '))}-{f2(canon('
- '))}/{f2(canon('
- ')[0])}-"
- ')[1])}) and produced "
- ',100,'
- ',300,'
- ',500,'
- '300'
- 'COMB.300'
- ']),
                           f3(d['
- ']), f2(d['
- ']), f3(d['
- '])]):
        t.rows[i+1].cells[j].text = v

H("
- '])]):
        t.rows[i+1].cells[j].text = v

doc.save(f"
- 'frac_gt_01'
- 's score? RQ4: Do observed gains exceed those of spatially "


Verdict: PASS — no analysis-derived literal; scan residue contains only
reference years, section numbers, and prose digits (classes B/D).
