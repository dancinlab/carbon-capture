---
id: H_001
slug: separation-floor
title: DAC thermodynamic separation floor W_min = RT·ln(1/x) is ~19–20 kJ/mol at 420 ppm/298 K, monotone-rising as air gets more dilute
domain: process
status: supported
exploration_method: closed-form (Sherwood / reversible separation work)
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_001 — DAC separation thermodynamic floor

## Hypothesis

The minimum reversible work to pull one mole of CO₂ out of a dilute mixture is
`W_min = R·T·ln(1/x_CO2)`. Evaluated at ambient air (`x = 420 ppm`, `T = 298.15 K`)
this is a hard lower bound near **19–20 kJ/mol** — independent of sorbent
chemistry. The bound rises as the source gets more dilute (lower x) and collapses
toward 0 as the source approaches pure CO₂.

## Why

This is the `thesis.energy-floor` node in `ARCHITECTURE.json` (`W_min ≈ J₂−τ = 20`).
It is the physical anchor of the whole HEXA-CCUS cost argument: if the floor were
itself ~200 kJ/mol there would be no headroom. L1.process targets 20 kJ/mol; this
card tests whether 20 is actually the floor (not the achieved value — that is H_002).

## Predictions

- **P1**: `W_min(420 ppm, 298.15 K)` ∈ [19, 20] kJ/mol.
- **P2**: `W_min` strictly increases as `x_CO2` decreases (more dilute = more work).
- **P3**: `W_min(12 % flue gas)` ≤ 6 kJ/mol (≈ ¼ of the air floor — flue is easier).
- **P4**: as `x → 1` (pure CO₂), `W_min → 0`.

## Variables

- `x_air = 420e-6` (ambient CO₂ mole fraction, current ~422 ppm) — source: spec.
- `x_flue = 0.12` (typical coal flue gas) — source: separations literature, representative.
- `T = 298.15 K` (ambient) — source: standard.
- output: `W_min` (kJ/mol) at each x; sign of finite-difference dW/dx.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `min_separation_work`.
- **run script**: `state/H_001_separation-floor_2026-06-27/run_H_001.py`
- **deterministic**: stdlib only, no randomness, $0 local.
- **run cmd**: `python3 state/H_001_separation-floor_2026-06-27/run_H_001.py`
- **artifacts**: `state/H_001_separation-floor_2026-06-27/result.json`

## Criteria

- **C1**: all of P1–P4 hold within stated bounds.
- **verdict_rule**: SUPPORTED = all falsifiers PASS; FALSIFIED = any trigger.

## Falsifiers (pre-registered, measurable)

- **F-001-1**: `W_min(420 ppm)` > 20.0 kJ/mol (floor higher than the J₂−τ target).
- **F-001-2**: `W_min(420 ppm)` < 19.0 kJ/mol (floor lower than claimed — over-optimistic).
- **F-001-3**: monotonicity broken — `W_min` not strictly increasing as x falls across a 5-point sweep.
- **F-001-4**: `W_min(12 % flue)` > 6 kJ/mol (flue not meaningfully easier than air).
- **F-001-5** (bounds check): `W_min(x=0.99)` > 0.1 kJ/mol (near-pure source should cost ~0).
- **F-001-6** (negative control): `W_min(x = 420 ppm)` does NOT exceed `W_min(x = 0.12)` (a dilute source must cost MORE than a concentrated one; if not, the relation is mis-signed).

## Honest Limits

- **L1**: reversible (Carnot-equivalent) floor — real processes are irreversible, so the
  achieved value (H_002) is always above this; this card bounds only the floor itself.
- **L2**: ignores co-adsorbed H₂O, kinetics, heat of adsorption, and recompression of the
  product stream — all push real energy up but cannot lower the floor.
- **L3**: the "≈ J₂−τ = 20" identity is a numerical coincidence at one (x,T) point, tested
  separately as a predictor in H_006 — this card only checks the physics, not the numerology.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `thesis.energy-floor`, `L1.process`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_002 (headroom above this floor), H_006 (is "20 = J₂−τ" predictive?).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**SUPPORTED** — 6/6 falsifiers PASS. Run `2026-06-27`. Verbatim stdout:

```
H_001 — DAC separation floor
  floor(420 ppm, 298 K) = 19.275 kJ/mol   (target J2-tau = 20)
  floor(12% flue)       = 5.256 kJ/mol
  floor(x=0.99)         = 0.0249 kJ/mol
  W_min strictly rising as x falls: True
  sweep [1.718, 5.256, 7.979, 13.687, 19.275] kJ/mol over x=[0.5, 0.12, 0.04, 0.004, 0.00042]
  [PASS] F-001-1
  [PASS] F-001-2
  [PASS] F-001-3
  [PASS] F-001-4
  [PASS] F-001-5
  [PASS] F-001-6
  6/6 falsifiers PASS
VERDICT: SUPPORTED
```

Artifact: `state/H_001_separation-floor_2026-06-27/result.json`. The floor is 19.275 kJ/mol
(within [19,20]), strictly rises as x falls, flue is ~3.7× easier, and a near-pure source
costs ~0 — the physics holds. (The "≈ J₂−τ = 20" identity itself is audited in H_006.)
