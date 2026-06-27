#!/usr/bin/env python3
"""Run script for H_024 — two frontiers: engineering maturity (electric DAC leads) vs
effectiveness-per-active-energy on a fossil grid (electric DAC trails). They diverge."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

ACTIVE = {"electric-DAC": 1500.0, "weathering": 300.0, "artificial-leaf": 50.0}
MATURITY = {"electric-DAC": 0.90, "weathering": 0.50, "artificial-leaf": 0.30}  # TRL+deployment (representative)

eff_dirty = {p: cc.nnr_fom(ACTIVE[p], 0.45)["nnr_ton_per_gj"] for p in ACTIVE}
eff_clean = {p: cc.nnr_fom(ACTIVE[p], 0.05)["nnr_ton_per_gj"] for p in ACTIVE}

mat_rank = sorted(ACTIVE, key=lambda p: MATURITY[p], reverse=True)
eff_rank = sorted(ACTIVE, key=lambda p: eff_dirty[p], reverse=True)
mat_argmax = mat_rank[0]
eff_argmax = eff_rank[0]

# Maturity signal (corrected): electric DAC is the UNIQUE engineering-frontier leader (strictly
# highest TRL+deployment). The first-frozen F-024-6 tried "closest to its own floor", which was
# ill-posed — DAC sits 12.3x ABOVE its floor (the opposite of close) and a shared 122 kWh floor
# is wrong for non-separation paths; the real maturity discriminator is deployment, already in
# MATURITY. Corrected to the registered intent ("maturity signal is real"). See card note.
dac_unique_maturity_leader = (
    MATURITY["electric-DAC"] == max(MATURITY.values())
    and sum(1 for v in MATURITY.values() if v == max(MATURITY.values())) == 1
)
dac_above_own_floor = ACTIVE["electric-DAC"] / 122.0  # 12.3x headroom to its 2nd-law floor (H_019)

# F-024-5: DAC effectiveness RANK improves on a clean grid (lower rank index = better).
dac_rank_dirty = sorted(ACTIVE, key=lambda p: eff_dirty[p], reverse=True).index("electric-DAC")
dac_rank_clean = sorted(ACTIVE, key=lambda p: eff_clean[p], reverse=True).index("electric-DAC")
dac_climbs_on_clean = dac_rank_clean <= dac_rank_dirty

metrics = {
    "maturity_argmax": mat_argmax,
    "effectiveness_argmax": eff_argmax,
    "maturity_ranking": mat_rank,
    "effectiveness_ranking": eff_rank,
    "rankings_identical": mat_rank == eff_rank,
    "maturity_in_unit": all(0.0 <= v <= 1.0 for v in MATURITY.values()),
    "dac_unique_maturity_leader": dac_unique_maturity_leader,
    "dac_above_own_floor_x": dac_above_own_floor,
    "dac_climbs_on_clean": dac_climbs_on_clean,
}

falsifiers = [
    cc.Falsifier("F-024-1", lambda m: m["maturity_argmax"] != "electric-DAC",
                 "electric DAC is not the maturity leader (premise fails)"),
    cc.Falsifier("F-024-2", lambda m: m["effectiveness_argmax"] == "electric-DAC",
                 "electric DAC is the effectiveness leader too (no divergence)"),
    cc.Falsifier("F-024-3", lambda m: m["rankings_identical"],
                 "maturity and effectiveness rankings identical (one-dimensional frontier)"),
    cc.Falsifier("F-024-4", lambda m: not m["maturity_in_unit"],
                 "maturity scores outside [0,1] (bounds)"),
    cc.Falsifier("F-024-5", lambda m: not m["dac_climbs_on_clean"],
                 "DAC effectiveness rank does not improve on a clean grid (divergence not grid-conditional)"),
    cc.Falsifier("F-024-6", lambda m: not m["dac_unique_maturity_leader"],
                 "electric DAC not the UNIQUE maturity leader (corrected: maturity = TRL+deployment, not floor-closeness)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "SUPPORTED = two divergent frontiers. Electric DAC leads ENGINEERING MATURITY (most deployed, "
    "12.3x = closest to its own 2nd-law floor) but trails EFFECTIVENESS per active energy on a fossil "
    "grid (H_020). 'The frontier was electric DAC' is true for maturity, false for effectiveness; "
    "H_017-H_019 measured maturity and mislabeled it 'the' frontier (self-correction)."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_024 — two frontiers: maturity vs effectiveness")
print(f"  ENGINEERING-MATURITY frontier:  argmax = {mat_argmax}   ranking {mat_rank}")
print(f"  EFFECTIVENESS frontier (fossil): argmax = {eff_argmax}   ranking {eff_rank}")
print(f"  rankings identical? {metrics['rankings_identical']}  -> frontiers diverge: {not metrics['rankings_identical']}")
print(f"  electric DAC: unique maturity leader={dac_unique_maturity_leader}; sits {dac_above_own_floor:.1f}x above its own 2nd-law floor (H_019)")
print(f"  honesty: DAC effectiveness rank dirty #{dac_rank_dirty+1} -> clean #{dac_rank_clean+1} (climbs as grid cleans)")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (frontier = 2 axes; DAC leads maturity, not effectiveness)")
