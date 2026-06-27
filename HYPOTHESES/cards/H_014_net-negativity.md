---
id: H_014
slug: net-negativity
title: DAC at 9 GJ/ton is net-futile on a fossil grid — breakeven is ~0.40 kgCO₂/kWh, so a 0.45 grid removes ≤0 net; meaningful net-negativity needs clean energy (<~0.2 kg/kWh) OR the H_010 efficiency gains
domain: system
status: supported
exploration_method: closed-form lifecycle carbon balance (capture energy × grid intensity)
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_014 — Net-negativity threshold (lifecycle carbon)

## Hypothesis

Capturing CO₂ is only a *removal* if the energy to run it emits less CO₂ than it
captures. At today's ~9 GJ/ton (= 2500 kWh/ton, H_002), the **breakeven grid carbon
intensity is `1000 kg / 2500 kWh = 0.40 kgCO₂/kWh`**. A typical fossil-leaning grid
(~0.45) gives **net ≤ 0 — the plant emits as much as it removes**. Meaningful
net-negativity needs **clean power (< ~0.2 kg/kWh → ≥ 0.5 net)** *or* the H_010
efficiency gains (lower kWh/ton raises the breakeven intensity). DAC on a dirty grid
is not carbon removal.

## Why

This is the systems-level wire-to-reality check the per-level numbers omit: L4/L6
scale only makes sense if each ton is *net* removed. It couples the energy thesis
(H_001/H_002/H_010) to climate impact — the efficiency fight is also the
clean-energy-budget fight.

## Predictions

- **P1**: breakeven intensity at 9 GJ/ton ≈ 0.40 kg/kWh.
- **P2**: `net_capture_fraction(9 GJ/ton, 0.45)` ≤ 0 (fossil grid → futile or net-emitting).
- **P3**: `net_capture_fraction(9 GJ/ton, 0.05)` ≥ 0.8 (clean renewables → mostly net removal).
- **P4**: halving energy to 4.5 GJ/ton doubles the breakeven intensity to ~0.8 kg/kWh (efficiency relaxes the clean-power requirement).

## Variables

- `E_capture = 9e9 J/ton` (real DAC) — source: H_002 band, representative.
- `grid_intensity ∈ {0.45, 0.20, 0.05} kg/kWh` — source: fossil/mixed/renewable grids, representative.
- `E_half = 4.5e9 J/ton` (next-gen) — source: representative.
- output: net fraction at each intensity; breakeven intensity at 9 and 4.5 GJ/ton.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `net_capture_fraction`.
- **run script**: `state/H_014_net-negativity_2026-06-27/run_H_014.py`
- **run cmd**: `python3 state/H_014_net-negativity_2026-06-27/run_H_014.py`
- **artifacts**: `state/H_014_net-negativity_2026-06-27/result.json`

## Criteria

- **C1**: P1–P4 hold → fossil-grid DAC is futile; clean energy / efficiency is mandatory.
- **verdict_rule**: SUPPORTED here = the "futile on fossil, needs clean energy" claim survives.

## Falsifiers (pre-registered, measurable)

- **F-014-1**: `net_capture_fraction(9 GJ/ton, 0.45)` > 0.1 (fossil grid would still net-remove meaningfully).
- **F-014-2**: breakeven intensity at 9 GJ/ton outside [0.35, 0.45] kg/kWh (arithmetic off).
- **F-014-3**: `net_capture_fraction(9 GJ/ton, 0.05)` < 0.8 (even clean power fails to net-remove).
- **F-014-4** (bounds check): `net_capture_fraction(0, x)` = 1.0 (zero energy → 100% net, trivially).
- **F-014-5** (negative control): `net_capture_fraction(E, 0)` = 1.0 for any E (zero-carbon energy → fully net).
- **F-014-6**: halving energy does NOT roughly double the breakeven intensity (efficiency-doesn't-help — would break the linear coupling).

## Honest Limits

- **L1**: only operating-energy carbon is modeled — embodied carbon (steel, sorbent manufacture,
  construction) adds a fixed debt that further raises the effective intensity, never lowers it.
- **L2**: grid intensity is marginal and time-varying; co-locating with curtailed renewables can
  hit ~0 kg/kWh, but then DAC competes with other uses for that clean power (opportunity cost).
- **L3**: assumes the captured CO₂ is permanently stored; if it leaks or is used in a fuel that
  re-emits, the "removal" is temporary regardless of the energy source (permanence, see H_015).

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `thesis.energy-floor`, `L6.universal`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_002 (energy), H_010 (efficiency lever), H_009 (planetary energy budget).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**SUPPORTED** (the "futile on fossil, needs clean energy" claim survives) — 6/6 falsifiers PASS.
Run `2026-06-27`. Verbatim stdout:

```
H_014 — net-negativity threshold
  capture energy           = 2500 kWh/ton
  breakeven grid intensity = 0.400 kg/kWh  (halved energy -> 0.800)
  net @ 0.45 fossil grid   = -0.12 ton/ton  FUTILE
  net @ 0.20 mixed grid    = +0.50 ton/ton
  net @ 0.05 clean grid    = +0.88 ton/ton
  [PASS] F-014-1
  [PASS] F-014-2
  [PASS] F-014-3
  [PASS] F-014-4
  [PASS] F-014-5
  [PASS] F-014-6
  6/6 falsifiers PASS
VERDICT: SUPPORTED  (fossil-grid DAC futile; clean energy / efficiency mandatory)
```

Artifact: `state/H_014_net-negativity_2026-06-27/result.json`. At 9 GJ/ton the breakeven grid
intensity is 0.40 kgCO₂/kWh — a fossil-leaning grid (0.45) yields **net −0.12 ton/ton** (emits
more than it removes). Clean power (0.05) gives +0.88. And halving the energy doubles the
breakeven to 0.80, so the H_010 efficiency fight directly relaxes the clean-power requirement.
The whole HEXA-CCUS stack is conditional on clean energy — a systems wire-to-reality the
per-level numbers omit.
