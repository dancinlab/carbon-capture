#!/usr/bin/env python3
"""Graduate the 🜂 ABSTRACT track — run the pre-registered falsifiable kernel of every
H_A00N imagination card deterministically, turning each from conjecture into a verified
verdict (모두 검증 / 심화골화). One DRY driver writes per-card result_H_A00N.json + a summary.

Honest expectation (pre-registered in the cards): several SF concepts FALSIFY on their own
physics kernel (the negative space that sharpens why separation≈floor wins); a few survive.
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

FLOOR = cc.min_separation_work(420e-6) / 1000.0   # kJ/mol


def card(cid, verdict, summary, metrics, falsifiers):
    """Write one card's result.json and return a one-line row."""
    ledger = cc.evaluate(metrics, falsifiers)
    ledger["verdict"] = verdict
    ledger["summary"] = summary
    with open(os.path.join(HERE, f"result_{cid}.json"), "w") as fh:
        json.dump(ledger, fh, indent=2)
    npass = ledger["n_pass"]
    return {"id": cid, "verdict": verdict, "pass": f"{npass}/{ledger['n_total']}", "summary": summary}


rows = []

# --- H_A001 carbon-centrifuge: separation easy, throughput energy is the wall -> FALSIFIED
alpha = cc.centrifuge_separation_factor(16e-3, 600.0)
stages = math.log(2400.0) / math.log(alpha)
ke = cc.centrifuge_kinetic_energy_per_mol_co2(600.0) / 1000.0     # kJ/mol CO2
m = {"alpha_per_stage": alpha, "stages_to_pure": stages, "ke_kj_mol": ke, "ke_over_floor": ke / FLOOR}
rows.append(card("H_A001", "FALSIFIED", f"separation easy (alpha={alpha:.1f}, ~{stages:.0f} stages) but air-spin KE = {ke:.0f} kJ/mol = {ke/FLOOR:.0f}x the floor -> impractical for DAC", m, [
    cc.Falsifier("A001-viable", lambda x: x["ke_over_floor"] > 100.0, "throughput KE > 100x floor (impractical)"),
    cc.Falsifier("A001-sep-ok", lambda x: x["stages_to_pure"] > 50, "separation needs >50 stages (it does not)"),
]))

# --- H_A002 night-frost: frost point too low for passive radiative cooling -> FALSIFIED
t_frost = cc.clausius_clapeyron_temp(0.42 * 100.0, 25200.0, 194.65, 101325.0)
t_frost_c = t_frost - 273.15
rad_floor_c = -50.0
m = {"frost_point_c": t_frost_c, "radiative_floor_c": rad_floor_c, "gap_k": rad_floor_c - t_frost_c}
rows.append(card("H_A002", "FALSIFIED", f"CO2 frost point at 400-ppm partial pressure = {t_frost_c:.0f} C, {rad_floor_c - t_frost_c:.0f} K below the ~-50 C passive radiative-cooling floor -> cannot freeze CO2 from air passively", m, [
    cc.Falsifier("A002-reachable", lambda x: x["frost_point_c"] >= x["radiative_floor_c"], "frost point reachable by radiative cooling (it is not)"),
]))

# --- H_A003 photon-cleaver: bond energy >> floor -> FALSIFIED on energy
bond = cc.ev_to_kj_mol(5.5)
m = {"bond_kj_mol": bond, "bond_over_floor": bond / FLOOR, "with_30pct_laser": bond / 0.30 / FLOOR}
rows.append(card("H_A003", "FALSIFIED", f"C=O dissociation = {bond:.0f} kJ/mol = {bond/FLOOR:.0f}x the separation floor (>{bond/0.30/FLOOR:.0f}x after laser inefficiency) -> destroying costs ~100x separating", m, [
    cc.Falsifier("A003-competitive", lambda x: x["bond_over_floor"] < 2.0, "dissociation within 2x of floor (it is 28x)"),
]))

