"""carbon_capture — shared runnable harness for HYPOTHESES hypothesis cards.

Deterministic, dependency-free (stdlib `math` only) primitives for the CO2
capture-storage-conversion (HEXA-CCUS) problem. HYPOTHESES cards reference these
functions from their per-hypothesis run scripts under `state/<hX>/` (anima-parity:
shared machinery lives in repo-root `tool/`, per-hypothesis runs live in `state/`).

Every function is a closed-form public relation — no fitting, no hidden constants
beyond documented defaults. All inputs are explicit so a card's falsifiers can be
evaluated against the returned numbers.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# Universal gas constant (J/mol/K).
R_GAS = 8.314462618

# Molar mass of CO2 (g/mol) — used for gravimetric uptake <-> mass-fraction conversion.
M_CO2 = 44.009

# Molar mass of carbon (g/mol).
M_C = 12.011

# Standard enthalpy of formation of CO2 from graphite + O2 (J/mol, magnitude). The
# reverse (CO2 -> C(graphite) + O2) costs at least this much — the thermodynamic floor
# to reduce captured CO2 back to solid carbon (HEXA-TRANSMUTE L5).
DH_F_CO2 = 393.5e3

# Atmospheric mass of CO2 per ppmv (Gt CO2 / ppmv). 1 ppmv CO2 ~ 2.13 Gt C ~ 7.82 Gt CO2.
GT_CO2_PER_PPM = 7.82


# --- thermodynamic separation floor -------------------------------------------

def min_separation_work(x_co2: float, temp_k: float = 298.15) -> float:
    """Minimum reversible work to separate CO2 from a mixture, per mole CO2:

        W_min = R * T * ln(1 / x_CO2)        [J/mol]

    The Sherwood/thermodynamic floor. At ambient air x_CO2 ~ 4.2e-4 and T=298 K
    this is ~ 20 kJ/mol (the HEXA-CCUS `J2 - tau = 20` target floor); today's wet
    amine rigs sit ~ 10x above it.
    """
    if not (0.0 < x_co2 < 1.0):
        raise ValueError(f"x_co2 must be in (0,1): {x_co2}")
    if temp_k <= 0:
        raise ValueError(f"temp_k must be > 0: {temp_k}")
    return R_GAS * temp_k * math.log(1.0 / x_co2)


def energy_headroom(current_kj_mol: float, floor_kj_mol: float) -> float:
    """Reduction factor between a current capture energy and the thermodynamic
    floor: current / floor. ~10x for 200 kJ/mol amine vs the ~20 kJ/mol floor."""
    if floor_kj_mol <= 0:
        raise ValueError(f"floor must be > 0: {floor_kj_mol}")
    return current_kj_mol / floor_kj_mol


# --- sorbent / capacity --------------------------------------------------------

def capacity_ratio(target_mmol_g: float, baseline_mmol_g: float) -> float:
    """Working-capacity improvement of a sorbent vs a baseline (e.g. Climeworks
    ~2.0 mmol/g). Target 48 mmol/g = J2*phi gives a 24x ratio."""
    if baseline_mmol_g <= 0:
        raise ValueError(f"baseline must be > 0: {baseline_mmol_g}")
    return target_mmol_g / baseline_mmol_g


# --- cost / throughput ---------------------------------------------------------

def cost_ratio(baseline_usd_ton: float, target_usd_ton: float) -> float:
    """Capture-cost reduction factor, baseline / target. Climeworks ~$600/ton vs
    the $24/ton (= J2) target gives a 25x ratio."""
    if target_usd_ton <= 0:
        raise ValueError(f"target must be > 0: {target_usd_ton}")
    return baseline_usd_ton / target_usd_ton


def annual_capacity_ratio(plant_ton_yr: float, baseline_ton_yr: float) -> float:
    """Per-plant annual-capture scale-up vs a baseline (Climeworks ~4 kt/yr).
    HEXA-PLANT 1 Mt/yr gives a 250x ratio."""
    if baseline_ton_yr <= 0:
        raise ValueError(f"baseline must be > 0: {baseline_ton_yr}")
    return plant_ton_yr / baseline_ton_yr


# --- gravimetric bound ---------------------------------------------------------

def co2_mass_fraction(mmol_per_g: float) -> float:
    """Convert a gravimetric CO2 uptake (mmol CO2 per gram of sorbent) into the
    mass of CO2 captured per gram of sorbent:

        m_CO2/m_sorbent = uptake[mol/g] * M_CO2[g/mol]
                        = mmol_per_g * 1e-3 * 44.009

    A physical sanity bound for any sorbent target. The HEXA-CCUS `48 mmol/g`
    (= J2*phi) target maps to 48e-3 * 44.009 = 2.11 g CO2 per g sorbent (211 %
    of the sorbent's own mass) — far above any measured adsorbent, which top out
    near ~1 mmol/g at DAC partial pressure and well under ~1 g/g even at high
    pressure. Returned value is dimensionless (g per g)."""
    if mmol_per_g < 0:
        raise ValueError(f"mmol_per_g must be >= 0: {mmol_per_g}")
    return mmol_per_g * 1e-3 * M_CO2


# --- packing geometry ----------------------------------------------------------

def perimeter_area_ratio(n_sides: int) -> float:
    """Dimensionless wall-cost of a regular n-gon channel: perimeter divided by
    sqrt(area), the cross-sectional wall length per unit throughput area.

        P / sqrt(A) = 2 * sqrt(n * tan(pi / n))

    Lower = less wall material per unit flow area. Among the only three regular
    polygons that tile the plane (n=3,4,6), the hexagon (n=6) is the minimum —
    the closed-form statement behind the honeycomb conjecture (Hales 2001) and
    the HEXA-REACTOR geometry choice. The circle (limit n->inf) gives 2*sqrt(pi)
    = 3.545 but does not tile."""
    if n_sides < 3:
        raise ValueError(f"n_sides must be >= 3: {n_sides}")
    return 2.0 * math.sqrt(n_sides * math.tan(math.pi / n_sides))


# --- sensing resolution (L3 chip) ---------------------------------------------

def bits_for_resolution(full_scale: float, resolution: float) -> float:
    """ADC bit-depth required to resolve `resolution` over a `full_scale` span:

        bits = log2(full_scale / resolution)

    e.g. resolving 1 ppb of CO2 over a 420 ppm (= 420_000 ppb) ambient full-scale
    needs log2(420_000) ~ 18.7 bits — far above the HEXA-CHIP `sigma = 12`-bit ADC.
    Returned value is a real number of bits (not yet rounded up)."""
    if full_scale <= 0 or resolution <= 0:
        raise ValueError(f"full_scale and resolution must be > 0: {full_scale}, {resolution}")
    return math.log2(full_scale / resolution)


# --- CO2 -> carbon reduction floor (L5 transmute) -----------------------------

def carbon_reduction_energy_floor(dh_f_co2_j_mol: float = DH_F_CO2) -> float:
    """Thermodynamic minimum energy to reduce CO2 to one ton of solid carbon, per
    ton of carbon product:

        E_floor = dh_f_co2 / M_C * 1e6        [J / ton C]

    Uses the CO2 formation enthalpy (default DH_F_CO2 = 393.5 kJ/mol). This is the
    reverse-of-combustion floor for CO2 -> C + O2 (HEXA-TRANSMUTE), before any CVD
    overhead — a hard lower bound, ignoring catalysts/electrochem efficiency."""
    if dh_f_co2_j_mol <= 0:
        raise ValueError(f"dh_f_co2_j_mol must be > 0: {dh_f_co2_j_mol}")
    return dh_f_co2_j_mol / M_C * 1e6


# --- planetary mass balance (L6 universal) ------------------------------------

def ppm_to_gt_co2(delta_ppm: float, gt_per_ppm: float = GT_CO2_PER_PPM) -> float:
    """Atmospheric CO2 mass (Gt CO2) corresponding to a `delta_ppm` change in mixing
    ratio: delta_ppm * GT_CO2_PER_PPM. Drawing 420 -> 280 ppm (140 ppm) is ~1095 Gt
    CO2 of gross atmospheric removal (before ocean re-equilibration)."""
    if delta_ppm < 0:
        raise ValueError(f"delta_ppm must be >= 0: {delta_ppm}")
    return delta_ppm * gt_per_ppm


# --- falsifier harness --------------------------------------------------------

@dataclass
class Falsifier:
    """One pre-registered, measurable falsifier. `predicate(metrics) -> bool`
    returns True when the falsifier is TRIGGERED (hypothesis component refuted)."""

    name: str
    predicate: object  # callable(dict) -> bool
    desc: str = ""


def evaluate(metrics: dict, falsifiers: list) -> dict:
    """Run each falsifier against the measured metrics. A falsifier PASSes when
    it is NOT triggered. Returns a verdict ledger (all-stdlib, JSON-safe)."""
    results = []
    for f in falsifiers:
        triggered = bool(f.predicate(metrics))
        results.append(
            {"name": f.name, "triggered": triggered, "status": "FAIL" if triggered else "PASS"}
        )
    n_pass = sum(1 for r in results if r["status"] == "PASS")
    return {
        "metrics": metrics,
        "falsifiers": results,
        "n_pass": n_pass,
        "n_total": len(results),
        "all_pass": n_pass == len(results),
    }
