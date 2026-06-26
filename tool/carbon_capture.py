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
