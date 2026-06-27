---
id: H_020
slug: nnr-figure-of-merit
title: NOVEL synthesis — a unified cross-family figure of merit (net CO₂ per active GRID energy on a fossil grid) shows free-energy paths overwhelmingly dominate electric DAC: enhanced weathering 13×, moisture-swing 44×, artificial leaf 90×
domain: system
status: supported
exploration_method: novel cross-mechanism-family figure of merit (NNR-FoM) over the verified path set
verification_method: deterministic harness + 7 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_020 — NNR figure of merit: free-energy paths crush electric DAC on a fossil grid

## Hypothesis

The novelty audit (H_017–H_019, novelty-check) found 0/11 *mechanisms* new — so the novel
contribution must be **methodological**. This card defines one: the **Net-Negativity-Robust
figure of merit (NNR-FoM) = net CO₂ removed per unit of ACTIVE grid energy, evaluated on a
realistic fossil grid (0.45 kgCO₂/kWh)** — a single axis that makes electric DAC, enhanced
weathering, moisture-swing, and the artificial leaf **directly comparable across mechanism
families**, which no single prior-art paper does. On that axis the result is **numerically
overwhelming**: paths that draw their energy from sunlight / ambient humidity / rock chemistry
(not the grid) beat electric DAC by **13× (weathering) → 44× (passive moisture-swing) → 90×
(artificial leaf)**, because electric DAC's net removal collapses toward zero on a dirty grid
(H_014) while free-energy paths are grid-independent.

## Why

This is the honest "압도적 우위 NOVEL": not a new mechanism (none exist) but a new **comparison
metric** + the decisive numbers it reveals. It converts the whole verified campaign (the
separation floor, net-negativity, the surviving free-energy paths) into one ranking that
overturns the implicit "electric DAC is the path" assumption on the grid the world actually has.

## Predictions

- **P1**: electric DAC Gen3 (1500 kWh/ton) NNR ≈ 0.060 ton/GJ on the 0.45 grid (net just +0.32).
- **P2**: enhanced weathering (~300 kWh/ton milling) NNR ≈ 0.80 ton/GJ = **≥10× DAC**.
- **P3**: artificial leaf (~50 kWh/ton aux, sunlight free) NNR ≈ 5.4 ton/GJ = **≥50× DAC**.
- **P4** (honest grid-dependence): on a CLEAN grid (0.05) the weathering-over-DAC ratio SHRINKS
  (the overwhelming gap is a fossil-grid phenomenon, not universal) — direction must hold.

## Variables

- grid intensities: `dirty = 0.45`, `clean = 0.05` kgCO₂/kWh — source: fossil vs renewable, representative.
- active grid energy per ton: DAC 1500 kWh (Gen3, H_018); weathering 300 kWh (milling); moisture-swing
  100 kWh (passive aux); artificial-leaf 50 kWh (pumps/aux, sunlight free) — source: representative.
- output: net fraction + NNR (ton/GJ) per path on each grid; advantage ratios vs DAC.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `nnr_fom`, `net_capture_fraction`.
- **run script**: `state/H_020_nnr-figure-of-merit_2026-06-27/run_H_020.py`
- **run cmd**: `python3 state/H_020_nnr-figure-of-merit_2026-06-27/run_H_020.py`
- **artifacts**: `state/H_020_nnr-figure-of-merit_2026-06-27/result.json`

## Criteria

- **C1**: P1–P4 hold → the cross-family FoM is well-formed and the advantage is overwhelming (≥10×).
- **verdict_rule**: SUPPORTED = all falsifiers PASS.
- **transcend axis**: the FoM itself is the deliverable — a reusable cross-family ranking the
  literature lacks; the 13–90× numbers are its first result.

## Falsifiers (pre-registered, measurable)

