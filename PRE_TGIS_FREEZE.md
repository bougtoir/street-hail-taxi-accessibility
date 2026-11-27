# Pre-TGIS freeze record

- Scientific analysis frozen. No data, model, design, numerical result or figure changed.
- `analysis/canonical_results.json` SHA-256 `ee1ce5bb26df5605aec7b803c459056b525de133b7f1d9bf8e81d448e33a22ac` (identical to wip master and to the pre-retarget record).
- Frozen builder sources reused unmodified: `analysis/_lit_builder_head.py`, `analysis/_lit_body.py`. The TGIS builder `analysis/build_manuscript_tgis.py` is generated from them by `analysis/make_tgis_builder.py` (explicit, fail-loud text edits limited to format and framing) plus `_tgis_tail.py` and `_tgis_cover.py`.
- Figures: `figures/*.png` reused byte-for-byte (copied to `output/tgis_figures/Figure_k.png`).
- Tables: same table functions; only their position changes (after References).
