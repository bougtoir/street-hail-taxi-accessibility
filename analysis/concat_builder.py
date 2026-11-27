#!/usr/bin/env python3
"""Concatenate builder sources into the single runnable IJGIS builder."""
import os
A = os.path.dirname(os.path.abspath(__file__))
src = "".join(open(f"{A}/{f}").read() for f in ["_lit_builder_head.py", "_lit_body.py"])
open(f"{A}/build_manuscript_ijgis.py", "w").write(src)
print("wrote build_manuscript_ijgis.py", src.count("\n"), "lines")
