#!/usr/bin/env python3
"""Run script for H_009 — planetary-scale removal: mass coherent but energy/ocean gated.

Verdict logic: SUPPORTED needs mass coherent AND no wall (energy feasible AND ocean
negligible). The mass arithmetic holds but both walls fire, so it resolves to PARTIAL.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

delta_ppm = 140.0
years = 12.0
stated_rate = 100.0      # Gt/yr
E_dac = 9e9              # J/ton (9 GJ/ton real DAC)
global_primary_ej = 600.0
ocean_factor = 2.0

gross_gt = cc.ppm_to_gt_co2(delta_ppm)
gross_rate = gross_gt / years
# energy for 100 Gt/yr (1 ton = 1e6 g):
energy_real_ej = stated_rate * 1e9 * E_dac / 1e18
floor_j_per_ton = cc.min_separation_work(420e-6) / cc.M_CO2 * 1e6   # J/ton-CO2 at floor
energy_floor_ej = stated_rate * 1e9 * floor_j_per_ton / 1e18
net_rate_ocean = gross_rate * ocean_factor

nc_linear = abs(cc.ppm_to_gt_co2(280) - 2 * cc.ppm_to_gt_co2(140)) < 1e-6
zero_ppm = cc.ppm_to_gt_co2(0.0)

metrics = {
    "gross_gt_co2": gross_gt,
    "gross_rate_gt_yr": gross_rate,
    "energy_real_ej_yr": energy_real_ej,
    "energy_floor_ej_yr": energy_floor_ej,
    "global_primary_ej_yr": global_primary_ej,
    "net_rate_with_ocean_gt_yr": net_rate_ocean,
    "nc_linear_ok": nc_linear,
    "zero_ppm_gt": zero_ppm,
}

falsifiers = [
    cc.Falsifier("F-009-1", lambda m: not (1000.0 <= m["gross_gt_co2"] <= 1200.0),
                 "140 ppm mass not in [1000,1200] Gt (conversion off)"),
    cc.Falsifier("F-009-2", lambda m: not (80.0 <= m["gross_rate_gt_yr"] <= 100.0),
                 "gross rate not in [80,100] Gt/yr (not mass-coherent)"),
    cc.Falsifier("F-009-3", lambda m: m["energy_real_ej_yr"] < m["global_primary_ej_yr"],
                 "100 Gt/yr at 9 GJ/ton fits within global primary energy (no energy wall)"),
    cc.Falsifier("F-009-4", lambda m: m["zero_ppm_gt"] != 0.0,
                 "zero drawdown is not zero mass (bounds)"),
    cc.Falsifier("F-009-5", lambda m: not m["nc_linear_ok"],
                 "ppm_to_gt_co2 not linear (neg control)"),
    cc.Falsifier("F-009-6", lambda m: m["energy_floor_ej_yr"] < 10.0,
                 "even at the floor, 100 Gt/yr energy < 10 EJ/yr (scale trivial)"),
]

ledger = cc.evaluate(metrics, falsifiers)
# mass coherent (F1,F2,F4,F5 pass) is necessary; energy/ocean walls (F3,F6) mark PARTIAL.
mass_ok = all(r["status"] == "PASS" for r in ledger["falsifiers"] if r["name"] in ("F-009-1", "F-009-2", "F-009-4", "F-009-5"))
energy_wall = metrics["energy_real_ej_yr"] >= global_primary_ej
ocean_wall = net_rate_ocean >= 1.5 * stated_rate
if ledger["all_pass"] and not energy_wall and not ocean_wall:
    verdict = "SUPPORTED"
elif mass_ok and (energy_wall or ocean_wall):
    verdict = "PARTIAL"
else:
    verdict = "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "Mass balance coherent (~91 Gt/yr matches ~100 Gt/yr claim); but real-DAC energy "
    "(~900 EJ/yr) exceeds global primary energy and ocean re-equilibration needs ~2x more "
    "-> PARTIAL, gated on the H_001/H_002 efficiency thesis."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_009 — planetary-scale removal: mass vs energy")
print(f"  140 ppm drawdown     = {gross_gt:.0f} Gt CO2  -> /{years:.0f}yr = {gross_rate:.1f} Gt/yr (claim ~{stated_rate:.0f})")
print(f"  energy @ 9 GJ/ton    = {energy_real_ej:.0f} EJ/yr   (global primary ~{global_primary_ej:.0f} EJ/yr)")
print(f"  energy @ thermo floor = {energy_floor_ej:.1f} EJ/yr  (~{100*energy_floor_ej/global_primary_ej:.0f}% of global)")
print(f"  net rate w/ ocean 2x  = {net_rate_ocean:.0f} Gt/yr  (vs stated {stated_rate:.0f})")
print(f"  energy wall: {energy_wall}   ocean wall: {ocean_wall}")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (mass coherent; energy + ocean walls gate the literal target)")
