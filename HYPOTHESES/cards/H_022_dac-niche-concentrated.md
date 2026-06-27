---
id: H_022
slug: dac-niche-concentrated
title: Electric capture is not the WRONG technology, it is mis-TARGETED — on concentrated sources (flue, 12% CO₂) it needs 286× less air and a 3.7× lower floor than dilute air, so point-source = electric, dilute air = free-energy
domain: system
status: supported
exploration_method: closed-form flue-vs-air separation floor + air-throughput ratio
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_022 — Electric capture's right niche is concentrated CO₂

## Hypothesis

"Is electric DAC the right path?" splits by **target**, not technology. Electric (TSA/PSA/
electro-swing) capture from a **concentrated source** — flue gas (12% CO₂), cement, steel —
needs **286× less air handling** (H_013) and sits on a **3.7× lower separation floor**
(5.26 vs 19.3 kJ/mol, H_001) than dilute 420-ppm air. So electric capture is the *right* path
for **point sources**, and the H_020 free-energy advantage applies to **dilute air on a fossil
grid**. The honest reframe: electric capture isn't the wrong technology, it's mis-targeted when
pointed at dilute air on a dirty grid.

## Why

Prevents the over-correction "electric capture is dead." It is excellent where CO₂ is already
concentrated (point-source abatement); the air-handling (H_013) and dilution (H_016) walls only
bite at 420 ppm. Maps technology to target.

## Predictions

- **P1**: `air_volume_per_ton(420 ppm) / air_volume_per_ton(12%)` ≈ 286× (the dilution penalty).
- **P2**: `floor(420 ppm) / floor(12%)` ≈ 3.7× (concentrated is thermodynamically cheaper).
- **P3**: flue floor ≤ 6 kJ/mol (point-source separation is near the cheap end).
- **P4**: the dilution penalty (air ratio) is ≫ the floor ratio — i.e. air HANDLING, not separation work, is what makes dilute DAC hard.

## Variables

- `x_air = 420e-6`, `x_flue = 0.12` — source: spec / flue gas.
- output: air-volume ratio, floor ratio, flue floor.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `air_volume_per_ton_co2`, `min_separation_work`.
- **run script**: `state/H_022_dac-niche-concentrated_2026-06-27/run_H_022.py`
- **run cmd**: `python3 state/H_022_dac-niche-concentrated_2026-06-27/run_H_022.py`
- **artifacts**: `state/H_022_dac-niche-concentrated_2026-06-27/result.json`

## Criteria

- **C1**: P1–P4 hold → electric capture belongs on concentrated sources, free-energy on dilute air.
- **verdict_rule**: SUPPORTED = all falsifiers PASS.

## Falsifiers (pre-registered, measurable)

- **F-022-1**: air-volume ratio (air/flue) < 100× (dilution penalty not large → DAC not specially hard).
- **F-022-2**: floor ratio (air/flue) < 2× (concentrated not thermodynamically cheaper).
- **F-022-3**: flue floor > 6 kJ/mol (point-source not near the cheap end).
- **F-022-4** (bounds check): `air_volume_per_ton_co2(0.99)` ≤ `air_volume_per_ton_co2(0.12)` (purer → even less air).
- **F-022-5** (negative control): `air_volume_per_ton(x) → ` larger as x falls (monotone dilution penalty across 0.12 → 0.01 → 420 ppm).
- **F-022-6**: the air ratio is NOT ≫ the floor ratio (would mean separation work, not air handling, is the dilute-DAC wall).

## Honest Limits

- **L1**: point-source capture has its own real costs (solvent regeneration, plant retrofit, SOx/NOx) not
  modelled — "286× less air" bounds the *air-handling* term only, the strongest dilute-DAC penalty.
- **L2**: point sources are finite and themselves should be phased out (abatement, H_023); DAC/dilute is
  needed for legacy + hard-to-abate + net-negative — so this is a sequencing point, not "never do dilute".
- **L3**: ratios use the H_001 reversible floor and H_013 ideal air volume; real multipliers differ but the
  286× / 3.7× ORDER is robust.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `L1.process`, `L4.plant`, `thesis`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_013 (air wall), H_001 (floor), H_016 (dilution), H_020 (energy FoM), H_023 (abatement-first).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**🟢 SUPPORTED** — 6/6 falsifiers PASS. Run `2026-06-27`:

```
H_022 — electric capture's niche is concentrated CO2
  air volume penalty (420 ppm / 12% flue) = 286x less air for flue
  separation floor (air 19.27 / flue 5.26 kJ/mol) = 3.7x lower for flue
  air ratio (286x) >> floor ratio (3.7x) -> air HANDLING is the dilute-DAC wall
  6/6 falsifiers PASS
VERDICT: SUPPORTED  (point-source = electric; dilute air on a fossil grid = free-energy)
```

Artifact: `state/H_022_dac-niche-concentrated_2026-06-27/result.json`. Electric capture is
mis-TARGETED, not wrong-tech: on a concentrated source (flue, 12% CO₂) it needs 286× less air
(H_013) and a 3.7× lower floor (H_001) than dilute air — and the air ratio (286×) ≫ the floor
ratio (3.7×) confirms **air HANDLING, not separation work, is the dilute-DAC wall**. Map tech to
target: point-source → electric; dilute air on a fossil grid → free-energy (H_020).
