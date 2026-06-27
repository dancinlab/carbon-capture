#!/usr/bin/env python3
"""Run script for H_012 — Sabatier-optimal CO2 binding energy at DAC partial pressure."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

P_DAC = 4.2e-4   # bar (420 ppm)
E_sweep = [20, 30, 40, 50, 60, 70]
theta = {E: cc.langmuir_coverage(E, P_DAC) for E in E_sweep}
monotone = all(theta[E_sweep[i]] < theta[E_sweep[i + 1]] for i in range(len(E_sweep) - 1))
in_unit = all(0.0 <= t < 1.0 for t in theta.values())
theta_30_highP = cc.langmuir_coverage(30, 1.0)   # weak sorbent at high partial pressure

metrics = {
    "theta": {str(E): theta[E] for E in E_sweep},
    "theta_30_dac": theta[30],
    "theta_50_dac": theta[50],
    "theta_60_dac": theta[60],
    "monotone_increasing": monotone,
    "all_in_unit_interval": in_unit,
    "theta_30_highP": theta_30_highP,
}

falsifiers = [
    cc.Falsifier("F-012-1", lambda m: m["theta_30_dac"] >= 0.01,
                 "weak binding (30) already gives uptake at DAC (no low-end wall)"),
    cc.Falsifier("F-012-2", lambda m: m["theta_60_dac"] <= 0.5,
                 "strong binding (60) fails to fill (model broken)"),
    cc.Falsifier("F-012-3", lambda m: not m["monotone_increasing"],
                 "theta not monotonically increasing in E_ads"),
    cc.Falsifier("F-012-4", lambda m: not m["all_in_unit_interval"],
                 "some theta outside [0,1) (bounds)"),
    cc.Falsifier("F-012-5", lambda m: not (m["theta_30_highP"] > 10 * m["theta_30_dac"]),
                 "weak sorbent not rescued by high pressure (mechanism = dilution unconfirmed)"),
    cc.Falsifier("F-012-6", lambda m: not (0.05 <= m["theta_50_dac"] <= 0.95),
                 "theta(50) outside tunable window (no optimum)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "SUPPORTED = a Sabatier optimum exists: weak binding gives ~0 uptake at 400 ppm, strong "
    "binding fills but owes its E_ads back at regeneration; the usable window is ~45-55 kJ/mol."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_012 — Sabatier-optimal CO2 binding energy at 400 ppm")
for E in E_sweep:
    print(f"  E_ads = {E:2d} kJ/mol -> theta = {theta[E]:.4f}")
print(f"  monotone increasing: {monotone}   all theta in [0,1): {in_unit}")
print(f"  weak sorbent rescue by pressure: theta(30,DAC)={theta[30]:.4g} -> theta(30,1bar)={theta_30_highP:.4f}")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (binding-energy optimum ~45-55 kJ/mol: coverage vs regeneration)")