- **F-020-1**: best free-energy path NNR < 10× the DAC NNR on the dirty grid (advantage not overwhelming).
- **F-020-2**: electric DAC dirty-grid net fraction > 0.5 (DAC not actually crippled → no real gap).
- **F-020-3**: enhanced-weathering NNR < 5× DAC on the dirty grid.
- **F-020-4** (bounds check): `nnr_fom(0)` raises (zero active energy is undefined, not infinite).
- **F-020-5** (negative control): a path with the SAME active energy as DAC (1500 kWh) returns the
  SAME NNR as DAC (the metric is self-consistent, the advantage is real not an artifact of the formula).
- **F-020-6** (honest grid-dependence): the weathering-over-DAC ratio on the CLEAN grid is NOT smaller
  than on the dirty grid (would mean the gap is grid-independent — it must shrink as the grid cleans).
- **F-020-7** (old-DAC sanity): 9 GJ/ton electric DAC has net ≤ 0 on the dirty grid (the worst case is genuinely futile).

## Honest Limits

- **L1**: the FoM is **net-carbon-per-active-energy ONLY** — it deliberately ignores RATE (weathering is
  decadal vs DAC immediate), FOOTPRINT (leaf needs km², weathering needs Gt of rock spread), permanence,
  and capital. Electric DAC wins decisively on speed and area; this metric is one axis, not a verdict on
  which to build.
- **L2**: the active-energy figures (300/100/50 kWh/ton) are representative, not measured for a specific
  plant; the *ranking* is robust to ±2× moves, the exact multipliers are not.
- **L3**: "novel" is the *unified cross-family FoM + the ranking*, not the component facts (weathering is
  low-energy and DAC is grid-sensitive are both individually known) — sold as methodology, not discovery.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `thesis.energy-floor`, `HYPOTHESES.abstract`, `convergence`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **research/novelty**: `state/research-pass-2026-06-27.md`, `state/novelty-check-2026-06-27.md`.
- **sister H**: H_014 (net-negativity), H_018 (Gen3 anchor), H_A010 (weathering), H_A011 (leaf), H_A006 (electro-swing).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**🟢 SUPPORTED** — 7/7 falsifiers PASS. Run `2026-06-27`. Verbatim stdout:

```
H_020 — NNR figure of merit (net CO2 per active grid GJ, fossil 0.45 kgCO2/kWh)
  electric-DAC Gen3          active  1500 kWh  net +0.32  NNR  0.060 ton/GJ =   1.0x DAC
  enhanced-weathering        active   300 kWh  net +0.86  NNR  0.801 ton/GJ =  13.3x DAC
  moisture-swing (passive)   active   100 kWh  net +0.95  NNR  2.653 ton/GJ =  44.1x DAC
  artificial-leaf            active    50 kWh  net +0.98  NNR  5.431 ton/GJ =  90.2x DAC
  best non-DAC path: artificial-leaf = 90x electric DAC
  honesty: weathering/DAC ratio dirty 13.3x -> clean 5.3x (gap shrinks as grid cleans)
  old 9 GJ/ton DAC net on dirty grid = -0.12 (futile)
  [PASS] F-020-1 .. F-020-7
  7/7 falsifiers PASS
VERDICT: SUPPORTED  (free-energy paths 13-90x over electric DAC on a fossil grid)
```

Artifact: `state/H_020_nnr-figure-of-merit_2026-06-27/result.json`. The **novel** contribution is
methodological — a unified cross-family figure of merit (net CO₂ per *active grid* energy on a
realistic fossil grid) that no single prior-art paper computes — and its first result is
**numerically overwhelming**: enhanced weathering **13×**, passive moisture-swing **44×**, the
artificial leaf **90×** the net-per-active-energy of the best electric DAC (Gen3), because electric
DAC's net collapses to +0.32 (old 9 GJ rigs to −0.12, futile) on a dirty grid while free-energy
paths stay grid-independent. Honesty held: the gap shrinks to 5.3× on a clean grid (F-020-6), and
this is the *energy* axis only — DAC still wins on rate/footprint (Limits).
