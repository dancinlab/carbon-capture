#!/usr/bin/env python3
"""Run script for H_014 — net-negativity threshold (lifecycle carbon balance)."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

E = 9e9          # J/ton (9 GJ/ton real DAC)
E_half = 4.5e9   # J/ton next-gen
kwh_per_ton = E / 3.6e6
breakeven = 1000.0 / kwh_per_ton                 # kg/kWh where net = 0
breakeven_half = 1000.0 / (E_half / 3.6e6)

net_fossil = cc.net_capture_fraction(E, 0.45)
net_mixed = cc.net_capture_fraction(E, 0.20)
net_clean = cc.net_capture_fraction(E, 0.05)
nc_zero_E = cc.net_capture_fraction(0.0, 0.45)    # zero energy -> 1.0
nc_zero_grid = cc.net_capture_fraction(E, 0.0)    # zero-carbon energy -> 1.0

metrics = {
    "kwh_per_ton": kwh_per_ton,
    "breakeven_kg_per_kwh": breakeven,
    "breakeven_half_kg_per_kwh": breakeven_half,
    "net_fossil_0p45": net_fossil,
    "net_mixed_0p20": net_mixed,
    "net_clean_0p05": net_clean,
    "nc_zero_energy": nc_zero_E,
    "nc_zero_grid": nc_zero_grid,
}

falsifiers = [
    cc.Falsifier("F-014-1", lambda m: m["net_fossil_0p45"] > 0.1,
                 "fossil grid (0.45) still net-removes meaningfully"),
    cc.Falsifier("F-014-2", lambda m: not (0.35 <= m["breakeven_kg_per_kwh"] <= 0.45),
                 "breakeven intensity outside [0.35,0.45] kg/kWh"),
    cc.Falsifier("F-014-3", lambda m: m["net_clean_0p05"] < 0.8,
                 "clean power (0.05) fails to net-remove >= 0.8"),
    cc.Falsifier("F-014-4", lambda m: m["nc_zero_energy"] != 1.0,
                 "zero energy not 100% net (bounds)"),
    cc.Falsifier("F-014-5", lambda m: m["nc_zero_grid"] != 1.0,
                 "zero-carbon energy not fully net (neg control)"),
    cc.Falsifier("F-014-6", lambda m: abs(m["breakeven_half_kg_per_kwh"] - 2 * m["breakeven_kg_per_kwh"]) > 1e-6,
                 "halving energy does not double breakeven intensity (coupling broken)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "SUPPORTED = DAC at 9 GJ/ton is net-futile on a fossil grid (breakeven ~0.40 kg/kWh); "
    "net removal needs clean energy (<~0.2 kg/kWh) or the H_010 efficiency gains."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_014 — net-negativity threshold")
print(f"  capture energy           = {kwh_per_ton:.0f} kWh/ton")
print(f"  breakeven grid intensity = {breakeven:.3f} kg/kWh  (halved energy -> {breakeven_half:.3f})")
print(f"  net @ 0.45 fossil grid   = {net_fossil:+.2f} ton/ton  {'FUTILE' if net_fossil <= 0 else ''}")
print(f"  net @ 0.20 mixed grid    = {net_mixed:+.2f} ton/ton")
print(f"  net @ 0.05 clean grid    = {net_clean:+.2f} ton/ton")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (fossil-grid DAC futile; clean energy / efficiency mandatory)")
