#!/usr/bin/env python3
"""Run script for H_006 — is the n=6 lattice a predictor? (negative control).

Audits the 6 lattice->target identities against the physics verdicts of the sister
cards (H_001..H_005). The skeptical hypothesis (lattice is decorative, not predictive)
is SUPPORTED when >= 2 of 6 identities map to physically implausible targets AND a
physics-blind relabeling matches the targets just as easily.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tool"))

import carbon_capture as cc

# Numeric anchors (re-derived, not free parameters).
floor = cc.min_separation_work(420e-6, 298.15) / 1000.0   # H_001 anchor ~19.275
mf48 = cc.co2_mass_fraction(48.0)                          # H_003 anchor ~2.11 g/g

# The audit table: identity -> spec target -> plausibility (per sister-card verdicts).
audit = [
    {"identity": "J2-tau = 20 kJ/mol (floor)",       "sister": "H_001", "plausible": True},
    {"identity": "sigma-phi = 10x (headroom)",        "sister": "H_002", "plausible": True},
    {"identity": "J2*phi = 48 mmol/g (capacity)",     "sister": "H_003", "plausible": False},
    {"identity": "J2 = 24 $/ton (cost)",              "sister": "H_004", "plausible": False},
    {"identity": "n=6 hexagon (reactor)",             "sister": "H_005", "plausible": True},
    {"identity": "J2 = 24x capacity ratio (48/2)",    "sister": "H_003", "plausible": False},
]
n_total = len(audit)
n_implausible = sum(1 for a in audit if not a["plausible"])
frac_implausible = n_implausible / n_total

# Independent re-check of the two recomputable flags (F-006-6 consistency).
floor_flag_ok = (abs(floor - 20.0) < 2.0) == audit[0]["plausible"]      # floor ~ plausible
capacity_flag_ok = (mf48 > 1.0) == (not audit[2]["plausible"])          # 48 ~ implausible
flags_consistent = floor_flag_ok and capacity_flag_ok

# Negative control: a physics-blind relabeling from the lattice base {2,4,12,24}.
base = [2, 4, 12, 24]
reachable = set(base)
for a in base:
    for b in base:
        reachable.add(a + b)
        if a - b > 0:
            reachable.add(a - b)
        reachable.add(a * b)
        if b and a % b == 0:
            reachable.add(a // b)
numeric_targets = [20, 10, 48, 24, 6]   # the magnitude targets (hexagon is a count)
relabel_matches = sum(1 for t in numeric_targets if t in reachable)

metrics = {
    "floor_kj_mol": floor,
    "mass_frac_48_g_g": mf48,
    "n_total_identities": n_total,
    "n_implausible": n_implausible,
    "frac_implausible": frac_implausible,
    "flags_consistent": flags_consistent,
    "relabel_matches": relabel_matches,
    "relabel_total": len(numeric_targets),
}

falsifiers = [
    cc.Falsifier("F-006-1", lambda m: m["n_implausible"] <= 1,
                 "<=1 identity implausible (lattice would BE a predictor — refutes skeptic)"),
    cc.Falsifier("F-006-2", lambda m: abs(m["floor_kj_mol"] - 19.275) > 0.05,
                 "floor anchor diverges from H_001"),
    cc.Falsifier("F-006-3", lambda m: m["mass_frac_48_g_g"] <= 1.0,
                 "48 mmol/g anchor not implausible (contradicts H_003)"),
    cc.Falsifier("F-006-4", lambda m: not (0.0 <= m["frac_implausible"] <= 1.0),
                 "fraction implausible outside [0,1] (bounds)"),
    cc.Falsifier("F-006-5", lambda m: m["relabel_matches"] < 4,
                 "physics-blind relabeling does NOT cheaply match targets (neg control)"),
    cc.Falsifier("F-006-6", lambda m: not m["flags_consistent"],
                 "a recomputable plausibility flag disagrees with its sister card"),
]

ledger = cc.evaluate(metrics, falsifiers)
verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
ledger["verdict"] = verdict
ledger["interpretation"] = (
    "SUPPORTED here = the SKEPTICAL claim holds: the n=6 lattice is decorative, not "
    "predictive. It labels impossible targets (48 mmol/g, $24/ton) as cleanly as real "
    "ones (20 kJ/mol, hexagon), and a physics-blind relabel matches just as well."
)

with open(os.path.join(HERE, "result.json"), "w") as fh:
    json.dump(ledger, fh, indent=2)

print("H_006 — is the n=6 lattice a predictor? (negative control)")
print(f"  floor anchor       = {floor:.3f} kJ/mol  (H_001)")
print(f"  mass_frac(48) anchor = {mf48:.3f} g/g     (H_003, >1.0 = impossible)")
print(f"  audit: {n_implausible}/{n_total} lattice->target identities are physically implausible")
for a in audit:
    flag = "PLAUSIBLE  " if a["plausible"] else "IMPLAUSIBLE"
    print(f"    [{flag}] {a['identity']}  ({a['sister']})")
print(f"  fraction implausible = {frac_implausible:.2f}")
print(f"  neg control: physics-blind relabel matches {relabel_matches}/{len(numeric_targets)} targets")
for r in ledger["falsifiers"]:
    print(f"  [{r['status']}] {r['name']}")
print(f"  {ledger['n_pass']}/{ledger['n_total']} falsifiers PASS")
print(f"VERDICT: {verdict}  (lattice = decorative label, not a predictor)")
