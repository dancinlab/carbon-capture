---
id: H_010
slug: tsa-regeneration-heat
title: TSA regeneration sensible heat (~100 kJ/mol at cp=1·ΔT=100·wc=1) dominates the 20 kJ/mol separation floor and scales as 1/working-capacity — the mechanism behind the 10× headroom
domain: process
status: supported
exploration_method: closed-form sensible-heat balance (cp·ΔT / working-capacity)
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_010 — TSA regeneration sensible-heat penalty

## Hypothesis

The reason real TSA capture (H_002) sits ~10× above the separation floor is **not**
the separation work — it is the **sensible heat to swing the sorbent's temperature**.
Per mole of CO₂ cycled, `q = cp·ΔT / working_capacity`. At representative
`cp = 1 kJ/kg/K`, `ΔT = 100 K`, `working_capacity = 1 mol/kg`, that is **~100 kJ/mol**
— 5× the 19.3 kJ/mol floor, on top of it, and **independent of W_min**. It scales as
`1/working_capacity`, which is exactly why higher working capacity (the *direction*
H_003 endorsed, even though 48 mmol/g is unreachable) is the lever.

## Why

`L1.process` is the named bottleneck. H_002 measured the ~10× headroom; this card
gives its **mechanism**: sensible heat. That makes the headroom *attackable* (raise
working capacity, recover heat, lower ΔT) rather than mysterious — break-walls:
classify the wall as investment/engineering, not a thermodynamic ceiling.

## Predictions

- **P1**: `q(cp=1, ΔT=100, wc=1)` ≈ 100 kJ/mol, > 4× the 19.3 kJ/mol floor.
- **P2**: `q` strictly decreases as working capacity rises (1/wc scaling).
- **P3**: a poor sorbent (`wc = 0.5`) gives `q ≥ 150 kJ/mol` — approaching the ~200 kJ/mol real figure.
- **P4**: even a good sorbent (`wc = 2`) gives `q = 50 kJ/mol` — still > the floor, so regeneration stays the dominant term before heat recovery.

## Variables

- `cp = 1.0 kJ/kg/K` (sorbent + bound CO₂ heat capacity) — source: solid-sorbent literature, representative.
- `ΔT = 100 K` (swing 25 → 125 °C) — source: TSA practice, representative.
- `wc ∈ {0.5, 1, 2} mol/kg` (working capacity sweep) — source: DAC sorbent range, representative.
- `floor = 19.275 kJ/mol` — from H_001.
- output: `q` at each wc; monotonicity; ratio to floor.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `regeneration_sensible_heat`, `min_separation_work`.
- **run script**: `state/H_010_tsa-regeneration-heat_2026-06-27/run_H_010.py`
- **run cmd**: `python3 state/H_010_tsa-regeneration-heat_2026-06-27/run_H_010.py`
- **artifacts**: `state/H_010_tsa-regeneration-heat_2026-06-27/result.json`

## Criteria

- **C1**: P1–P4 hold → sensible heat is the dominant, working-capacity-driven term.
- **verdict_rule**: SUPPORTED = all falsifiers PASS.

## Falsifiers (pre-registered, measurable)

- **F-010-1**: `q(1,100,1)` ≤ the floor (19.275) — regeneration would then be negligible.
- **F-010-2**: `q` not strictly decreasing across wc = 0.5 → 1 → 2 (breaks 1/wc scaling).
- **F-010-3**: `q(1,100,0.5)` < 100 kJ/mol (poor-sorbent penalty not large).
- **F-010-4** (bounds check): `regeneration_sensible_heat(1,100,0)` raises (no divide-by-zero).
- **F-010-5** (negative control): linear in ΔT — `q(1,200,1) = 2·q(1,100,1)`.
- **F-010-6**: `q(1,100,2)` ≤ the floor (a good sorbent would make regeneration sub-floor → mechanism not dominant).

## Honest Limits

- **L1**: this is the raw sensible heat with NO heat recovery; real TSA recovers 50–80 % via
  heat integration, so the *net* penalty is lower — but even 30 % of 100 kJ/mol exceeds the floor.
- **L2**: ignores the heat of adsorption (a second, comparable term ~ the binding energy of H_012)
  and steam/purge energy — both add to, never subtract from, the regeneration cost.
- **L3**: `cp`, `ΔT`, `wc` are representative; the *conclusion* (sensible heat dominates, ∝ 1/wc)
  is robust across the plausible ranges, only the exact kJ/mol moves.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `L1.process`, `thesis.energy-floor`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_002 (the headroom this explains), H_003 (working-capacity direction), H_012 (binding-energy term).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**SUPPORTED** — 6/6 falsifiers PASS. Run `2026-06-27`. Verbatim stdout:

```
H_010 — TSA regeneration sensible-heat penalty
  separation floor          = 19.27 kJ/mol
  q (cp=1,dT=100,wc=1)      = 100.0 kJ/mol  (5.2x the floor)
  q (wc=0.5 poor sorbent)   = 200.0 kJ/mol  (~real ~200 regime)
  q (wc=2 good sorbent)     = 50.0 kJ/mol  (still > floor)
  monotone decreasing in wc : True
  [PASS] F-010-1
  [PASS] F-010-2
  [PASS] F-010-3
  [PASS] F-010-4
  [PASS] F-010-5
  [PASS] F-010-6
  6/6 falsifiers PASS
VERDICT: SUPPORTED  (sensible heat dominates; lever = working capacity + heat recovery)
```

Artifact: `state/H_010_tsa-regeneration-heat_2026-06-27/result.json`. The mechanism behind the
H_002 ~10× headroom is sensible heat: ~100 kJ/mol at typical params (5.2× the floor), and at a
poor sorbent (wc=0.5) it hits **exactly the ~200 kJ/mol** real-amine figure. It scales as
1/working-capacity, so the levers are higher working capacity (H_003's direction) and heat
recovery — an engineering wall, not a thermodynamic ceiling (break-walls).
