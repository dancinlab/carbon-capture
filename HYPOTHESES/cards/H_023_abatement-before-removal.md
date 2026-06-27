---
id: H_023
slug: abatement-before-removal
title: While the marginal grid plant emits > 0.67 kgCO₂/kWh, a clean kWh AVOIDS more CO₂ displacing fossil generation than it REMOVES via electric DAC — abatement before removal until the grid is clean
domain: system
status: supported
exploration_method: closed-form marginal-electron opportunity-cost crossover
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_023 — Abatement before removal (the marginal-electron test)

## Hypothesis

The deepest answer to "is electric DAC the right path?" is an **opportunity-cost** test on the
scarce resource: a clean kWh. Spend it to **displace** the marginal fossil plant and you AVOID
its intensity `g` kgCO₂. Spend it on **electric DAC** and you REMOVE `1000 / E_dac` kgCO₂
(Gen3: 1000/1500 = 0.667). They tie at the crossover **g\* = 0.667 kgCO₂/kWh**. While the
marginal grid plant is dirtier than g\* (coal ≈ 0.9), the clean kWh **avoids more than it
removes** → **abatement before removal**. Electric DAC becomes the better use of a clean kWh
only once the marginal grid intensity drops below ~0.67 (a gas-or-cleaner grid).

## Why

This is the strongest form of the user's implication: not "DAC is bad" but "on a dirty grid,
the same clean electricity does MORE good decarbonizing the grid than running DAC." It sequences
removal after abatement — and explains why DAC's value rises as the grid cleans (the opposite of
the naive "DAC fixes a dirty grid").

## Predictions

- **P1**: `abatement_crossover_intensity(1500)` = 0.667 kgCO₂/kWh.
- **P2**: at a coal-marginal grid (0.9), displacement avoids > DAC removes → abatement wins (0.9 > 0.667).
- **P3**: at a gas-marginal grid (0.4), DAC removes > displacement avoids → removal wins (0.4 < 0.667).
- **P4**: the crossover rises as DAC energy falls — a 750 kWh/ton next-gen DAC has g\* = 1.33, so it beats displacement on almost any fossil grid (efficiency widens DAC's window).

## Variables

- `E_dac_gen3 = 1500 kWh/ton`, `E_dac_nextgen = 750 kWh/ton` — source: H_018 / projection.
- marginal intensities: `coal = 0.9`, `gas = 0.4` kgCO₂/kWh — source: representative.
- output: crossover g\* for each DAC efficiency; win/lose at coal & gas margins.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `abatement_crossover_intensity`.
- **run script**: `state/H_023_abatement-before-removal_2026-06-27/run_H_023.py`
- **run cmd**: `python3 state/H_023_abatement-before-removal_2026-06-27/run_H_023.py`
- **artifacts**: `state/H_023_abatement-before-removal_2026-06-27/result.json`

## Criteria

- **C1**: P1–P4 hold → abatement-before-removal while the marginal grid > g\*.
- **verdict_rule**: SUPPORTED = all falsifiers PASS.

## Falsifiers (pre-registered, measurable)

- **F-023-1**: `crossover(1500)` ∉ [0.65, 0.68] kgCO₂/kWh (arithmetic of g\* wrong).
- **F-023-2**: at coal margin (0.9), displacement does NOT beat DAC (0.9 ≤ g\* → removal wins on coal).
- **F-023-3**: at gas margin (0.4), DAC does NOT beat displacement (0.4 ≥ g\* → abatement wins on gas).
- **F-023-4** (bounds check): `abatement_crossover_intensity(0)` raises (no zero-energy DAC).
- **F-023-5** (monotonicity): g\* strictly increases as DAC energy falls (efficiency widens DAC's window).
- **F-023-6** (negative control): at a zero-carbon marginal grid (0.0), displacement avoids 0 → DAC always wins (removal is the only lever once the grid is clean).

## Honest Limits

- **L1**: assumes the clean kWh is fungible between "displace fossil" and "run DAC" at the margin — real
  grids have curtailment, transmission, and timing; co-located curtailed renewables can make DAC's effective
  intensity ~0, shifting the calculus (but then displacement is also unavailable, so the trade still holds).
- **L2**: marginal intensities (0.9 coal / 0.4 gas) are representative; the *crossover* g\* = 1000/E_dac is exact,
  the win/lose at a specific grid moves with the real marginal mix.
- **L3**: this is a flow (abatement) vs stock (removal) sequencing argument; permanent removal is still needed
  for legacy CO₂ and hard-to-abate sectors — the claim is "sequence", not "never remove".

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `thesis.energy-floor`, `convergence`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_014 (net-negativity), H_020 (energy FoM), H_021 (portfolio), H_022 (DAC niche).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**🟢 SUPPORTED** — 6/6 falsifiers PASS. Run `2026-06-27`:

```
H_023 — abatement before removal (marginal-electron test)
  crossover g* (Gen3 1500 kWh/ton) = 0.667 kgCO2/kWh
  crossover g* (next-gen 750 kWh)  = 1.333 kgCO2/kWh (efficiency widens DAC's window)
  coal margin 0.9 > g*? True -> displace fossil first
  gas margin 0.4 < g*?  True -> DAC removes more
  clean grid 0.0 < g*?  True -> DAC is the only lever once grid is clean
  6/6 falsifiers PASS
VERDICT: SUPPORTED  (abatement before removal while the marginal grid > 0.67 kgCO2/kWh)
```

Artifact: `state/H_023_abatement-before-removal_2026-06-27/result.json`. The marginal-electron
opportunity cost: a clean kWh AVOIDS the grid's marginal intensity by displacing fossil, or REMOVES
1000/E_dac via DAC. They tie at **g\* = 0.667 kgCO₂/kWh** (Gen3). While the marginal plant is coal
(~0.9 > g\*), the clean kWh does MORE good displacing it than running DAC → **abatement before
removal**. DAC's value RISES as the grid cleans (g\* widens to 1.33 at 750 kWh/ton) — the inverse of
"DAC fixes a dirty grid". Sequencing claim, not "never remove" (legacy + hard-to-abate still need removal).
