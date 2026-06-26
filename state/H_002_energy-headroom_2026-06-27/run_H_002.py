#!/usr/bin/env python3
"""Run script for H_002 — energy headroom above the separation floor."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

floor = cc.min_separation_work(420e-6, 298.15) / 1000.0  # ~19.275 kJ/mol (H_001 anchor)

E_spec = 200.0
E_climeworks = 8.8e9 / (1e6 / cc.M_CO2) / 1000.0  # 8.8 GJ/ton -> kJ/mol
E_optimistic = 150.0

h_spec = cc.energy_headroom(E_spec, floor)
h_climeworks = cc.energy_headroom(E_climeworks, floor)
h_optimistic = cc.energy_headroom(E_optimistic, floor)
h_at_floor = cc.energy_headroom(floor, floor)

metrics = {
    "floor_kj_mol": floor,
    "E_climeworks_kj_mol": E_climeworks,
    "headroom_spec_200": h_spec,
    "headroom_climeworks": h_climeworks,
    "headroom_optimistic_150": h_optimistic,
    "headroom_at_floor": h_at_floor,
}

falsifiers = [
    cc.Falsifier("F-002-1", lambda m: not (9.0 <= m["headroom_spec_200"] <= 12.0),
                 "spec-point headroom not in [9,12] (not ~10x)"),
    cc.Falsifier("F-002-2", lambda m: m["headroom_climeworks"] > 30.0,
                 "Climeworks headroom > 30x"),
    cc.Falsifier("F-002-3", lambda m: m["headroom_optimistic_150"] < 3.0,
                 "optimistic headroom < 3x (thesis weak)"),
    cc.Falsifier("F-002-4", lambda m: min(m["headroom_spec_200"], m["headroom_climeworks"],
                                          m["headroom_optimistic_150"]) < 1.0,
                 "any headroom < 1 (below reversible floor — impossible)"),
    cc.Falsifier("F-002-5", lambda m: abs(m["headroom_at_floor"] - 1.0) > 1e-9,
                 "headroom at the floor not exactly 1.0 (self-consistency)"),
    cc.Falsifier("F-002-6", lambda m: abs(m["floor_kj_mol"] - 19.275) > 0.05,
                 "floor diverges from H_001 (re-fitting guard)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_002 — energy headroom above the floor")
print(f"  floor                 = {floor:.3f} kJ/mol")
print(f"  headroom(200 spec)    = {h_spec:.2f}x   (target sigma-phi = 10)")
print(f"  headroom(8.8 GJ/ton)  = {h_climeworks:.2f}x   (E={E_climeworks:.1f} kJ/mol)")
print(f"  headroom(150 next-gen)= {h_optimistic:.2f}x")
print(f"  headroom(at floor)    = {h_at_floor:.4f}x")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}")
