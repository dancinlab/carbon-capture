---
id: H_016
slug: humidity-coload
title: Ambient air carries ~37× more H₂O than CO₂ (50% RH, 25°C), rising to ~170× at 40°C/100% RH — the parasitic water co-load the L0 candidate list ignores, and a key driver of real DAC energy
domain: sorbent
status: supported
exploration_method: closed-form Tetens vapour pressure → H₂O/CO₂ molar ratio
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_016 — Humidity co-load vs CO₂

## Hypothesis

The contactor does not see CO₂ in isolation — it sees air that is **~37× richer in
water vapour than in CO₂** at 50% RH / 25°C (`x_H2O ≈ 1.6%` vs `x_CO2 = 0.042%`),
and **~170×** at 40°C / 100% RH. On physisorbents H₂O competes for sites and is
co-desorbed, so a large share of the real regeneration energy (H_010) and lost
capacity (H_003/H_012) goes to **water, not CO₂**. The bare `L0.candidates` MOF list
(which says nothing about humidity) understates the real duty.

## Why

`L0.sorbent` lists physisorbent MOFs by metal/CN but not water tolerance — yet water
is the dominant minor species the sorbent must reject or tolerate. This card sizes the
co-load so the design record names humidity as a first-order constraint, linking to
the regeneration-energy (H_010) and binding-optimum (H_012) findings.

## Predictions

- **P1**: `humidity_to_co2_ratio(0.5, 25°C)` ∈ [30, 45] (≈ 37×).
- **P2**: ratio rises with temperature and RH — `ratio(1.0, 40°C)` ≥ 150×.
- **P3**: even cold/dry air (`ratio(0.2, 10°C)`) ≥ 3× (water still exceeds CO₂).
- **P4**: ratio scales linearly with RH at fixed T (`ratio(0.8,T) = 4× ratio(0.2,T)`).

## Variables

- `x_co2 = 420e-6` — source: spec.
- `p_atm = 101.325 kPa` — source: standard.
- `(RH, T) ∈ {(0.5,25),(1.0,40),(0.2,10),(0.8,25),(0.2,25)}` — source: ambient range, representative.
- Tetens: `es(T) = 0.6108·exp(17.27T/(T+237.3))` kPa — source: standard meteorology.
- output: H₂O/CO₂ molar ratio across conditions; RH-linearity check.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `humidity_to_co2_ratio`.
- **run script**: `state/H_016_humidity-coload_2026-06-27/run_H_016.py`
- **run cmd**: `python3 state/H_016_humidity-coload_2026-06-27/run_H_016.py`
- **artifacts**: `state/H_016_humidity-coload_2026-06-27/result.json`

## Criteria

- **C1**: P1–P4 hold → water co-load dominates the minor-species duty across ambient conditions.
- **verdict_rule**: SUPPORTED = all falsifiers PASS.

## Falsifiers (pre-registered, measurable)

- **F-016-1**: `ratio(0.5, 25)` < 30 or > 45 (vapour-pressure arithmetic off).
- **F-016-2**: `ratio(1.0, 40)` < 150 (hot humid air does not show a large co-load).
- **F-016-3**: `ratio(0.2, 10)` < 3 (water fails to exceed CO₂ even in cold/dry air).
- **F-016-4** (bounds check): `humidity_to_co2_ratio(rh=0, T)` = 0 (no water at 0% RH).
- **F-016-5** (negative control): `ratio(0.8,25) = 4 × ratio(0.2,25)` (linear in RH at fixed T).
- **F-016-6**: `humidity_to_co2_ratio(rh=1.5, …)` raises (RH > 100% is unphysical — domain guard).

## Honest Limits

- **L1**: molar abundance ≠ adsorbed amount — selectivity depends on the sorbent; hydrophobic
  sorbents/membranes reject most water, so the *delivered* co-load is sorbent-specific and lower.
  This card bounds the gas-phase challenge, not the captured ratio.
- **L2**: some processes exploit water (moisture-swing sorbents desorb CO₂ on wetting); for those
  the sign flips — water is a resource, not only a parasite. The card states the abundance, not the polarity of its effect.
- **L3**: Tetens is an approximation (~1% near 0–50°C); the order-of-magnitude co-load is robust to it.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `L0.sorbent`, `L0.candidates`, `L1.process`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_010 (regeneration heat), H_012 (binding optimum), H_003 (capacity).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**SUPPORTED** — 6/6 falsifiers PASS. Run `2026-06-27`. Verbatim stdout:

```
H_016 — humidity co-load vs CO2
  H2O/CO2 @ 50% RH, 25C = 37.2x
  H2O/CO2 @ 100% RH,40C = 173.3x
  H2O/CO2 @ 20% RH, 10C = 5.8x
  RH-linearity: ratio(80%)=59.5 vs 4x ratio(20%)=59.5
  [PASS] F-016-1
  [PASS] F-016-2
  [PASS] F-016-3
  [PASS] F-016-4
  [PASS] F-016-5
  [PASS] F-016-6
  6/6 falsifiers PASS
VERDICT: SUPPORTED  (water co-load dominates; first-order DAC constraint)
```

Artifact: `state/H_016_humidity-coload_2026-06-27/result.json`. Ambient air carries ~37× more
H₂O than CO₂ at 50% RH/25°C, ~170× at 40°C/100% RH, and still ~6× even cold/dry (20% RH/10°C).
Water is the dominant minor species the contactor must reject or tolerate — a first-order driver
of real regeneration energy (H_010) and lost capacity (H_012) that the bare `L0.candidates` MOF
list (metal/CN only, no water tolerance) entirely omits.
