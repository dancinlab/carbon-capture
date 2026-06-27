#!/usr/bin/env python3
"""Run script for H_013 — plant air-throughput wall + scale-up arithmetic."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

air_per_ton = cc.air_volume_per_ton_co2(420e-6, capture_efficiency=1.0)
air_per_ton_eff50 = cc.air_volume_per_ton_co2(420e-6, capture_efficiency=0.5)
annual_air = air_per_ton * 1e6
scale_ratio = cc.annual_capacity_ratio(1e6, 4e3)
air_flue = cc.air_volume_per_ton_co2(0.12)
try:
    cc.air_volume_per_ton_co2(1.0)
    pure_raises = False
except ValueError:
    pure_raises = True

metrics = {
    "air_per_ton_m3": air_per_ton,
    "air_per_ton_eff50_m3": air_per_ton_eff50,
    "annual_air_m3_yr": annual_air,
    "scale_ratio_climeworks": scale_ratio,
    "air_per_ton_flue_m3": air_flue,
    "pure_co2_raises": pure_raises,
}

falsifiers = [
    cc.Falsifier("F-013-1", lambda m: not (1.0e6 <= m["air_per_ton_m3"] <= 1.6e6),
                 "air per ton outside [1.0e6,1.6e6] m3 (mass balance off)"),
    cc.Falsifier("F-013-2", lambda m: m["annual_air_m3_yr"] < 1e12,
                 "annual air at 1 Mt/yr < 1e12 m3/yr"),
    cc.Falsifier("F-013-3", lambda m: abs(m["scale_ratio_climeworks"] - 250.0) > 1e-9,
                 "1 Mt/yr vs 4 kt/yr scale ratio != 250x"),
    cc.Falsifier("F-013-4", lambda m: not m["pure_co2_raises"],
                 "pure CO2 (x=1) did not raise (bounds)"),
    cc.Falsifier("F-013-5", lambda m: abs(m["air_per_ton_eff50_m3"] - 2 * m["air_per_ton_m3"]) > 1.0,
                 "eff=0.5 not 2x the eff=1 air volume (1/efficiency neg control)"),
    cc.Falsifier("F-013-6", lambda m: m["air_per_ton_flue_m3"] >= m["air_per_ton_m3"],
                 "flue gas needs >= air than 420 ppm (dilution advantage inverted)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "SUPPORTED = scale-up arithmetic sound (250x) and the binding duty is air handling: "
    "~1.3e6 m3 air/ton -> ~1.3e12 m3/yr at 1 Mt/yr (a throughput/fan-power wall, not chemistry)."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_013 — plant air-throughput wall")
print(f"  air per ton CO2 (420 ppm, eff=1) = {air_per_ton:.3e} m3")
print(f"  air at 1 Mt/yr                   = {annual_air:.3e} m3/yr")
print(f"  scale-up 1 Mt/yr vs 4 kt/yr      = {scale_ratio:.0f}x Climeworks")
print(f"  air per ton at 12% flue          = {air_flue:.3e} m3  (vs {air_per_ton:.2e} for air)")
print(f"  eff=0.5 doubles air              = {air_per_ton_eff50:.3e} m3")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (250x scale arithmetic sound; air-handling is the binding duty)")
