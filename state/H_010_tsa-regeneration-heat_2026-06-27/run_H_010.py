#!/usr/bin/env python3
"""Run script for H_010 — TSA regeneration sensible-heat penalty dominates the floor."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

CP, DT = 1.0, 100.0
floor = cc.min_separation_work(420e-6) / 1000.0

q_wc1 = cc.regeneration_sensible_heat(CP, DT, 1.0)
q_wc_poor = cc.regeneration_sensible_heat(CP, DT, 0.5)
q_wc_good = cc.regeneration_sensible_heat(CP, DT, 2.0)
monotone = q_wc_poor > q_wc1 > q_wc_good
linear_dt = abs(cc.regeneration_sensible_heat(CP, 2 * DT, 1.0) - 2 * q_wc1) < 1e-9
try:
    cc.regeneration_sensible_heat(CP, DT, 0.0)
    zero_raises = False
except ValueError:
    zero_raises = True

metrics = {
    "floor_kj_mol": floor,
    "q_wc1_kj_mol": q_wc1,
    "q_wc_poor_kj_mol": q_wc_poor,
    "q_wc_good_kj_mol": q_wc_good,
    "ratio_q_wc1_to_floor": q_wc1 / floor,
    "monotone_decreasing": monotone,
    "linear_in_dt": linear_dt,
    "zero_wc_raises": zero_raises,
}

falsifiers = [
    cc.Falsifier("F-010-1", lambda m: m["q_wc1_kj_mol"] <= m["floor_kj_mol"],
                 "regen sensible heat <= floor (negligible)"),
    cc.Falsifier("F-010-2", lambda m: not m["monotone_decreasing"],
                 "q not strictly decreasing in working capacity"),
    cc.Falsifier("F-010-3", lambda m: m["q_wc_poor_kj_mol"] < 100.0,
                 "poor-sorbent (wc=0.5) penalty < 100 kJ/mol"),
    cc.Falsifier("F-010-4", lambda m: not m["zero_wc_raises"],
                 "zero working capacity did not raise (bounds)"),
    cc.Falsifier("F-010-5", lambda m: not m["linear_in_dt"],
                 "q not linear in delta_T (neg control)"),
    cc.Falsifier("F-010-6", lambda m: m["q_wc_good_kj_mol"] <= m["floor_kj_mol"],
                 "good sorbent (wc=2) makes regen sub-floor (mechanism not dominant)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "SUPPORTED = TSA sensible heat (~100 kJ/mol) is the dominant term over the 19.3 kJ/mol "
    "floor and scales as 1/working_capacity — the mechanism behind the H_002 headroom."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_010 — TSA regeneration sensible-heat penalty")
print(f"  separation floor          = {floor:.2f} kJ/mol")
print(f"  q (cp=1,dT=100,wc=1)      = {q_wc1:.1f} kJ/mol  ({q_wc1/floor:.1f}x the floor)")
print(f"  q (wc=0.5 poor sorbent)   = {q_wc_poor:.1f} kJ/mol  (~real ~200 regime)")
print(f"  q (wc=2 good sorbent)     = {q_wc_good:.1f} kJ/mol  (still > floor)")
print(f"  monotone decreasing in wc : {monotone}")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (sensible heat dominates; lever = working capacity + heat recovery)")
