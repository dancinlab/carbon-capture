#!/usr/bin/env python3
"""Run script for H_001 — DAC thermodynamic separation floor.

Deterministic, stdlib-only. Imports the shared harness from repo-root tool/.
Writes result.json next to this script and prints a verbatim verdict.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

T = 298.15

# --- measured quantities (kJ/mol) ---------------------------------------------
floor_air = cc.min_separation_work(420e-6, T) / 1000.0
floor_flue = cc.min_separation_work(0.12, T) / 1000.0
floor_pure = cc.min_separation_work(0.99, T) / 1000.0

# P2: monotonic rise as x falls — sweep x from concentrated to dilute.
x_sweep = [0.5, 0.12, 0.04, 0.004, 420e-6]
w_sweep = [cc.min_separation_work(x, T) / 1000.0 for x in x_sweep]
strictly_increasing = all(w_sweep[i] < w_sweep[i + 1] for i in range(len(w_sweep) - 1))

metrics = {
    "floor_air_kj_mol": floor_air,
    "floor_flue_kj_mol": floor_flue,
    "floor_pure_kj_mol": floor_pure,
    "x_sweep": x_sweep,
    "w_sweep_kj_mol": w_sweep,
    "strictly_increasing": strictly_increasing,
}

falsifiers = [
    cc.Falsifier("F-001-1", lambda m: m["floor_air_kj_mol"] > 20.0,
                 "floor > 20 kJ/mol (above J2-tau target)"),
    cc.Falsifier("F-001-2", lambda m: m["floor_air_kj_mol"] < 19.0,
                 "floor < 19 kJ/mol (over-optimistic)"),
    cc.Falsifier("F-001-3", lambda m: not m["strictly_increasing"],
                 "W_min not strictly increasing as x falls"),
    cc.Falsifier("F-001-4", lambda m: m["floor_flue_kj_mol"] > 6.0,
                 "12% flue floor > 6 kJ/mol (flue not easier)"),
    cc.Falsifier("F-001-5", lambda m: m["floor_pure_kj_mol"] > 0.1,
                 "near-pure (x=0.99) floor > 0.1 kJ/mol"),
    cc.Falsifier("F-001-6", lambda m: m["floor_air_kj_mol"] <= m["floor_flue_kj_mol"],
                 "dilute air does not cost more than concentrated flue (mis-signed)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_001 — DAC separation floor")
print(f"  floor(420 ppm, 298 K) = {floor_air:.3f} kJ/mol   (target J2-tau = 20)")
print(f"  floor(12% flue)       = {floor_flue:.3f} kJ/mol")
print(f"  floor(x=0.99)         = {floor_pure:.4f} kJ/mol")
print(f"  W_min strictly rising as x falls: {strictly_increasing}")
print(f"  sweep {[round(w,3) for w in w_sweep]} kJ/mol over x={x_sweep}")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}")
