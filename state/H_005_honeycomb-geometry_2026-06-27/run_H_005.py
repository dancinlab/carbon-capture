#!/usr/bin/env python3
"""Run script for H_005 — honeycomb reactor geometry (hexagon optimal among tilers)."""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

tiling = {n: cc.perimeter_area_ratio(n) for n in (3, 4, 6)}  # only regular tilers
pa12 = cc.perimeter_area_ratio(12)
pa1000 = cc.perimeter_area_ratio(1000)
circle = 2.0 * math.sqrt(math.pi)
argmin_tiling = min(tiling, key=tiling.get)

# F-005-6: domain guard — n<3 must raise.
try:
    cc.perimeter_area_ratio(2)
    n2_raised = False
except ValueError:
    n2_raised = True

metrics = {
    "pa_3": tiling[3], "pa_4": tiling[4], "pa_6": tiling[6],
    "pa_12": pa12, "pa_1000": pa1000, "circle_limit": circle,
    "argmin_over_tilers": argmin_tiling,
    "hex_ordering_ok": tiling[6] < tiling[4] < tiling[3],
    "n2_raises": n2_raised,
}

falsifiers = [
    cc.Falsifier("F-005-1", lambda m: m["argmin_over_tilers"] != 6,
                 "argmin over {3,4,6} is not the hexagon"),
    cc.Falsifier("F-005-2", lambda m: not m["hex_ordering_ok"],
                 "ordering pa(6) < pa(4) < pa(3) violated"),
    cc.Falsifier("F-005-3", lambda m: m["pa_12"] >= m["pa_6"],
                 "n=12 not below n=6 (would make hexagon the global min — overclaim)"),
    cc.Falsifier("F-005-4", lambda m: m["pa_1000"] < m["circle_limit"],
                 "pa(1000) below the circle limit 2*sqrt(pi) (crossed from below)"),
    cc.Falsifier("F-005-5", lambda m: abs(m["pa_4"] - 4.0) > 1e-9,
                 "unit-area square perimeter != 4 (closed-form anchor drift)"),
    cc.Falsifier("F-005-6", lambda m: not m["n2_raises"],
                 "n=2 did not raise (domain guard)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_005 — honeycomb reactor geometry")
print(f"  P/sqrt(A): n=3 {tiling[3]:.4f}  n=4 {tiling[4]:.4f}  n=6 {tiling[6]:.4f}  (tilers)")
print(f"  P/sqrt(A): n=12 {pa12:.4f}  n=1000 {pa1000:.4f}  circle {circle:.4f}")
print(f"  argmin over tilers {{3,4,6}} = n={argmin_tiling}  (hexagon best space-filling cell)")
print(f"  honest limit: n=12 ({pa12:.4f}) < n=6 ({tiling[6]:.4f}) -> hexagon NOT the global min")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}")
