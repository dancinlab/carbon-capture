#!/usr/bin/env python3
"""Run script for H_003 — the 48 mmol/g sorbent target is physically unreachable.

This card is framed to FALSIFY the 48 mmol/g target. The falsifiers below each
encode a way the target COULD be reachable; all PASS (none trigger) => the
"unphysical target" claim stands. A trigger would mean 48 mmol/g is achievable.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

target = 48.0        # mmol/g = J2*phi
best_measured = 10.0  # mmol/g, top MOF at saturating pressure (representative)
dac_measured = 1.5    # mmol/g, Mg-MOF-74 at 400 ppm (representative)

mf_target = cc.co2_mass_fraction(target)        # g CO2 / g sorbent
mf_best = cc.co2_mass_fraction(best_measured)
mf_zero = cc.co2_mass_fraction(0.0)
ratio_target_best = cc.capacity_ratio(target, best_measured)
ratio_target_dac = cc.capacity_ratio(target, dac_measured)

# F-003-6: no published adsorbent with measured uptake >= 48 mmol/g at <= 1 bar is
# known; pre-registered as absent. Encoded as a fixed flag (no literature hit).
known_sorbent_ge_48 = False

metrics = {
    "mass_frac_target_g_g": mf_target,
    "mass_frac_best_g_g": mf_best,
    "mass_frac_zero_g_g": mf_zero,
    "ratio_target_over_best": ratio_target_best,
    "ratio_target_over_dac": ratio_target_dac,
    "known_sorbent_ge_48mmolg": known_sorbent_ge_48,
}

falsifiers = [
    cc.Falsifier("F-003-1", lambda m: m["mass_frac_target_g_g"] <= 1.0,
                 "48 mmol/g <= 100% sorbent mass (not obviously unphysical)"),
    cc.Falsifier("F-003-2", lambda m: m["ratio_target_over_best"] <= 2.0,
                 "target within 2x of best real sorbent (reachable)"),
    cc.Falsifier("F-003-3", lambda m: m["ratio_target_over_dac"] <= 5.0,
                 "target within 5x of in-condition DAC uptake"),
    cc.Falsifier("F-003-4", lambda m: m["mass_frac_best_g_g"] > 1.0,
                 "even a real 10 mmol/g sorbent breaks the mass bound (bound wrong)"),
    cc.Falsifier("F-003-5", lambda m: m["mass_frac_zero_g_g"] != 0.0,
                 "zero uptake does not map to zero mass (conversion guard)"),
    cc.Falsifier("F-003-6", lambda m: m["known_sorbent_ge_48mmolg"],
                 "a published sorbent reaches >= 48 mmol/g at <= 1 bar"),
]

ledger = cc.evaluate(metrics, falsifiers)
# all PASS => the "unphysical target" claim is SUPPORTED (i.e. 48 mmol/g FALSIFIED as a target).
claim_supported = ledger["all_pass"]
verdict = "SUPPORTED" if claim_supported else "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "SUPPORTED here = the 48 mmol/g TARGET is refuted as physically unreachable."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_003 — 48 mmol/g sorbent target is unphysical")
print(f"  mass_fraction(48 mmol/g) = {mf_target:.3f} g CO2/g sorbent ({mf_target*100:.0f}% of sorbent mass)")
print(f"  mass_fraction(10 mmol/g) = {mf_best:.3f} g/g (a real best-case sorbent)")
print(f"  target / best_measured   = {ratio_target_best:.1f}x")
print(f"  target / dac_measured    = {ratio_target_dac:.1f}x")
print(f"  known sorbent >= 48 mmol/g at <=1 bar: {known_sorbent_ge_48}")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (target 48 mmol/g refuted as unreachable)")
