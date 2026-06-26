#!/usr/bin/env python3
"""Run script for H_004 — capture-cost floor & learning curve (expected PARTIAL).

Verdict logic: SUPPORTED needs (a) all falsifiers PASS AND (b) the $24/ton endpoint
clears a credible reference floor. The gap & learning-curve claims pass, but the
endpoint sits below the aspiration floor, so the card resolves to PARTIAL by design.
"""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

baseline = 600.0
target = 24.0
doe_target = 100.0
aspiration = 50.0
LR = 0.18

ratio = cc.cost_ratio(baseline, target)              # 25x
gap_to_doe = cc.cost_ratio(baseline, doe_target)     # 6x
# Wright's law: cost factor after d doublings = (1-LR)^d. Solve (1-LR)^d = 1/ratio.
doublings_for_25x = math.log(ratio) / (-math.log(1.0 - LR))
neg_control = cc.cost_ratio(baseline, baseline)      # must be 1.0
endpoint_clears_floor = target >= aspiration          # 24 >= 50 -> False

metrics = {
    "cost_ratio_600_24": ratio,
    "gap_to_doe_600_100": gap_to_doe,
    "doublings_for_25x_at_LR18": doublings_for_25x,
    "neg_control_ratio": neg_control,
    "endpoint_clears_aspiration_floor": endpoint_clears_floor,
}

falsifiers = [
    cc.Falsifier("F-004-1", lambda m: abs(m["cost_ratio_600_24"] - 25.0) > 1e-9,
                 "headline 25x ratio arithmetic wrong"),
    cc.Falsifier("F-004-2", lambda m: m["doublings_for_25x_at_LR18"] > 20.0,
                 "learning-curve route needs > 20 doublings (implausible)"),
    cc.Falsifier("F-004-3", lambda m: m["gap_to_doe_600_100"] < 3.0,
                 "gap to DOE target < 3x (too small to matter)"),
    cc.Falsifier("F-004-4", lambda m: target >= aspiration,
                 "endpoint >= aspiration floor (would mean endpoint credible)"),
    cc.Falsifier("F-004-5", lambda m: m["neg_control_ratio"] != 1.0,
                 "baseline==target does not give ratio 1.0 (neg control)"),
    cc.Falsifier("F-004-6", lambda m: m["doublings_for_25x_at_LR18"] <= 0.0,
                 "non-positive doublings (math bug guard)"),
]

ledger = cc.evaluate(metrics, falsifiers)
if ledger["all_pass"] and endpoint_clears_floor:
    verdict = "SUPPORTED"
elif ledger["all_pass"]:
    verdict = "PARTIAL"
else:
    verdict = "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "Gap (25x) and learning-curve route are credible; the $24/ton endpoint is below "
    "the $50 aspiration and $100 DOE reference floors -> PARTIAL (endpoint unverified-optimistic)."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_004 — capture cost floor & learning curve")
print(f"  cost_ratio(600 -> 24)        = {ratio:.1f}x")
print(f"  doublings for 25x at LR=18%   = {doublings_for_25x:.1f}")
print(f"  gap to DOE $100/ton           = {gap_to_doe:.1f}x")
print(f"  endpoint $24 clears $50 floor : {endpoint_clears_floor}")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (gap real & learnable; $24/ton endpoint unverified-optimistic)")
