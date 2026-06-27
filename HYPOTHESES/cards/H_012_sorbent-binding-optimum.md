---
id: H_012
slug: sorbent-binding-optimum
title: There is a Sabatier-optimal CO₂ binding energy (~45–55 kJ/mol) — weaker (~30) gives ~0 uptake at 400 ppm, stronger (~60+) gives full coverage but the same energy is owed back at regeneration
domain: sorbent
status: supported
exploration_method: closed-form Langmuir coverage vs adsorption energy at DAC partial pressure
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_012 — Sorbent binding-energy optimum (Sabatier)

## Hypothesis

CO₂ capture at the 420 ppm (`4.2e-4 bar`) DAC partial pressure has a **Sabatier
optimum** in adsorption energy. A Langmuir isotherm with Arrhenius affinity gives
fractional coverage θ that is a sigmoid in `E_ads`: too weak (≈30 kJ/mol) → θ ≈ 0
(no uptake at such low partial pressure), too strong (≥60 kJ/mol) → θ ≈ 1 but **that
same E_ads must be repaid to regenerate** (the H_010/heat-of-adsorption term). The
useful window is **~45–55 kJ/mol** — enough coverage without runaway regeneration —
which is exactly why weak physisorbents fail at DAC and strong amines work but cost
energy to strip.

## Why

`L0.sorbent` lists physisorbent MOFs and (implicitly) amine routes. This card gives
the design rule the bare candidate list omits: the binding energy itself is the tuned
quantity, and it trades coverage against regeneration — connecting H_003 (capacity),
H_010 (regeneration heat), and the real ~200 kJ/mol of amine systems.

## Predictions

- **P1**: `θ(E_ads=30, 4.2e-4 bar)` < 0.01 (weak binding → negligible uptake at DAC).
- **P2**: `θ(E_ads=60, 4.2e-4 bar)` > 0.5 (strong binding → high coverage).
- **P3**: θ is monotonically increasing in E_ads across 20→70 kJ/mol (sigmoid, no inversion).
- **P4**: a mid window exists — `θ(50)` ∈ [0.05, 0.95] (partial coverage, the tunable regime).

## Variables

- `partial_pressure = 4.2e-4 bar` (420 ppm) — source: spec.
- `T = 298.15 K`, `pre_exp = 1e-6 bar⁻¹` — source: representative entropic prefactor, documented (not fitted).
- `E_ads ∈ {20,30,40,50,60,70} kJ/mol` (sweep) — source: physisorption→chemisorption range.
- output: θ at each E_ads; monotonicity; window membership.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `langmuir_coverage`.
- **run script**: `state/H_012_sorbent-binding-optimum_2026-06-27/run_H_012.py`
- **run cmd**: `python3 state/H_012_sorbent-binding-optimum_2026-06-27/run_H_012.py`
- **artifacts**: `state/H_012_sorbent-binding-optimum_2026-06-27/result.json`

## Criteria

- **C1**: P1–P4 hold → a Sabatier optimum exists between no-uptake and high-regen.
- **verdict_rule**: SUPPORTED = all falsifiers PASS.

## Falsifiers (pre-registered, measurable)

- **F-012-1**: `θ(30)` ≥ 0.01 (weak binding already gives uptake → no low-end wall).
- **F-012-2**: `θ(60)` ≤ 0.5 (strong binding fails to fill → model broken).
- **F-012-3**: θ not monotonically increasing in E_ads over the sweep (sigmoid violated).
- **F-012-4** (bounds check): every θ ∈ [0, 1) (a coverage fraction, never ≥ 1 or < 0).
- **F-012-5** (negative control): at high partial pressure (1 bar) even weak `θ(30, 1 bar)` ≫ `θ(30, 4.2e-4 bar)` (dilution is what kills the weak sorbent, confirming the mechanism).
- **F-012-6**: `θ(50)` ∉ [0.05, 0.95] (no tunable mid window → no optimum to find).

## Honest Limits

- **L1**: single-site Langmuir with one representative prefactor is a cartoon — real isotherms
  (Toth, dual-site, cooperative amine step-isotherms) shift the exact window, but the *existence*
  of a coverage-vs-regeneration optimum is robust.
- **L2**: equates E_ads with the full regeneration energy; real regeneration also carries the
  sensible heat of H_010 and is partly recoverable — so the "owed back" term is a floor, not the total.
- **L3**: ignores kinetics, humidity competition (H₂O often out-competes CO₂ on physisorbents),
  and degradation of strong chemisorbents — all narrow the usable window further.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `L0.sorbent`, `L0.candidates`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_003 (capacity), H_010 (regeneration heat), H_002 (energy headroom).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**SUPPORTED** — 6/6 falsifiers PASS. Run `2026-06-27`. Verbatim stdout:

```
H_012 — Sabatier-optimal CO2 binding energy at 400 ppm
  E_ads = 20 kJ/mol -> theta = 0.0000
  E_ads = 30 kJ/mol -> theta = 0.0001
  E_ads = 40 kJ/mol -> theta = 0.0043
  E_ads = 50 kJ/mol -> theta = 0.1945
  E_ads = 60 kJ/mol -> theta = 0.9317
  E_ads = 70 kJ/mol -> theta = 0.9987
  monotone increasing: True   all theta in [0,1): True
  weak sorbent rescue by pressure: theta(30,DAC)=7.568e-05 -> theta(30,1bar)=0.1527
  [PASS] F-012-1
  [PASS] F-012-2
  [PASS] F-012-3
  [PASS] F-012-4
  [PASS] F-012-5
  [PASS] F-012-6
  6/6 falsifiers PASS
VERDICT: SUPPORTED  (binding-energy optimum ~45-55 kJ/mol: coverage vs regeneration)
```

Artifact: `state/H_012_sorbent-binding-optimum_2026-06-27/result.json`. The coverage sigmoid at
400 ppm puts the usable window at ~50 kJ/mol: E_ads=40 gives θ≈0.004 (weak physisorbent — fails
at DAC dilution), E_ads=60 gives θ≈0.93 (strong/amine — but owes 60 kJ/mol back at regeneration,
the H_010 term). The same weak sorbent is rescued at 1 bar (θ 7.6e-5 → 0.15), confirming dilution
is what kills it. This is the design rule the bare candidate list omits — links H_003/H_010/H_002.
