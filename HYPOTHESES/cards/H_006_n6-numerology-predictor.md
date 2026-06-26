---
id: H_006
slug: n6-numerology-predictor
title: The n=6 lattice (φ=2·τ=4·σ=12·J₂=24) is a post-hoc label, not a predictor — it attaches clean identities to physically-impossible targets as readily as to real ones (FALSIFIED as predictor)
domain: system
status: supported
exploration_method: meta — plausibility audit of the lattice→target identities (oracle = H_001..H_005)
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_006 — Is the n=6 lattice a predictor? (negative control)

## Hypothesis

The HEXA-CCUS spec derives engineering targets from a fixed integer lattice
(`φ=2, τ=4, σ=12, J₂=24`) via clean identities (20 = J₂−τ, 10 = σ−φ, 48 = J₂·φ,
24 = J₂, …). **Claim under test: that lattice has predictive power — its targets
land on physically reachable values more often than an indiscriminate labeling
would.** Prediction of THIS card (the skeptic's null): it does **not**. The lattice
attaches equally clean identities to targets that the physics-grounded sister cards
(H_001–H_005) found **impossible** (48 mmol/g) or **below credible floors**
($24/ton) as to ones it found real (20 kJ/mol, 10× headroom, hexagon). A scheme
that fits both the possible and the impossible has **zero filtering power** → it is
decorative, not predictive → the "lattice predicts targets" claim is **FALSIFIED**.

## Why

This is the honesty keystone of the whole verification effort. HEXA-CCUS leans on
n=6 numerology throughout `ARCHITECTURE.json`. If even one card (H_005) confirms a
lattice number, a reader might over-credit the lattice. This card forces the
question every other card defers: does `= J₂·φ` *explain* a target, or merely
*relabel* it after the fact? The negative control is the structure of the lattice
itself — any small target integer is reachable as a sum/product/difference of
{2,4,12,24}, so "it matches" is unsurprising and non-falsifiable on its own.

## Predictions

- **P1**: of the 6 audited lattice→target identities, **≥ 2 map to physically
  implausible targets** (per H_001–H_005 verdicts) → filtering power lost.
- **P2**: the *fraction implausible* ≥ 1/3 (a predictor worth the name would be ~0).
- **P3**: the two strongest *real* results (H_001 floor ≈20, H_005 hexagon) hold
  **independently of the lattice** — their physics is derived without {2,4,12,24},
  so the lattice adds no information even where it "agrees."
- **P4**: at least one identity (48 = J₂·φ) is *exactly* lattice-clean yet *maximally*
  unphysical (H_003) — the cleanliness of the identity is uncorrelated with truth.

## Variables

- audit table (identity → spec target → physical verdict from sister card):
  1. `J₂−τ = 20` kJ/mol floor → H_001 → PLAUSIBLE
  2. `σ−φ = 10×` headroom → H_002 → PLAUSIBLE
  3. `J₂·φ = 48` mmol/g capacity → H_003 → IMPLAUSIBLE
  4. `J₂ = 24` $/ton cost → H_004 → IMPLAUSIBLE (below credible floor)
  5. `n=6` hexagon reactor → H_005 → PLAUSIBLE (but lattice-independent math)
  6. `J₂ = 24×` capacity ratio (48/2 mmol/g) → derived from #3 → IMPLAUSIBLE
- output: count PLAUSIBLE / IMPLAUSIBLE; fraction implausible; predictor verdict.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — re-derives floor (H_001) & mass fraction (H_003)
  to anchor the audit numerically; the plausibility flags are the *pre-registered* verdicts
  of the sister cards, not free parameters.
- **run script**: `state/H_006_n6-numerology-predictor_2026-06-27/run_H_006.py`
- **run cmd**: `python3 state/H_006_n6-numerology-predictor_2026-06-27/run_H_006.py`
- **artifacts**: `state/H_006_n6-numerology-predictor_2026-06-27/result.json`

## Criteria

- **C1**: fraction implausible ≥ 1/3 → lattice has no filtering power → FALSIFIED as predictor.
- **verdict_rule**: this card is the skeptic. "SUPPORTED" here = the *skeptical* claim
  survives = the lattice is confirmed decorative (≥2 implausible). A trigger of F-006-1
  (0–1 implausible) would instead *vindicate* the lattice as a predictor.

## Falsifiers (pre-registered, measurable)

- **F-006-1**: ≤ 1 of the 6 identities is implausible (would mean the lattice mostly lands on
  real targets → it IS a predictor → the skeptical hypothesis is refuted).
- **F-006-2**: the floor re-derivation diverges from H_001 (`|floor−19.275|>0.05`) — audit not anchored to real physics.
- **F-006-3**: the capacity re-derivation diverges from H_003 (`co2_mass_fraction(48)` ≤ 1.0 g/g) — the implausible case isn't actually implausible.
- **F-006-4** (bounds check): fraction implausible computed outside [0,1].
- **F-006-5** (negative control): a deliberately *physics-blind* relabeling (map each target to the nearest {2,4,12,24} combination) "matches" ≥ 5/6 targets — demonstrating that "the lattice matches" is cheap and non-discriminating.
- **F-006-6**: any audited identity's plausibility flag disagrees with its sister card's recorded verdict (audit must mirror the pre-registered sister verdicts, not re-judge them).

## Honest Limits

- **L1**: the plausibility oracle is the sister cards (H_001–H_005); this card is only as sound
  as those verdicts — it inherits their representative-figure limits.
- **L2**: "predictor vs label" is argued via filtering power, not a formal information criterion;
  a Bayesian model-comparison would quantify it but needs a prior over target-generating schemes.
- **L3**: the lattice may still be a useful *mnemonic / design-organizing* device even with zero
  predictive power — this card refutes only the *predictive* reading, not the organizational one.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `overview`, all L0–L6 (the lattice spans them).
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_001, H_002, H_003, H_004, H_005 (the audited cases).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**SUPPORTED** (the *skeptical* claim holds — the lattice is decorative, not predictive) —
6/6 falsifiers PASS. Run `2026-06-27`. Verbatim stdout:

```
H_006 — is the n=6 lattice a predictor? (negative control)
  floor anchor       = 19.275 kJ/mol  (H_001)
  mass_frac(48) anchor = 2.112 g/g     (H_003, >1.0 = impossible)
  audit: 3/6 lattice->target identities are physically implausible
    [PLAUSIBLE  ] J2-tau = 20 kJ/mol (floor)  (H_001)
    [PLAUSIBLE  ] sigma-phi = 10x (headroom)  (H_002)
    [IMPLAUSIBLE] J2*phi = 48 mmol/g (capacity)  (H_003)
    [IMPLAUSIBLE] J2 = 24 $/ton (cost)  (H_004)
    [PLAUSIBLE  ] n=6 hexagon (reactor)  (H_005)
    [IMPLAUSIBLE] J2 = 24x capacity ratio (48/2)  (H_003)
  fraction implausible = 0.50
  neg control: physics-blind relabel matches 5/5 targets
  [PASS] F-006-1
  [PASS] F-006-2
  [PASS] F-006-3
  [PASS] F-006-4
  [PASS] F-006-5
  [PASS] F-006-6
  6/6 falsifiers PASS
VERDICT: SUPPORTED  (lattice = decorative label, not a predictor)
```

Artifact: `state/H_006_n6-numerology-predictor_2026-06-27/result.json`. Half (3/6) the
lattice→target identities map to physically implausible targets, and a physics-blind relabel
from {2,4,12,24} matches all 5 numeric targets just as cleanly — so "it matches the lattice"
carries no information. The two genuinely real results (floor, hexagon) are derived from
physics that never invokes {2,4,12,24}. **Conclusion: the n=6 lattice is a mnemonic/organizing
device, not a predictor; every lattice-derived target must clear an independent physics
bounds-check before being treated as a goal.**
