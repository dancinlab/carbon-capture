---
id: H_003
slug: sorbent-capacity-bound
title: The 48 mmol/g (= J₂·φ) sorbent target is physically unreachable — it demands 211 % CO₂ by sorbent mass, ~5–24× any measured adsorbent
domain: sorbent
status: supported
exploration_method: closed-form gravimetric bound vs measured-sorbent envelope
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_003 — Sorbent capacity target is unphysical

## Hypothesis

The HEXA-CCUS L0 target of **48 mmol CO₂/g** (`= J₂·φ = 24·2`) is not an
aggressive-but-reachable goal — it is **physically impossible** at any condition.
At 44.009 g/mol, 48 mmol/g = **2.11 g CO₂ per g of sorbent (211 % of the sorbent's
own mass)**, exceeding the gravimetric uptake of every measured adsorbent
(best-in-class ≈ 8–10 mmol/g at saturating pressure; ≈ 1–2 mmol/g at the 400 ppm
DAC partial pressure that L0 must actually operate at). This card *falsifies the
target value* while leaving the *direction* (higher capacity than Climeworks'
~2 mmol/g is worth pursuing) intact.

## Why

This is the sharpest test of the n=6 numerology: `48 = J₂·φ` is a clean lattice
identity, but lattice-clean ≠ physical. L0.sorbent claims 48 mmol/g = 24×
Climeworks. If the number is unreachable, the numerology over-promised and the
honest target must be re-anchored to measured physics — exactly the kind of
break-walls / honesty finding the verification system exists to surface.

## Predictions

- **P1**: `co2_mass_fraction(48)` > 1.0 g/g (target exceeds 100 % sorbent mass → unphysical).
- **P2**: `co2_mass_fraction(48)` ≈ 2.11 g/g.
- **P3**: best measured sorbent (≈ 10 mmol/g) gives a mass fraction ≤ 0.5 g/g — comfortably
  physical, and the 48 target is ≥ 4.8× above it.
- **P4**: at the real DAC operating point (~1.5 mmol/g for Mg-MOF-74 at 400 ppm), the 48
  target is ≥ 30× above what the same material delivers in-condition.

## Variables

- `target = 48` mmol/g (`J₂·φ`) — source: spec / `L0.sorbent`.
- `best_measured = 10` mmol/g (Mg-MOF-74 high-pressure regime) — source: MOF literature, representative.
- `dac_measured = 1.5` mmol/g (Mg-MOF-74 at 400 ppm) — source: DAC sorbent literature, representative.
- `climeworks = 2.0` mmol/g — source: spec baseline.
- output: mass fraction (g/g) for target & best; ratios target/best, target/dac.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `co2_mass_fraction`, `capacity_ratio`.
- **run script**: `state/H_003_sorbent-capacity-bound_2026-06-27/run_H_003.py`
- **run cmd**: `python3 state/H_003_sorbent-capacity-bound_2026-06-27/run_H_003.py`
- **artifacts**: `state/H_003_sorbent-capacity-bound_2026-06-27/result.json`

## Criteria

- **C1**: P1 holds → the target is unphysical → the *target-reachability* claim is FALSIFIED.
- **verdict_rule**: this card is FRAMED to falsify the 48 mmol/g target. SUPPORTED-of-this-card
  = "the target is unphysical" claim survives all falsifiers (i.e. F-003-* all PASS). A trigger
  would mean 48 mmol/g is actually reachable after all.

## Falsifiers (pre-registered, measurable)

- **F-003-1**: `co2_mass_fraction(48)` ≤ 1.0 g/g (would mean 48 mmol/g is under 100 % mass → not obviously unphysical).
- **F-003-2**: target/best_measured ratio ≤ 2 (48 within 2× of a real sorbent → "aggressive but reachable", not impossible).
- **F-003-3**: target/dac_measured ratio ≤ 5 (48 within 5× of in-condition uptake).
- **F-003-4** (bounds check): `co2_mass_fraction(best_measured=10)` > 1.0 g/g (would mean even real sorbents break the mass bound → the bound itself is wrong).
- **F-003-5** (negative control): `co2_mass_fraction(0)` ≠ 0.0 (zero uptake must map to zero mass — guards the conversion).
- **F-003-6**: any published adsorbent with measured equilibrium uptake ≥ 48 mmol/g at ≤ 1 bar exists in the cited literature (would directly refute "no sorbent reaches it"). Pre-registered as: none known; treated as PASS unless one is produced.

## Honest Limits

- **L1**: `best_measured` and `dac_measured` are representative literature figures, not a
  systematic max over all sorbents — a record-holder a few mmol/g higher would not change
  the >4× verdict, but would tighten it.
- **L2**: the gravimetric mass bound (211 %) is a *plausibility* argument, not a strict
  thermodynamic impossibility — exotic chemisorption/clathrate phases can exceed 1 g/g in
  niche cases; none approach 2.11 g/g for cyclic CO₂ DAC, so the target stays unreachable in practice.
- **L3**: volumetric (mmol/cm³) targets behave differently; this card addresses only the
  gravimetric `mmol/g` figure the spec actually states.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `L0.sorbent`, `L0.candidates`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_006 (numerology as predictor — this is its strongest disconfirming case).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**SUPPORTED** (the *unphysical-target* claim survives) — 6/6 falsifiers PASS, i.e. the
48 mmol/g target is refuted as unreachable. Run `2026-06-27`. Verbatim stdout:

```
H_003 — 48 mmol/g sorbent target is unphysical
  mass_fraction(48 mmol/g) = 2.112 g CO2/g sorbent (211% of sorbent mass)
  mass_fraction(10 mmol/g) = 0.440 g/g (a real best-case sorbent)
  target / best_measured   = 4.8x
  target / dac_measured    = 32.0x
  known sorbent >= 48 mmol/g at <=1 bar: False
  [PASS] F-003-1
  [PASS] F-003-2
  [PASS] F-003-3
  [PASS] F-003-4
  [PASS] F-003-5
  [PASS] F-003-6
  6/6 falsifiers PASS
VERDICT: SUPPORTED  (target 48 mmol/g refuted as unreachable)
```

Artifact: `state/H_003_sorbent-capacity-bound_2026-06-27/result.json`. 48 mmol/g demands
211% of the sorbent's own mass in captured CO₂ — 4.8× a generous best-case real sorbent and
32× what the same material delivers at the 400 ppm DAC operating point. The lattice identity
`48 = J₂·φ` is clean but the number is physically out of reach; the honest L0 target must be
re-anchored to measured uptake. (Strongest disconfirming case feeding H_006.)