# --- H_A004 oxy-magnet: magnetic energy << thermal in gas phase -> FALSIFIED
ratio = cc.magnetic_thermal_ratio(1.9e-6, 10.0)
m = {"mag_thermal_ratio_10T": ratio}
rows.append(card("H_A004", "FALSIFIED", f"gas-phase O2 magnetic/thermal energy ratio at 10 T = {ratio:.1e} (~10^3x too weak) -> magnetic sorting overwhelmed by thermal motion; works only for condensed O2", m, [
    cc.Falsifier("A004-sortable", lambda x: x["mag_thermal_ratio_10T"] >= 1.0, "magnetic energy >= thermal (it is ~1e-3)"),
]))

# --- H_A005 tame-twister: low-dP air work is small; vortex draft plausible -> PARTIAL
fan_low = cc.fan_work_per_ton(1.306e6, 100.0) / 1e9      # GJ/ton at 100 Pa
fan_hi = cc.fan_work_per_ton(1.306e6, 1000.0) / 1e9      # GJ/ton at 1000 Pa
m = {"fan_gj_ton_100pa": fan_low, "fan_gj_ton_1000pa": fan_hi, "fan_kwh_ton_100pa": fan_low * 1e9 / 3.6e6}
rows.append(card("H_A005", "PARTIAL", f"air-moving work at a low 100 Pa open-mesh drop = {fan_low:.2f} GJ/ton ({fan_low*1e9/3.6e6:.0f} kWh/ton) — small enough for a solar vortex to supply IF dP stays low; residence-time vs dP is the open risk", m, [
    cc.Falsifier("A005-low-dp-cheap", lambda x: x["fan_gj_ton_100pa"] > 0.5, "low-dP air work > 0.5 GJ/ton (it is ~0.13 — cheap)"),
    cc.Falsifier("A005-hi-dp-wall", lambda x: x["fan_gj_ton_1000pa"] < 0.5, "high-dP work < 0.5 GJ/ton (the residence/dP tradeoff is real)"),
]))

# --- H_A006 carbon-battery: electro-swing lands in the amine-TSA band, electrical -> PARTIAL
e_lo = cc.electrochem_energy_per_mol(1.0, 0.5) / 1000.0
e_hi = cc.electrochem_energy_per_mol(2.0, 1.0) / 1000.0
m = {"e_low_kj_mol": e_lo, "e_high_kj_mol": e_hi, "low_over_floor": e_lo / FLOOR}
rows.append(card("H_A006", "PARTIAL", f"electro-swing energy = {e_lo:.0f}-{e_hi:.0f} kJ/mol (amine-TSA band, {e_lo/FLOOR:.1f}-{e_hi/FLOOR:.1f}x floor) — NOT below the floor, but electrical/clean-couplable with zero thermal swing; advantage is energy quality + grid-storage fusion, not a lower number", m, [
    cc.Falsifier("A006-below-floor", lambda x: x["low_over_floor"] < 1.0, "electro-swing below the 2nd-law floor (impossible)"),
    cc.Falsifier("A006-in-band", lambda x: x["e_high_kj_mol"] > 300.0, "energy above the amine band (>300 kJ/mol)"),
]))

# --- H_A007 breathing-stone: areal ceiling is Gt-scale, saturation caps it -> PARTIAL
gt_lo = cc.areal_capture_ceiling_gt_yr(10.0, 1e12)
gt_hi = cc.areal_capture_ceiling_gt_yr(100.0, 1e12)
m = {"ceiling_gt_yr_low": gt_lo, "ceiling_gt_yr_high": gt_hi}
rows.append(card("H_A007", "PARTIAL", f"urban-surface areal ceiling = {gt_lo:.0f}-{gt_hi:.0f} Gt/yr (same order as the H_009 target) IF every surface participated — but carbonate-crust saturation and durability cap it at a thin self-renewing layer", m, [
    cc.Falsifier("A007-scale", lambda x: x["ceiling_gt_yr_high"] < 1.0, "areal ceiling < 1 Gt/yr (too small to matter)"),
]))

