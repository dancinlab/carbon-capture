#!/usr/bin/env python3
"""Run script for H_008 — CO2->carbon reduction energy floor & value-at-scale.

Skeptical framing: all falsifiers PASS => "conversion is a free value bonus at scale"
is refuted (energy-dominant + market-saturating).
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

reduction_per_ton_c = cc.carbon_reduction_energy_floor()           # J / ton C
reduction_per_ton_c_gj = reduction_per_ton_c / 1e9
# per ton CO2 captured you recover M_C/M_CO2 tons of carbon:
c_per_co2 = cc.M_C / cc.M_CO2
reduction_per_ton_co2_gj = reduction_per_ton_c_gj * c_per_co2
capture_floor_gj = cc.min_separation_work(420e-6) / cc.M_CO2 * 1e6 / 1e9   # GJ/ton-CO2 (H_001)
ratio_to_capture_floor = reduction_per_ton_co2_gj / capture_floor_gj

price = 1e6        # $/ton graphene
scale = 1e6        # ton/yr (1 Mt/yr)
market_ref = 1e9   # $/yr current graphene market (representative)
revenue = price * scale
market_ratio = revenue / market_ref

# F-008-5 negative control: linear scaling of the enthalpy floor.
nc_linear = abs(cc.carbon_reduction_energy_floor(2 * cc.DH_F_CO2)
                - 2 * cc.carbon_reduction_energy_floor()) < 1.0
# F-008-4 bounds: dh_f=0 must raise.
try:
    cc.carbon_reduction_energy_floor(0.0)
    zero_raises = False
except ValueError:
    zero_raises = True

metrics = {
    "reduction_floor_gj_per_ton_c": reduction_per_ton_c_gj,
    "reduction_floor_gj_per_ton_co2": reduction_per_ton_co2_gj,
    "capture_floor_gj_per_ton_co2": capture_floor_gj,
    "ratio_reduction_to_capture_floor": ratio_to_capture_floor,
    "revenue_usd_yr": revenue,
    "market_ratio": market_ratio,
    "nc_linear_scaling_ok": nc_linear,
    "zero_dhf_raises": zero_raises,
}

falsifiers = [
    cc.Falsifier("F-008-1", lambda m: not (30.0 <= m["reduction_floor_gj_per_ton_c"] <= 35.0),
                 "reduction floor not in [30,35] GJ/ton-C"),
    cc.Falsifier("F-008-2", lambda m: m["ratio_reduction_to_capture_floor"] < 15.0,
                 "reduction < 15x the capture floor (not energy-dominant)"),
    cc.Falsifier("F-008-3", lambda m: m["reduction_floor_gj_per_ton_co2"] < 5.0,
                 "reduction < 5 GJ/ton-CO2 (negligible vs capture)"),
    cc.Falsifier("F-008-4", lambda m: not m["zero_dhf_raises"],
                 "dh_f=0 did not raise (no free reduction)"),
    cc.Falsifier("F-008-5", lambda m: not m["nc_linear_scaling_ok"],
                 "reduction floor not linear in enthalpy (neg control)"),
    cc.Falsifier("F-008-6", lambda m: m["market_ratio"] < 100.0,
                 "Mt-scale revenue fits the market (=> $1M/ton sustainable)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "SUPPORTED here = conversion is energy-dominant (~20x the capture floor) and $1M/ton "
    "cannot survive Mt-scale (~1000x the current market) — the 'free value bonus' reading is refuted."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_008 — transmutation energy floor & value-at-scale")
print(f"  CO2->C reduction floor   = {reduction_per_ton_c_gj:.2f} GJ/ton-C = {reduction_per_ton_co2_gj:.2f} GJ/ton-CO2")
print(f"  capture thermo floor     = {capture_floor_gj:.3f} GJ/ton-CO2  (H_001)")
print(f"  reduction / capture floor = {ratio_to_capture_floor:.1f}x")
print(f"  $1M/ton x 1 Mt/yr        = ${revenue/1e9:.0f}B/yr  = {market_ratio:.0f}x the ~$1B/yr graphene market")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (conversion energy-dominant; $1M/ton not scale-sustainable)")
