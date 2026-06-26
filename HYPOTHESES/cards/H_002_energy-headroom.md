---
id: H_002
slug: energy-headroom
title: Today's DAC capture energy sits ~10× (band 3–30×) above the thermodynamic floor — real headroom exists, but not unlimited
domain: process
status: supported
exploration_method: closed-form (current/floor ratio over a realistic energy band)
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_002 — Energy headroom above the floor

## Hypothesis

The ratio of today's real DAC capture energy to the H_001 floor is a finite,
multi-fold headroom — large enough to be worth chasing, but bounded. Over a
realistic range of current DAC energy (150–400 kJ/mol-equivalent, spanning the
spec's 200 kJ/mol point and the measured Climeworks ~8.8 GJ/ton ≈ 387 kJ/mol),
the headroom is **3×–30×**, with a central estimate near **10×** (the spec's
`σ−φ = 10`). It is neither <3× (no room) nor >50× (implausible).

## Why

`thesis.cost-floor` and `L1.process` hinge on headroom: the claim "capture energy
is an engineering problem, not a ceiling" is only true if real rigs sit well above
the floor. This card bounds *how much* room — separating "10× is real" from
"10× is exactly right" (the latter is numerology, deferred to H_006).

## Predictions

- **P1**: `headroom(200 kJ/mol)` ∈ [9, 12] (spec point ≈ σ−φ = 10).
- **P2**: `headroom(387 kJ/mol)` (Climeworks 8.8 GJ/ton) ≤ 30.
- **P3**: `headroom(150 kJ/mol)` (optimistic next-gen) ≥ 3 — still meaningful room.
- **P4**: the floor used is H_001's value (≈19.3 kJ/mol), not a re-fit number.

## Variables

- `floor = min_separation_work(420e-6, 298.15)/1000` ≈ 19.275 kJ/mol — from H_001.
- `E_spec = 200` kJ/mol — source: spec point estimate.
- `E_climeworks = 8.8 GJ/ton → 8.8e9 / (1e6/44.009) = 387.3` kJ/mol — source: Climeworks
  disclosed ~2000 kWh-th + ~650 kWh-e per ton ≈ 8–10 GJ/ton, representative.
- `E_optimistic = 150` kJ/mol — source: next-gen solid-sorbent projections, representative.
- output: `headroom = E / floor` for each E.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `min_separation_work`, `energy_headroom`.
- **run script**: `state/H_002_energy-headroom_2026-06-27/run_H_002.py`
- **run cmd**: `python3 state/H_002_energy-headroom_2026-06-27/run_H_002.py`
- **artifacts**: `state/H_002_energy-headroom_2026-06-27/result.json`

## Criteria

- **C1**: P1–P4 all hold.
- **verdict_rule**: SUPPORTED = all falsifiers PASS; FALSIFIED = any trigger.

## Falsifiers (pre-registered, measurable)

- **F-002-1**: `headroom(200)` < 9 or > 12 (spec point not ≈10×).
- **F-002-2**: `headroom(387)` > 30 (even the worst real rig should be < 30× the floor).
- **F-002-3**: `headroom(150)` < 3 (optimistic case leaves <3× room → thesis weak).
- **F-002-4** (bounds check): any `headroom < 1` (current energy below the reversible floor — impossible, would mean the floor is wrong or 2nd law violated).
- **F-002-5** (negative control): `headroom` computed with `E = floor` is not exactly 1.0 (the ratio must be self-consistent at the floor).
- **F-002-6**: the floor used diverges from H_001 (`|floor − 19.275| > 0.05` kJ/mol) — guards against re-fitting a convenient floor.

## Honest Limits

- **L1**: "current DAC energy" is a moving, plant-specific figure; the 150–400 kJ/mol band
  is representative, not a single measured value — headroom is reported as a range.
- **L2**: thermal vs electrical energy are conflated into one kJ/mol-equivalent; exergy
  weighting (low-grade heat is cheaper) would lower the *effective* headroom.
- **L3**: the floor is the reversible bound; a real process can never reach 1× — practical
  floors (finite-rate, finite-area) sit ~2–4× above reversible, shrinking usable headroom.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `thesis.cost-floor`, `L1.process`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_001 (the floor), H_004 (cost analogue), H_006 (is "10 = σ−φ" predictive?).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**SUPPORTED** — 6/6 falsifiers PASS. Run `2026-06-27`. Verbatim stdout:

```
H_002 — energy headroom above the floor
  floor                 = 19.275 kJ/mol
  headroom(200 spec)    = 10.38x   (target sigma-phi = 10)
  headroom(8.8 GJ/ton)  = 20.09x   (E=387.3 kJ/mol)
  headroom(150 next-gen)= 7.78x
  headroom(at floor)    = 1.0000x
  [PASS] F-002-1
  [PASS] F-002-2
  [PASS] F-002-3
  [PASS] F-002-4
  [PASS] F-002-5
  [PASS] F-002-6
  6/6 falsifiers PASS
VERDICT: SUPPORTED
```

Artifact: `state/H_002_energy-headroom_2026-06-27/result.json`. Headroom is real and finite:
~10× at the spec point, up to ~20× for a measured Climeworks rig, ≥7.8× even on an
optimistic next-gen figure — all inside the pre-registered 3–30× band, none below 1× (no
2nd-law violation). The "exactly 10× = σ−φ" reading is numerology, audited in H_006.