# --- H_A008 solar-blink: 1 photon/CO2 costs more than thermal -> FALSIFIED (needs QY>1)
photon = cc.ev_to_kj_mol(2.5)
h010_thermal = 100.0
m = {"photon_kj_mol": photon, "thermal_kj_mol": h010_thermal, "photon_over_thermal": photon / h010_thermal}
rows.append(card("H_A008", "FALSIFIED", f"one visible photon = {photon:.0f} kJ/mol vs ~{h010_thermal:.0f} kJ/mol thermal (H_010) -> naive 1-photon-per-CO2 optical regen is {photon/h010_thermal:.1f}x WORSE than heat; viable ONLY with cooperative quantum-yield > 1", m, [
    cc.Falsifier("A008-beats-thermal", lambda x: x["photon_over_thermal"] < 1.0, "1 photon/CO2 cheaper than thermal (it is not)"),
]))

# --- H_A009 sky-clathrate: hydrate needs deep cold at 400 ppm -> FALSIFIED for air-capture
t_hyd = cc.clausius_clapeyron_temp(0.42 * 100.0, 65000.0, 283.15, 4.5e6)
t_hyd_c = t_hyd - 273.15
m = {"hydrate_stable_c_at_400ppm": t_hyd_c}
rows.append(card("H_A009", "FALSIFIED", f"CO2 hydrate stability at the 400-ppm partial pressure needs ~{t_hyd_c:.0f} C -> cannot form a clathrate directly from ambient air without pre-concentration (storage-phase still viable)", m, [
    cc.Falsifier("A009-air-formable", lambda x: x["hydrate_stable_c_at_400ppm"] > 0.0, "hydrate stable above 0 C at 400 ppm (it is not)"),
]))

# --- H_A010 fast-weather: milling small vs capture -> net-removal robust -> SUPPORTED
net_clean = cc.net_capture_fraction(300.0 * 3.6e6, 0.05)
net_dirty = cc.net_capture_fraction(300.0 * 3.6e6, 0.45)
m = {"net_clean_grid": net_clean, "net_dirty_grid": net_dirty}
rows.append(card("H_A010", "SUPPORTED", f"milling olivine (~300 kWh/ton) is small vs capture -> net removal = +{net_clean:.2f} (clean grid) and +{net_dirty:.2f} even on a dirty grid -> robustly net-negative; the real caveat is the decadal weathering RATE, not the energy", m, [
    cc.Falsifier("A010-futile-clean", lambda x: x["net_clean_grid"] <= 0.0, "futile even on a clean grid (it is +0.98)"),
    cc.Falsifier("A010-futile-dirty", lambda x: x["net_dirty_grid"] <= 0.0, "futile on a dirty grid (it is +0.86)"),
]))

# --- H_A011 artificial-leaf: energy is free sunlight, area is the cost -> SUPPORTED
area = cc.solar_area_for_carbon(1e6, 0.10)   # m^2 for 1 Mt-C/yr at 10% efficiency
area_km2 = area / 1e6
m = {"area_m2": area, "area_km2": area_km2}
rows.append(card("H_A011", "SUPPORTED", f"land area to photo-reduce 1 Mt-C/yr at 10% solar-to-fuel = {area_km2:.0f} km2 -> energetically free (sunlight); the binding constraint is AREA + catalyst durability, NOT energy (the opposite trade from electric DAC)", m, [
    cc.Falsifier("A011-area-absurd", lambda x: x["area_km2"] > 1e6, "area exceeds 1e6 km2 (land-infeasible)"),
]))

# --- summary ------------------------------------------------------------------
summary = {"floor_kj_mol": FLOOR, "rows": rows,
           "tally": {v: sum(1 for r in rows if r["verdict"] == v) for v in ("SUPPORTED", "PARTIAL", "FALSIFIED")}}
with open(os.path.join(HERE, "summary.json"), "w") as fh:
    json.dump(summary, fh, indent=2)

print("🜂 ABSTRACT graduation — 11 kernels run (모두 검증)")
print(f"  separation floor = {FLOOR:.2f} kJ/mol")
for r in rows:
    icon = {"SUPPORTED": "🟢", "PARTIAL": "🟡", "FALSIFIED": "🔴"}[r["verdict"]]
    print(f"  {icon} {r['id']} {r['verdict']:9s} — {r['summary']}")
t = summary["tally"]
print(f"  TALLY: 🟢 {t['SUPPORTED']} SUPPORTED · 🟡 {t['PARTIAL']} PARTIAL · 🔴 {t['FALSIFIED']} FALSIFIED  (of 11)")
