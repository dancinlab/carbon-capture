#!/usr/bin/env python3
"""Run script for H_016 — ambient H2O/CO2 molar co-load ratio."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

r_50_25 = cc.humidity_to_co2_ratio(0.5, 25)
r_100_40 = cc.humidity_to_co2_ratio(1.0, 40)
r_20_10 = cc.humidity_to_co2_ratio(0.2, 10)
r_80_25 = cc.humidity_to_co2_ratio(0.8, 25)
r_20_25 = cc.humidity_to_co2_ratio(0.2, 25)
r_0_25 = cc.humidity_to_co2_ratio(0.0, 25)
try:
    cc.humidity_to_co2_ratio(1.5, 25)
    over_rh_raises = False
except ValueError:
    over_rh_raises = True

metrics = {
    "ratio_50rh_25c": r_50_25,
    "ratio_100rh_40c": r_100_40,
    "ratio_20rh_10c": r_20_10,
    "ratio_80rh_25c": r_80_25,
    "ratio_20rh_25c": r_20_25,
    "ratio_0rh_25c": r_0_25,
    "over_rh_raises": over_rh_raises,
}

falsifiers = [
    cc.Falsifier("F-016-1", lambda m: not (30.0 <= m["ratio_50rh_25c"] <= 45.0),
                 "ratio(50%,25C) outside [30,45]"),
    cc.Falsifier("F-016-2", lambda m: m["ratio_100rh_40c"] < 150.0,
                 "hot humid air co-load < 150x"),
    cc.Falsifier("F-016-3", lambda m: m["ratio_20rh_10c"] < 3.0,
                 "cold/dry air water does not exceed CO2 by 3x"),
    cc.Falsifier("F-016-4", lambda m: m["ratio_0rh_25c"] != 0.0,
                 "0% RH not zero water (bounds)"),
    cc.Falsifier("F-016-5", lambda m: abs(m["ratio_80rh_25c"] - 4 * m["ratio_20rh_25c"]) > 1e-6,
                 "ratio not linear in RH at fixed T (neg control)"),
    cc.Falsifier("F-016-6", lambda m: not m["over_rh_raises"],
                 "RH>100% did not raise (domain guard)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "SUPPORTED = ambient air carries ~37x more H2O than CO2 (50%/25C), up to ~170x hot/humid -> "
    "water is the dominant minor-species duty the L0 candidate list omits."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_016 — humidity co-load vs CO2")
print(f"  H2O/CO2 @ 50% RH, 25C = {r_50_25:.1f}x")
print(f"  H2O/CO2 @ 100% RH,40C = {r_100_40:.1f}x")
print(f"  H2O/CO2 @ 20% RH, 10C = {r_20_10:.1f}x")
print(f"  RH-linearity: ratio(80%)={r_80_25:.1f} vs 4x ratio(20%)={4*r_20_25:.1f}")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (water co-load dominates; first-order DAC constraint)")
