---
id: H_013
slug: plant-air-throughput
title: 1 Mt/yr DAC = 250× Climeworks (arithmetic checks) but must pull ~1.3e12 m³ air/yr through the contactor at 420 ppm — the air-handling/fan-power scale wall, not a chemistry wall
domain: plant
status: supported
exploration_method: closed-form air-throughput mass balance + scale-up ratio
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_013 — Plant scale-up: air throughput wall

## Hypothesis

L4's `1 Mt/yr (250× Climeworks)` is arithmetically sound (`1e6 / 4e3 kt = 250×`),
but the binding constraint at DAC dilution is **air handling**: capturing 1 ton of
CO₂ from 420 ppm air requires moving `~1.3e6 m³` of air past the sorbent (even at
100% single-pass capture). At 1 Mt/yr that is **~1.3e12 m³ air/yr** — the volume
behind DAC's fan power and contactor area. The DAC wall is moving air, not binding
CO₂: a dilution/throughput engineering problem (break-walls: investment/infra wall).

## Why

`L4.plant` claims industrial scale; `flow.capture` starts at the air contactor. This
card sizes the air duty implied by the dilution — the cost driver (fan energy ∝ volume
× pressure drop) that the level's CO₂-centric numbers hide.

## Predictions

- **P1**: `air_volume_per_ton_co2(420 ppm, eff=1)` ∈ [1.0e6, 1.6e6] m³/ton (≈ 1.31e6).
- **P2**: at 1 Mt/yr → ≥ 1e12 m³ air/yr.
- **P3**: `annual_capacity_ratio(1e6, 4e3)` = 250× exactly (the headline scale-up).
- **P4**: a realistic single-pass efficiency (50%) **doubles** the air volume (∝ 1/efficiency).

## Variables

- `x_co2 = 420e-6` — source: spec.
- `air_density = 1.2 kg/m³`, `M_air = 0.02896 kg/mol` — source: standard ambient.
- `efficiency ∈ {1.0, 0.5}` — source: representative single-pass capture.
- `plant = 1e6 ton/yr`, `climeworks = 4e3 ton/yr` — source: spec / Climeworks Orca ~4 kt/yr.
- output: air volume per ton (eff 1 and 0.5); annual air volume; scale-up ratio.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `air_volume_per_ton_co2`, `annual_capacity_ratio`.
- **run script**: `state/H_013_plant-air-throughput_2026-06-27/run_H_013.py`
- **run cmd**: `python3 state/H_013_plant-air-throughput_2026-06-27/run_H_013.py`
- **artifacts**: `state/H_013_plant-air-throughput_2026-06-27/result.json`

## Criteria

- **C1**: P1–P4 hold → scale-up arithmetic sound, air-handling is the binding duty.
- **verdict_rule**: SUPPORTED = all falsifiers PASS.

## Falsifiers (pre-registered, measurable)

- **F-013-1**: `air_volume_per_ton_co2(420 ppm)` < 1.0e6 or > 1.6e6 m³ (mass balance off).
- **F-013-2**: annual air at 1 Mt/yr < 1e12 m³/yr (throughput not at claimed scale).
- **F-013-3**: `annual_capacity_ratio(1e6, 4e3)` ≠ 250 (headline scale-up arithmetic wrong).
- **F-013-4** (bounds check): `air_volume_per_ton_co2(x=1.0)` raises (pure CO₂ is not "air").
- **F-013-5** (negative control): `air_volume_per_ton_co2(420 ppm, eff=0.5)` = 2× the eff=1 value (1/efficiency scaling).
- **F-013-6**: air volume at flue-gas (12% CO₂) ≥ air volume at 420 ppm (would invert the dilution advantage — flue must need LESS gas handling per ton).

## Honest Limits

- **L1**: this is the *minimum* air volume (100% extraction of the CO₂ present); real contactors
  capture a fraction per pass, so actual air moved is larger — the wall only grows.
- **L2**: the *energy* of moving that air (fan power = volume × pressure drop / efficiency) is not
  computed here; it depends on contactor ΔP and is the actual cost — this card bounds the volume, the precursor.
- **L3**: ignores that the same air carries ~25× more H₂O than CO₂ (humidity load on the sorbent),
  a co-processing burden not in the CO₂-only volume.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `L4.plant`, `flow.capture`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_001 (dilution → floor), H_009 (planetary scale), H_010 (process energy).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**SUPPORTED** — 6/6 falsifiers PASS. Run `2026-06-27`. Verbatim stdout:

```
H_013 — plant air-throughput wall
  air per ton CO2 (420 ppm, eff=1) = 1.306e+06 m3
  air at 1 Mt/yr                   = 1.306e+12 m3/yr
  scale-up 1 Mt/yr vs 4 kt/yr      = 250x Climeworks
  air per ton at 12% flue          = 4.570e+03 m3  (vs 1.31e+06 for air)
  eff=0.5 doubles air              = 2.611e+06 m3
  [PASS] F-013-1
  [PASS] F-013-2
  [PASS] F-013-3
  [PASS] F-013-4
  [PASS] F-013-5
  [PASS] F-013-6
  6/6 falsifiers PASS
VERDICT: SUPPORTED  (250x scale arithmetic sound; air-handling is the binding duty)
```

Artifact: `state/H_013_plant-air-throughput_2026-06-27/result.json`. The 250× scale-up arithmetic
is sound, but the binding duty at DAC dilution is air handling: ~1.31e6 m³/ton → ~1.31e12 m³/yr at
1 Mt/yr. Flue gas (12% CO₂) needs only 4570 m³/ton — **286× less** — quantifying exactly why DAC is
harder than point-source capture. The DAC wall is moving air (fan power ∝ volume), an
infrastructure/investment wall, not a chemistry ceiling (break-walls).
