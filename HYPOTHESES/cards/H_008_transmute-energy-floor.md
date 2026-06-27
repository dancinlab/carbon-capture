---
id: H_008
slug: transmute-energy-floor
title: Reducing captured CO₂ to solid carbon costs ≥32.8 GJ/ton-C (≈9 GJ/ton-CO₂) — comparable to today's whole capture energy, ~20× the capture floor; and $1M/ton graphene cannot survive Mt-scale
domain: transmute
status: supported
exploration_method: closed-form reduction enthalpy + market-saturation bound
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_008 — Transmutation energy floor & value-at-scale

## Hypothesis

`thesis.waste-to-value` / L5 frames CO₂→graphene/diamond as a value-add bonus
($0/ton → ~$1M/ton). Two closed-form checks refute the "free bonus at scale" reading:

1. **Energy** — turning CO₂ back into solid carbon is the reverse of combustion. Its
   thermodynamic floor is the CO₂ formation enthalpy: `393.5 kJ/mol ÷ 12.011 g/mol ×
   1e6 = 32.8 GJ per ton of carbon` (≈ 9 GJ/ton-CO₂). That is **comparable to today's
   entire capture energy (~9 GJ/ton-CO₂)** and **~20× the capture thermodynamic floor
   (0.44 GJ/ton-CO₂)** — conversion is the *energy-dominant* step, not a free bonus.
2. **Value at scale** — `$1M/ton × 1 Mt/yr = $1e12/yr`, ~1000× the entire current
   graphene market (~$1B/yr). The $1M/ton price is a *niche* figure that collapses
   under Mt-scale oversupply.

## Why

The waste-to-value pitch (`thesis.waste-to-value`, `L5.transmute`) makes CO₂
conversion sound like upside. This card holds it to first-principles energy and
market arithmetic. The *direction* (carbon products have value) survives; the
"$1M/ton, energy-free at scale" reading does not.

## Predictions

- **P1**: `carbon_reduction_energy_floor()` ∈ [30, 35] GJ/ton-C (≈ 32.8).
- **P2**: reduction floor per ton-CO₂ ≥ 15× the capture thermodynamic floor (0.44 GJ/ton-CO₂).
- **P3**: reduction floor per ton-CO₂ ≥ 5 GJ — i.e. on the order of real capture energy,
  not negligible.
- **P4**: `$1M/ton × 1 Mt/yr` ≥ 100× a $1B/yr reference market → price unsustainable at scale.

## Variables

- `dh_f_co2 = 393.5e3 J/mol` (CO₂ formation enthalpy) — source: thermochemistry, standard.
- `M_C = 12.011`, `M_CO2 = 44.009` — source: standard.
- `capture_floor = min_separation_work(420 ppm)/M_CO2*1e6` ≈ 0.44 GJ/ton-CO₂ — from H_001.
- `price = 1e6 $/ton`, `scale = 1e6 ton/yr`, `market_ref = 1e9 $/yr` — source: spec / market, representative.
- output: reduction floor (GJ/ton-C and GJ/ton-CO₂); ratio to capture floor; revenue/market ratio.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `carbon_reduction_energy_floor`, `min_separation_work`.
- **run script**: `state/H_008_transmute-energy-floor_2026-06-27/run_H_008.py`
- **run cmd**: `python3 state/H_008_transmute-energy-floor_2026-06-27/run_H_008.py`
- **artifacts**: `state/H_008_transmute-energy-floor_2026-06-27/result.json`

## Criteria

- **C1**: P1–P4 hold → "free value bonus at scale" refuted (energy-dominant + market-saturating).
- **verdict_rule**: SUPPORTED here = the skeptical claim survives all falsifiers.

## Falsifiers (pre-registered, measurable)

- **F-008-1**: `carbon_reduction_energy_floor()` < 30 or > 35 GJ/ton-C (enthalpy arithmetic off).
- **F-008-2**: reduction floor per ton-CO₂ < 15× the capture floor (conversion not energy-dominant).
- **F-008-3**: reduction floor per ton-CO₂ < 5 GJ (conversion energy negligible vs capture).
- **F-008-4** (bounds check): `carbon_reduction_energy_floor(dh_f=0)` raises (no free reduction).
- **F-008-5** (negative control): reduction floor scales linearly — `floor(2·ΔHf) = 2·floor(ΔHf)`.
- **F-008-6**: `price × scale` < 100× `market_ref` (Mt-scale revenue would fit the market → $1M/ton sustainable).

## Honest Limits

- **L1**: the 32.8 GJ/ton-C floor is the *thermodynamic minimum*; real electrochemical/CVD
  routes are far less efficient, so the true energy is higher — the floor only strengthens the
  "energy-dominant" conclusion, it cannot weaken it.
- **L2**: some products (diamond, structural graphite) embody less reduction if made from
  partially-reduced feeds (CO, CH₄); this card assumes the full CO₂→C(graphite)+O₂ path the
  spec implies. Co-product O₂ has minor value, not modeled.
- **L3**: market saturation uses a single representative current-market figure; a future
  bulk carbon-materials market (construction-scale) could be far larger, but then the price is
  no longer $1M/ton — the two assumptions ($1M/ton AND Mt/yr) cannot hold together.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `thesis.waste-to-value`, `L5.transmute`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_001 (capture floor baseline), H_004 (cost realism), H_006 (numerology).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**SUPPORTED** (the "free value bonus at scale" reading is refuted) — 6/6 falsifiers PASS.
Run `2026-06-27`. Verbatim stdout:

```
H_008 — transmutation energy floor & value-at-scale
  CO2->C reduction floor   = 32.76 GJ/ton-C = 8.94 GJ/ton-CO2
  capture thermo floor     = 0.438 GJ/ton-CO2  (H_001)
  reduction / capture floor = 20.4x
  $1M/ton x 1 Mt/yr        = $1000B/yr  = 1000x the ~$1B/yr graphene market
  [PASS] F-008-1
  [PASS] F-008-2
  [PASS] F-008-3
  [PASS] F-008-4
  [PASS] F-008-5
  [PASS] F-008-6
  6/6 falsifiers PASS
VERDICT: SUPPORTED  (conversion energy-dominant; $1M/ton not scale-sustainable)
```

Artifact: `state/H_008_transmute-energy-floor_2026-06-27/result.json`. Reducing CO₂ to solid
carbon costs ≥32.8 GJ/ton-C (8.94 GJ/ton-CO₂) — **20× the capture thermodynamic floor** and on
par with today's whole capture energy, so conversion is the energy-dominant step, not a free
bonus. And $1M/ton × 1 Mt/yr = $1000B/yr is ~1000× the current graphene market — the niche price
cannot survive Mt-scale. The waste-to-value *direction* stands; the "$1M/ton, energy-free at
scale" framing does not. Pairs with H_004 (cost realism).
