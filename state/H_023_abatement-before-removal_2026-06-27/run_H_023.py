#!/usr/bin/env python3
"""Run script for H_023 — abatement before removal (marginal-electron crossover)."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

COAL, GAS, CLEAN = 0.9, 0.4, 0.0
g_gen3 = cc.abatement_crossover_intensity(1500.0)
g_nextgen = cc.abatement_crossover_intensity(750.0)

# at a grid margin g: displacement avoids g; DAC removes g* (=1000/E). abatement wins if g > g*.
abate_wins_coal = COAL > g_gen3
dac_wins_gas = GAS < g_gen3
clean_grid_dac_only = CLEAN < g_gen3   # displacement avoids 0 -> DAC always the lever
monotone = g_nextgen > g_gen3

try:
    cc.abatement_crossover_intensity(0.0)
    zero_raises = False
except ValueError:
    zero_raises = True

metrics = {
    "crossover_gen3": g_gen3,
    "crossover_nextgen": g_nextgen,
    "abatement_wins_at_coal": abate_wins_coal,
    "dac_wins_at_gas": dac_wins_gas,
    "clean_grid_dac_only": clean_grid_dac_only,
    "crossover_rises_with_efficiency": monotone,
    "zero_raises": zero_raises,
}

falsifiers = [
    cc.Falsifier("F-023-1", lambda m: not (0.65 <= m["crossover_gen3"] <= 0.68),
                 "crossover g* not in [0.65,0.68] kgCO2/kWh"),
    cc.Falsifier("F-023-2", lambda m: not m["abatement_wins_at_coal"],
                 "displacement does not beat DAC at coal margin (0.9)"),
    cc.Falsifier("F-023-3", lambda m: not m["dac_wins_at_gas"],
                 "DAC does not beat displacement at gas margin (0.4)"),
    cc.Falsifier("F-023-4", lambda m: not m["zero_raises"],
                 "zero-energy DAC did not raise (bounds)"),
    cc.Falsifier("F-023-5", lambda m: not m["crossover_rises_with_efficiency"],
                 "g* does not rise as DAC energy falls (efficiency doesn't widen DAC window)"),
    cc.Falsifier("F-023-6", lambda m: not m["clean_grid_dac_only"],
                 "on a zero-carbon grid DAC is not the only lever (neg control)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "SUPPORTED = while the marginal grid plant emits > 0.667 kgCO2/kWh (coal), a clean kWh AVOIDS "
    "more CO2 displacing fossil than it REMOVES via electric DAC -> abatement before removal; DAC's "
    "value rises as the grid cleans (g* widens with efficiency)."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_023 — abatement before removal (marginal-electron test)")
print(f"  crossover g* (Gen3 1500 kWh/ton) = {g_gen3:.3f} kgCO2/kWh")
print(f"  crossover g* (next-gen 750 kWh)  = {g_nextgen:.3f} kgCO2/kWh (efficiency widens DAC's window)")
print(f"  coal margin 0.9 > g*? {abate_wins_coal} -> displace fossil first")
print(f"  gas margin 0.4 < g*?  {dac_wins_gas} -> DAC removes more")
print(f"  clean grid 0.0 < g*?  {clean_grid_dac_only} -> DAC is the only lever once grid is clean")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (abatement before removal while the marginal grid > 0.67 kgCO2/kWh)")
