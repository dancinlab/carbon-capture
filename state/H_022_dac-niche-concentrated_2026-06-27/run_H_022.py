#!/usr/bin/env python3
"""Run script for H_022 — electric capture's right niche is concentrated CO2."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

air_dilute = cc.air_volume_per_ton_co2(420e-6)
air_flue = cc.air_volume_per_ton_co2(0.12)
air_ratio = air_dilute / air_flue
floor_air = cc.min_separation_work(420e-6) / 1000.0
floor_flue = cc.min_separation_work(0.12) / 1000.0
floor_ratio = floor_air / floor_flue

monotone = (cc.air_volume_per_ton_co2(0.12) < cc.air_volume_per_ton_co2(0.01)
            < cc.air_volume_per_ton_co2(420e-6))
purer_less = cc.air_volume_per_ton_co2(0.99) <= cc.air_volume_per_ton_co2(0.12)

metrics = {
    "air_ratio_air_over_flue": air_ratio,
    "floor_ratio_air_over_flue": floor_ratio,
    "flue_floor_kj_mol": floor_flue,
    "monotone_dilution": monotone,
    "purer_needs_less_air": purer_less,
}

falsifiers = [
    cc.Falsifier("F-022-1", lambda m: m["air_ratio_air_over_flue"] < 100.0,
                 "air dilution penalty < 100x (DAC not specially hard)"),
    cc.Falsifier("F-022-2", lambda m: m["floor_ratio_air_over_flue"] < 2.0,
                 "concentrated not >= 2x thermodynamically cheaper"),
    cc.Falsifier("F-022-3", lambda m: m["flue_floor_kj_mol"] > 6.0,
                 "flue floor > 6 kJ/mol (not near the cheap end)"),
    cc.Falsifier("F-022-4", lambda m: not m["purer_needs_less_air"],
                 "purer source does not need less air (bounds)"),
    cc.Falsifier("F-022-5", lambda m: not m["monotone_dilution"],
                 "air volume not monotone in dilution (neg control)"),
    cc.Falsifier("F-022-6", lambda m: not (m["air_ratio_air_over_flue"] > m["floor_ratio_air_over_flue"]),
                 "air ratio not >> floor ratio (separation work, not air handling, is the wall)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "SUPPORTED = electric capture is mis-TARGETED not wrong-tech: on flue (12% CO2) it needs "
    "286x less air and a 3.7x lower floor than dilute air -> point-source = electric, dilute air "
    "on a fossil grid = free-energy (H_020)."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_022 — electric capture's niche is concentrated CO2")
print(f"  air volume penalty (420 ppm / 12% flue) = {air_ratio:.0f}x less air for flue")
print(f"  separation floor (air {floor_air:.2f} / flue {floor_flue:.2f} kJ/mol) = {floor_ratio:.1f}x lower for flue")
print(f"  air ratio ({air_ratio:.0f}x) >> floor ratio ({floor_ratio:.1f}x) -> air HANDLING is the dilute-DAC wall")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (point-source = electric; dilute air on a fossil grid = free-energy)")
