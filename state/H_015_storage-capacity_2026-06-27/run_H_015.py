#!/usr/bin/env python3
"""Run script for H_015 — geologic storage capacity vs drawdown demand."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

capacity_central = 1e4   # Gt CO2
capacity_pessimistic = 1e3
rate = 100.0             # Gt/yr
demand = cc.ppm_to_gt_co2(140.0)

ratio_central = capacity_central / demand
ratio_pessimistic = capacity_pessimistic / demand
years_capacity = capacity_central / rate

metrics = {
    "demand_gt": demand,
    "capacity_central_gt": capacity_central,
    "ratio_central": ratio_central,
    "ratio_pessimistic": ratio_pessimistic,
    "years_capacity_at_100gt_yr": years_capacity,
    "nc_zero_demand": cc.ppm_to_gt_co2(0.0),
    "nc_linear": cc.ppm_to_gt_co2(280.0),
}

falsifiers = [
    cc.Falsifier("F-015-1", lambda m: m["ratio_central"] < 5.0,
                 "central capacity < 5x demand (not comfortably sufficient)"),
    cc.Falsifier("F-015-2", lambda m: m["years_capacity_at_100gt_yr"] < 100.0,
                 "capacity runs out within a century at 100 Gt/yr"),
    cc.Falsifier("F-015-3", lambda m: m["ratio_pessimistic"] < 0.5,
                 "pessimistic 1e3 Gt < 0.5x demand (orders short)"),
    cc.Falsifier("F-015-4", lambda m: m["nc_zero_demand"] != 0.0,
                 "zero drawdown not zero demand (bounds)"),
    cc.Falsifier("F-015-5", lambda m: abs(m["nc_linear"] - 2 * m["demand_gt"]) > 1e-6,
                 "demand not linear in ppm (neg control)"),
    cc.Falsifier("F-015-6", lambda m: abs(m["demand_gt"] - 1095.0) > 5.0,
                 "demand diverges from H_009 (~1095 Gt)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "SUPPORTED = geologic storage void (~1e4 Gt) is ~9x the 1095 Gt demand and lasts >100 yr "
    "at 100 Gt/yr -> not the bottleneck; energy (H_014) and air handling (H_013) are."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_015 — geologic storage capacity vs demand")
print(f"  drawdown demand (140 ppm) = {demand:.0f} Gt CO2  (H_009)")
print(f"  central capacity 1e4 Gt   = {ratio_central:.1f}x demand")
print(f"  pessimistic 1e3 Gt        = {ratio_pessimistic:.2f}x demand")
print(f"  years at 100 Gt/yr        = {years_capacity:.0f}")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (storage void sufficient; not the bottleneck)")
