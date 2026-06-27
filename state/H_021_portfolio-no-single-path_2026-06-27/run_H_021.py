#!/usr/bin/env python3
"""Run script for H_021 — no single removal path dominates all four axes (portfolio)."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

AXES = ["energy", "rate", "footprint", "permanence"]
PATHS = {
    "electric-DAC": {"energy": 0.20, "rate": 0.90, "footprint": 0.90, "permanence": 0.90},
    "weathering": {"energy": 0.90, "rate": 0.20, "footprint": 0.20, "permanence": 0.90},
    "artificial-leaf": {"energy": 0.95, "rate": 0.50, "footprint": 0.30, "permanence": 0.30},
}

# any path that dominates EVERY other path?
single_winner = None
for a in PATHS:
    if all(cc.dominates(PATHS[a], PATHS[b]) for b in PATHS if b != a):
        single_winner = a
        break

argmax = {ax: max(PATHS, key=lambda p: PATHS[p][ax]) for ax in AXES}
dac_best_rate = argmax["rate"] == "electric-DAC" and sum(1 for p in PATHS if PATHS[p]["rate"] == PATHS["electric-DAC"]["rate"]) == 1
dac_best_foot = argmax["footprint"] == "electric-DAC"
energy_best = argmax["energy"]
energy_is_free = energy_best in ("weathering", "artificial-leaf")
worst_axis = {p: min(AXES, key=lambda ax: PATHS[p][ax]) for p in PATHS}
all_have_worst = all(any(PATHS[p][ax] == min(PATHS[q][ax] for q in PATHS) for ax in AXES) for p in PATHS)

# F-021-4/5 controls
self_dom = cc.dominates(PATHS["electric-DAC"], PATHS["electric-DAC"])
better = {ax: 0.99 for ax in AXES}
control_dom = cc.dominates(better, {ax: 0.10 for ax in AXES})

metrics = {
    "single_winner": single_winner, "argmax": argmax,
    "dac_unique_best_rate": dac_best_rate, "dac_best_footprint": dac_best_foot,
    "energy_best_path": energy_best, "energy_best_is_free": energy_is_free,
    "all_paths_worst_somewhere": all_have_worst,
    "self_dominates": self_dom, "control_dominates": control_dom,
}

falsifiers = [
    cc.Falsifier("F-021-1", lambda m: m["single_winner"] is not None,
                 "a single path dominates all others (portfolio false)"),
    cc.Falsifier("F-021-2", lambda m: not m["dac_unique_best_rate"],
                 "electric DAC not the unique best on rate"),
    cc.Falsifier("F-021-3", lambda m: not m["energy_best_is_free"],
                 "no free-energy path is best on energy"),
    cc.Falsifier("F-021-4", lambda m: m["self_dominates"],
                 "a path strictly dominates itself (bounds)"),
    cc.Falsifier("F-021-5", lambda m: not m["control_dominates"],
                 "domination test fails to detect a real all-axes-better card (neg control)"),
    cc.Falsifier("F-021-6", lambda m: any(all(m["argmax"][ax] == p for ax in AXES) for p in PATHS),
                 "some path is best on ALL four axes (true single winner)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "SUPPORTED = no path dominates all four axes (energy/rate/footprint/permanence) -> "
    "removal is a PORTFOLIO, not a single winner; 'is electric DAC THE path?' is mis-framed."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_021 — no single path dominates (portfolio)")
print(f"  single dominating path? {single_winner or 'NONE'}")
for ax in AXES:
    print(f"  best on {ax:11s}: {argmax[ax]}")
for p in PATHS:
    print(f"  {p:16s} worst axis: {worst_axis[p]}")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (removal is a portfolio; 'is DAC THE path' is the wrong question)")
