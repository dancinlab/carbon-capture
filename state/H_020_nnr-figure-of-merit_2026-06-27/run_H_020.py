#!/usr/bin/env python3
"""Run script for H_020 — NNR figure of merit: free-energy paths overwhelmingly
dominate electric DAC on a fossil grid (net CO2 per active grid energy)."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

DIRTY, CLEAN = 0.45, 0.05
PATHS = {
    "electric-DAC Gen3": 1500.0,
    "enhanced-weathering": 300.0,
    "moisture-swing (passive)": 100.0,
    "artificial-leaf": 50.0,
}

dac = cc.nnr_fom(PATHS["electric-DAC Gen3"], DIRTY)
fom = {name: cc.nnr_fom(kwh, DIRTY) for name, kwh in PATHS.items()}
adv = {name: fom[name]["nnr_ton_per_gj"] / dac["nnr_ton_per_gj"] for name in PATHS}
best_path = max((n for n in PATHS if n != "electric-DAC Gen3"), key=lambda n: adv[n])
best_adv = adv[best_path]

# F-020-5 neg control: same active energy as DAC -> same NNR.
nc_same = abs(cc.nnr_fom(1500.0, DIRTY)["nnr_ton_per_gj"] - dac["nnr_ton_per_gj"]) < 1e-12
# F-020-4 bounds.
try:
    cc.nnr_fom(0.0)
    zero_raises = False
except ValueError:
    zero_raises = True
# F-020-6 grid dependence: weathering/DAC ratio shrinks on a clean grid.
dac_clean = cc.nnr_fom(1500.0, CLEAN)["nnr_ton_per_gj"]
weath_clean = cc.nnr_fom(300.0, CLEAN)["nnr_ton_per_gj"]
ratio_clean = weath_clean / dac_clean
ratio_dirty = adv["enhanced-weathering"]
# F-020-7 old DAC futile.
old_dac_net = cc.net_capture_fraction(9e9, DIRTY)

metrics = {
    "dac_net_dirty": dac["net_fraction"],
    "dac_nnr": dac["nnr_ton_per_gj"],
    "weathering_nnr": fom["enhanced-weathering"]["nnr_ton_per_gj"],
    "leaf_nnr": fom["artificial-leaf"]["nnr_ton_per_gj"],
    "adv_weathering": adv["enhanced-weathering"],
    "adv_moisture": adv["moisture-swing (passive)"],
    "adv_leaf": adv["artificial-leaf"],
    "best_path": best_path, "best_adv": best_adv,
    "nc_same_active_same_nnr": nc_same, "zero_raises": zero_raises,
    "ratio_dirty": ratio_dirty, "ratio_clean": ratio_clean,
    "old_dac_net_dirty": old_dac_net,
}

falsifiers = [
    cc.Falsifier("F-020-1", lambda m: m["best_adv"] < 10.0,
                 "best free-energy path < 10x DAC (advantage not overwhelming)"),
    cc.Falsifier("F-020-2", lambda m: m["dac_net_dirty"] > 0.5,
                 "electric DAC dirty-grid net > 0.5 (not crippled)"),
    cc.Falsifier("F-020-3", lambda m: m["adv_weathering"] < 5.0,
                 "enhanced-weathering < 5x DAC"),
    cc.Falsifier("F-020-4", lambda m: not m["zero_raises"],
                 "nnr_fom(0) did not raise (bounds)"),
    cc.Falsifier("F-020-5", lambda m: not m["nc_same_active_same_nnr"],
                 "same active energy != same NNR (metric not self-consistent)"),
    cc.Falsifier("F-020-6", lambda m: m["ratio_clean"] >= m["ratio_dirty"],
                 "clean-grid advantage >= dirty-grid (gap not grid-dependent — honesty check)"),
    cc.Falsifier("F-020-7", lambda m: m["old_dac_net_dirty"] > 0.0,
                 "9 GJ/ton DAC net > 0 on a dirty grid (worst case not futile)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "SUPPORTED = on a fossil grid, free-energy paths overwhelmingly dominate electric DAC on "
    "net-CO2-per-active-grid-energy: enhanced weathering 13x, moisture-swing 44x, artificial leaf "
    "90x. The unified cross-family FoM is the NOVEL (methodological) contribution; the 13-90x are "
    "its decisive numbers. (Energy axis only — DAC still wins on rate/footprint, see Limits.)"
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_020 — NNR figure of merit (net CO2 per active grid GJ, fossil 0.45 kgCO2/kWh)")
for name, kwh in PATHS.items():
    r = fom[name]
    print(f"  {name:26s} active {kwh:5.0f} kWh  net {r['net_fraction']:+.2f}  "
          f"NNR {r['nnr_ton_per_gj']:6.3f} ton/GJ = {adv[name]:5.1f}x DAC")
print(f"  best non-DAC path: {best_path} = {best_adv:.0f}x electric DAC")
print(f"  honesty: weathering/DAC ratio dirty {ratio_dirty:.1f}x -> clean {ratio_clean:.1f}x (gap shrinks as grid cleans)")
print(f"  old 9 GJ/ton DAC net on dirty grid = {old_dac_net:+.2f} (futile)")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (free-energy paths 13-90x over electric DAC on a fossil grid)")
