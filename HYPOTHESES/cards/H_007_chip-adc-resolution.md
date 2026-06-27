---
id: H_007
slug: chip-adc-resolution
title: A 12-bit (σ) ADC cannot deliver ppb-level CO₂ sensing over the ambient full-scale — it is ~7 bits (128×) short; ppb needs ~19 bits or a narrowed span
domain: chip
status: supported
exploration_method: closed-form ADC bit-depth vs resolution-over-span
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_007 — Chip ADC resolution vs ppb sensing

## Hypothesis

L3 HEXA-CHIP claims both an `ADC σ = 12-bit system` and `ppb-level CO₂ sensing`.
These are inconsistent over the ambient full-scale: resolving **1 ppb** of CO₂
across a **420 ppm (= 420 000 ppb)** ambient span needs `log2(420 000) ≈ 18.7`
bits. A 12-bit ADC gives only 4096 levels → a coarsest step of
`420 000 / 4096 ≈ 103 ppb`, **~100× too coarse** for ppb resolution. The claim is
reachable only by *narrowing the span* (zooming around a setpoint) or *adding bits*
— not by the stated 12-bit converter over full ambient range. This card *falsifies
the "12-bit → ppb over ambient full-scale" reading*.

## Why

`L3.chip` is the sensing/control layer feeding L6's ppm setpoint tracking. If the
quantization floor is ~100 ppb, the chip cannot close a ppb-level loop as stated.
Like H_003, this is a numerology-vs-physics check: `σ = 12` is a clean lattice
number, but 12 bits do not buy ppb resolution over a 420 ppm span.

## Predictions

- **P1**: `bits_for_resolution(420 ppm, 1 ppb)` ∈ [18, 19] (≈ 18.7).
- **P2**: deficit vs 12-bit ≥ 6 bits (≥ 64× too few levels).
- **P3**: a 12-bit ADC's coarsest step over 420 ppm full-scale ≥ 50 ppb (≫ 1 ppb).
- **P4**: to actually hit 1 ppb resolution at 12 bits, the span must shrink to
  `4096 × 1 ppb ≈ 4.1 ppm` — a ~100× narrower window than ambient.

## Variables

- `full_scale = 420e-6` (ambient CO₂ mole fraction) — source: spec.
- `resolution = 1e-9` (1 ppb target) — source: spec "ppb-level".
- `bits_adc = 12` (σ) — source: `L3.chip`.
- output: required bits, bit deficit, coarsest step (ppb), 12-bit-feasible span (ppm).

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `bits_for_resolution`.
- **run script**: `state/H_007_chip-adc-resolution_2026-06-27/run_H_007.py`
- **run cmd**: `python3 state/H_007_chip-adc-resolution_2026-06-27/run_H_007.py`
- **artifacts**: `state/H_007_chip-adc-resolution_2026-06-27/result.json`

## Criteria

- **C1**: P1–P4 hold → the 12-bit→ppb-over-ambient claim is refuted.
- **verdict_rule**: SUPPORTED here = "12-bit is insufficient for ppb over ambient" survives
  all falsifiers. A trigger would mean 12 bits actually suffice.

## Falsifiers (pre-registered, measurable)

- **F-007-1**: `bits_for_resolution(420 ppm, 1 ppb)` ≤ 12 (12-bit would then suffice).
- **F-007-2**: bit deficit (required − 12) < 6 (less than 64× short → "close enough").
- **F-007-3**: 12-bit coarsest step over 420 ppm < 50 ppb (fine enough for ppb-ish).
- **F-007-4** (bounds check): `bits_for_resolution(x, x)` ≠ 0 for any x (resolving the full
  scale itself is 0 bits — guards the log).
- **F-007-5** (negative control): `bits_for_resolution(420 ppm, 420 ppm)` = 0 AND
  `bits_for_resolution(420 ppm, 210 ppm)` = 1 (halving the step is exactly 1 bit).
- **F-007-6**: the 12-bit-feasible span for 1 ppb resolution ≥ 420 ppm (would mean 12 bits
  already cover ambient at ppb — refutes the "must narrow span" claim).

## Honest Limits

- **L1**: real CO₂ sensing (NDIR, tunable-laser) does reach ppb — by operating over a
  *narrow* span around a baseline, oversampling/sigma-delta (noise-shaping trades rate for
  bits), or auto-ranging; this card only refutes the literal "12-bit ADC over full ambient".
- **L2**: ignores sensor noise floor, drift, and analog front-end — the ADC bit-depth is a
  *necessary* not *sufficient* condition; real resolution is usually noise-limited first.
- **L3**: "σ = 12-bit" may have been meant as the system/control word width, not the gas ADC
  (the spec also lists `σ−τ = 8-bit gas`) — in which case ppb sensing rests on neither.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `L3.chip`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_003 (same numerology-vs-physics pattern), H_006 (lattice as predictor).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**SUPPORTED** (the "12-bit insufficient for ppb over ambient" claim survives) — 6/6
falsifiers PASS. Run `2026-06-27`. Verbatim stdout:

```
H_007 — 12-bit ADC vs ppb CO2 sensing
  required bits (1 ppb over 420 ppm) = 18.68  (have sigma=12)
  bit deficit                        = 6.68 bits (103x too few levels)
  12-bit coarsest step over ambient  = 102.5 ppb  (target 1 ppb)
  span where 12-bit reaches 1 ppb    = 4.10 ppm  (vs 420 ppm ambient)
  [PASS] F-007-1
  [PASS] F-007-2
  [PASS] F-007-3
  [PASS] F-007-4
  [PASS] F-007-5
  [PASS] F-007-6
  6/6 falsifiers PASS
VERDICT: SUPPORTED  (12-bit insufficient for ppb over ambient span)
```

Artifact: `state/H_007_chip-adc-resolution_2026-06-27/result.json`. A 12-bit ADC quantizes
420 ppm into 103-ppb steps — ~100× too coarse for ppb sensing, ~6.7 bits short of the ~18.7
needed. ppb is reachable only by narrowing the span to ~4 ppm or adding bits (sigma-delta);
the literal `σ = 12-bit over ambient` does not deliver it. Same numerology-vs-physics pattern
as H_003 — feeds H_006's thesis that lattice numbers need a physics check.
