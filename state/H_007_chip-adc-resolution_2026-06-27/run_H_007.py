#!/usr/bin/env python3
"""Run script for H_007 — 12-bit ADC cannot deliver ppb CO2 sensing over ambient span.

Framed to falsify the "12-bit -> ppb over 420 ppm full-scale" claim: all falsifiers
PASS (none trigger) => 12 bits are insufficient. A trigger would mean 12 bits suffice.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

FULL = 420e-6       # ambient CO2 mole fraction
PPB = 1e-9          # 1 ppb target resolution
BITS = 12           # sigma-bit ADC

req_bits = cc.bits_for_resolution(FULL, PPB)
deficit = req_bits - BITS
# 12-bit coarsest step over the 420 ppm span, expressed in ppb:
coarsest_step_ppb = (FULL / (2 ** BITS)) / PPB
# span (in ppm) over which a 12-bit ADC *does* reach 1 ppb resolution:
feasible_span_ppm = ((2 ** BITS) * PPB) / 1e-6
nc_full = cc.bits_for_resolution(FULL, FULL)      # resolving full scale = 0 bits
nc_half = cc.bits_for_resolution(FULL, FULL / 2)  # halving the step = 1 bit

metrics = {
    "required_bits": req_bits,
    "bit_deficit_vs_12": deficit,
    "coarsest_step_ppb_at_12bit": coarsest_step_ppb,
    "feasible_span_ppm_at_12bit": feasible_span_ppm,
    "nc_full_scale_bits": nc_full,
    "nc_half_step_bits": nc_half,
}

falsifiers = [
    cc.Falsifier("F-007-1", lambda m: m["required_bits"] <= 12,
                 "12-bit would suffice for ppb over ambient"),
    cc.Falsifier("F-007-2", lambda m: m["bit_deficit_vs_12"] < 6,
                 "deficit < 6 bits (<64x short)"),
    cc.Falsifier("F-007-3", lambda m: m["coarsest_step_ppb_at_12bit"] < 50,
                 "12-bit coarsest step < 50 ppb (fine enough)"),
    cc.Falsifier("F-007-4", lambda m: m["nc_full_scale_bits"] != 0.0,
                 "resolving full scale is not 0 bits (log guard)"),
    cc.Falsifier("F-007-5", lambda m: abs(m["nc_half_step_bits"] - 1.0) > 1e-9,
                 "halving the step is not exactly 1 bit (neg control)"),
    cc.Falsifier("F-007-6", lambda m: m["feasible_span_ppm_at_12bit"] >= 420,
                 "12-bit already covers ambient at ppb (refutes must-narrow-span)"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "SUPPORTED here = the '12-bit ADC -> ppb over ambient' claim is refuted; ppb needs "
    "~19 bits or a ~100x narrower span."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_007 — 12-bit ADC vs ppb CO2 sensing")
print(f"  required bits (1 ppb over 420 ppm) = {req_bits:.2f}  (have sigma=12)")
print(f"  bit deficit                        = {deficit:.2f} bits ({2**deficit:.0f}x too few levels)")
print(f"  12-bit coarsest step over ambient  = {coarsest_step_ppb:.1f} ppb  (target 1 ppb)")
print(f"  span where 12-bit reaches 1 ppb    = {feasible_span_ppm:.2f} ppm  (vs 420 ppm ambient)")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (12-bit insufficient for ppb over ambient span)")
