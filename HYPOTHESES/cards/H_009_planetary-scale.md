---
id: H_009
slug: planetary-scale
title: The 100 Gt/yr removal rate is mass-consistent with 420→280 ppm in 12 yr, but ignores ocean re-equilibration (~2× more) and at real DAC energy needs ~900 EJ/yr > all human primary energy — PARTIAL
domain: system
status: partial
exploration_method: closed-form atmospheric mass balance + energy-at-scale
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_009 — Planetary-scale removal: mass vs energy

## Hypothesis

L6 HEXA-UNIVERSAL claims `420 → 280 ppm in σ = 12 years` at `100 Gt CO₂/yr`.
Two closed-form checks:

1. **Mass balance (holds)** — drawing down 140 ppm removes `140 × 7.82 = 1095 Gt
   CO₂`; over 12 years that is `91 Gt/yr`, consistent with the stated ~100 Gt/yr.
   The arithmetic is internally coherent.
2. **Two walls (break the literal claim)** —
   (a) *Ocean re-equilibration*: the ocean holds ~50× the atmosphere's CO₂; as air
       CO₂ falls, the ocean out-gasses to re-equilibrate, so net removal needs
       **roughly 2× the gross atmospheric figure** → ~180 Gt/yr, not 100.
   (b) *Energy*: 100 Gt/yr at real DAC (~9 GJ/ton) is `9e20 J/yr = 900 EJ/yr`,
       **larger than total human primary energy (~600 EJ/yr)**. Even at the H_001
       thermodynamic floor it is ~44 EJ/yr (~7% of global energy).

Net: the rate is mass-coherent but the literal target is **gated on the upstream
efficiency thesis (H_001/H_002)** and under-counts the ocean — **PARTIAL**.

## Why

L6 is the apex claim. It is only meaningful if the mass and energy budgets close.
This card confirms the mass arithmetic (honesty: the spec's numbers are *coherent*,
not nonsense) while exposing the two physical walls — exactly the break-walls
discipline: classify the wall (here: investment/efficiency + an omitted-term
measurement gap), don't rubber-stamp.

## Predictions

- **P1**: `ppm_to_gt_co2(140)` ∈ [1000, 1200] Gt (≈ 1095).
- **P2**: required gross rate `1095/12` ∈ [85, 95] Gt/yr — consistent with the ~100 Gt/yr claim.
- **P3** (energy wall): 100 Gt/yr at 9 GJ/ton ≥ 600 EJ/yr (≥ global primary energy).
- **P4** (ocean wall): net-removal rate accounting for ~2× re-equilibration ≥ 1.5× the stated 100 Gt/yr.

## Variables

- `delta_ppm = 140` (420→280) — source: spec.
- `years = 12` (σ) — source: spec.
- `stated_rate = 100` Gt/yr — source: `L6.universal`.
- `E_dac = 9 GJ/ton` (real DAC) — source: H_002 / Climeworks band, representative.
- `global_primary = 600 EJ/yr` — source: IEA world primary energy, representative.
- `ocean_factor = 2.0` (airborne-fraction re-equilibration) — source: carbon-cycle literature, representative.
- output: gross Gt, gross rate, energy EJ/yr (real & floor), net rate with ocean factor.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `ppm_to_gt_co2`, `min_separation_work`.
- **run script**: `state/H_009_planetary-scale_2026-06-27/run_H_009.py`
- **run cmd**: `python3 state/H_009_planetary-scale_2026-06-27/run_H_009.py`
- **artifacts**: `state/H_009_planetary-scale_2026-06-27/result.json`

## Criteria

- **C1**: P1, P2 hold (mass coherent) AND P3, P4 hold (both walls real) → PARTIAL by construction.
- **verdict_rule**: SUPPORTED only if NO wall triggers (mass coherent AND energy feasible AND ocean
  negligible); FALSIFIED if the mass arithmetic itself collapses; else PARTIAL.

## Falsifiers (pre-registered, measurable)

- **F-009-1** (mass arithmetic): `ppm_to_gt_co2(140)` < 1000 or > 1200 Gt (conversion off).
- **F-009-2** (rate coherence): gross rate `1095/12` outside [80, 100] Gt/yr (claim not mass-coherent).
- **F-009-3** (energy wall, expected to MARK the partial): 100 Gt/yr at 9 GJ/ton < global primary
  (600 EJ/yr) — if energy fit within global supply the energy wall would be absent; it does not.
- **F-009-4** (bounds check): `ppm_to_gt_co2(0)` ≠ 0 (zero drawdown = zero mass).
- **F-009-5** (negative control): `ppm_to_gt_co2` linear — `ppm_to_gt_co2(280) = 2 × ppm_to_gt_co2(140)`.
- **F-009-6** (floor sanity): even at the thermodynamic floor, 100 Gt/yr energy > 10 EJ/yr (the
  scale is non-trivial regardless of efficiency — guards against "floor makes it free").

## Honest Limits

- **L1**: `ocean_factor = 2` is a representative airborne-fraction approximation; the true
  re-equilibration is time-dependent and nonlinear — the "~2× more" is order-of-magnitude.
- **L2**: `9 GJ/ton` real DAC and `600 EJ/yr` global energy are representative external figures;
  the energy wall scales directly with both (a 3 GJ/ton next-gen sorbent would cut it to ~300 EJ/yr,
  still ~50% of global — the wall narrows but does not vanish without the H_001/H_002 gains).
- **L3**: this is a budget check, not a climate model — ignores natural sinks/sources dynamics,
  permanence of storage, and the distinction between flow (emissions) and stock (drawdown).

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `L6.universal`, `thesis.energy-floor`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_001 (floor), H_002 (real energy), H_006 (numerology — σ=12 yr).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**PARTIAL** — 6/6 falsifiers PASS (mass arithmetic coherent), but both physical walls fire,
so by the pre-registered rule it resolves to PARTIAL. Run `2026-06-27`. Verbatim stdout:

```
H_009 — planetary-scale removal: mass vs energy
  140 ppm drawdown     = 1095 Gt CO2  -> /12yr = 91.2 Gt/yr (claim ~100)
  energy @ 9 GJ/ton    = 900 EJ/yr   (global primary ~600 EJ/yr)
  energy @ thermo floor = 43.8 EJ/yr  (~7% of global)
  net rate w/ ocean 2x  = 182 Gt/yr  (vs stated 100)
  energy wall: True   ocean wall: True
  [PASS] F-009-1
  [PASS] F-009-2
  [PASS] F-009-3
  [PASS] F-009-4
  [PASS] F-009-5
  [PASS] F-009-6
  6/6 falsifiers PASS
VERDICT: PARTIAL  (mass coherent; energy + ocean walls gate the literal target)
```

Artifact: `state/H_009_planetary-scale_2026-06-27/result.json`. The mass budget is genuinely
coherent — 140 ppm = 1095 Gt CO₂, /12 yr = 91 Gt/yr, matching the ~100 Gt/yr claim (honesty:
the spec's apex number is not nonsense). But two walls gate the literal target: at real DAC
energy (9 GJ/ton) it needs ~900 EJ/yr, **exceeding all human primary energy (~600 EJ/yr)**, and
ocean re-equilibration (~2×) pushes net removal to ~180 Gt/yr. The target is therefore **gated
on the upstream efficiency thesis (H_001/H_002)** — only near the thermodynamic floor (~44 EJ/yr,
~7% of global) does it enter the realm of feasibility, and even then the ocean term remains.
