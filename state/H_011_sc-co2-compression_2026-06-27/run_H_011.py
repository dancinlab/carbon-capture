#!/usr/bin/env python3
"""Run script for H_011 — SC-CO2 compression work to 12 MPa for storage."""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

PC_CO2_BAR = 73.8
T = 298.15
floor = cc.min_separation_work(420e-6) / 1000.0

work = cc.isothermal_compression_work(120.0, 1.0, T) / 1000.0   # kJ/mol
nc_zero = cc.isothermal_compression_work(1.0, 1.0, T)            # 0 at ratio 1
doubling = (cc.isothermal_compression_work(240.0, 1.0, T) - cc.isothermal_compression_work(120.0, 1.0, T)) / 1000.0
expected_doubling = cc.R_GAS * T * math.log(2) / 1000.0

metrics = {
    "floor_kj_mol": floor,
    "compression_kj_mol": work,
    "ratio_to_floor": work / floor,
    "supercritical": 120.0 > PC_CO2_BAR,
    "nc_zero_ratio_work": nc_zero,
    "doubling_delta_kj_mol": doubling,
    "expected_doubling_kj_mol": expected_doubling,
}

falsifiers = [
    cc.Falsifier("F-011-1", lambda m: not (11.0 <= m["compression_kj_mol"] <= 13.0),
                 "compression not in [11,13] kJ/mol"),
    cc.Falsifier("F-011-2", lambda m: not (0.4 <= m["ratio_to_floor"] <= 0.8),
                 "compression/floor outside [0.4,0.8]"),
    cc.Falsifier("F-011-3", lambda m: not m["supercritical"],
                 "120 bar not above CO2 critical pressure (wrong regime)"),
    cc.Falsifier("F-011-4", lambda m: m["nc_zero_ratio_work"] != 0.0,
                 "work at pressure ratio 1 is not zero (bounds)"),
    cc.Falsifier("F-011-5", lambda m: abs(m["doubling_delta_kj_mol"] - m["expected_doubling_kj_mol"]) > 1e-6,
                 "doubling pressure != R*T*ln(2) (ln-scaling neg control)"),
    cc.Falsifier("F-011-6", lambda m: m["compression_kj_mol"] >= m["floor_kj_mol"],
                 "compression >= separation floor (would dominate capture)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_011 — SC-CO2 compression to 12 MPa")
print(f"  separation floor        = {floor:.2f} kJ/mol")
print(f"  compression 1->120 bar  = {work:.2f} kJ/mol  ({work/floor:.2f}x the floor)")
print(f"  12 MPa supercritical?   = {120.0 > PC_CO2_BAR}  (Pc = {PC_CO2_BAR/10:.2f} MPa)")
print(f"  doubling to 240 bar adds = {doubling:.3f} kJ/mol (expect R*T*ln2 = {expected_doubling:.3f})")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (storage compression ~60% of floor, supercritical regime correct)")
