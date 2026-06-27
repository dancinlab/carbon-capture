---
id: H_021
slug: portfolio-no-single-path
title: "Is electric DAC the path?" is the wrong question — no single removal path dominates on all four axes (energy · rate · footprint · permanence), so the answer is a PORTFOLIO, not a winner
domain: system
status: supported
exploration_method: multi-axis Pareto domination test over the verified path set
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_021 — No single path dominates: removal is a portfolio

## Hypothesis

H_020 showed free-energy paths crush electric DAC on *energy-per-active-grid-kWh*. But that
is one axis. Score the live paths on the **four axes that actually decide deployment** —
energy(NNR), rate(Gt/yr speed), footprint(land/material), permanence(storage durability) —
and **no path is best on all four**: electric DAC leads on rate/footprint/permanence but
trails on energy; enhanced weathering leads on energy/permanence but trails on rate/footprint;
the artificial leaf leads on energy but trails on footprint/permanence. By Pareto domination,
**none dominates** → "is electric DAC THE path?" is mis-framed; the answer is a **portfolio**.

## Why

Directly answers the user's implication. H_020 could be mis-read as "abandon DAC for
weathering"; this card prevents that over-correction by showing the trade is multi-axis. The
honest conclusion is not a single winner but a portfolio matched to each axis's priority.

## Predictions

- **P1**: no path Pareto-dominates all others across the four axes.
- **P2**: electric DAC is the unique best on rate AND footprint (its real strengths).
- **P3**: at least one free-energy path is the unique best on energy (its real strength).
- **P4**: every path is the worst on at least one axis (no free lunch).

## Variables

- paths × axes scorecard (0–1, higher=better), representative:
  electric-DAC {energy 0.20, rate 0.90, footprint 0.90, permanence 0.90};
  weathering {0.90, 0.20, 0.20, 0.90}; artificial-leaf {0.95, 0.50, 0.30, 0.30}.
- output: domination matrix; per-axis argmax; whether any path dominates all.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `dominates`.
- **run script**: `state/H_021_portfolio-no-single-path_2026-06-27/run_H_021.py`
- **run cmd**: `python3 state/H_021_portfolio-no-single-path_2026-06-27/run_H_021.py`
- **artifacts**: `state/H_021_portfolio-no-single-path_2026-06-27/result.json`

## Criteria

- **C1**: P1–P4 hold → portfolio, not a single winner.
- **verdict_rule**: SUPPORTED = all falsifiers PASS.

## Falsifiers (pre-registered, measurable)

- **F-021-1**: some path Pareto-dominates all others (a single winner exists → portfolio claim false).
- **F-021-2**: electric DAC is NOT the unique best on rate (its claimed strength fails).
- **F-021-3**: no free-energy path is the unique best on energy.
- **F-021-4** (bounds check): `dominates(x, x)` is False (a path does not strictly dominate itself).
- **F-021-5** (negative control): `dominates(strictly-better, baseline)` is True for a constructed all-axes-better card (the test detects real domination when it exists).
- **F-021-6**: any path is best on ALL four axes simultaneously (would be a true single winner).

## Honest Limits

- **L1**: the scores are representative ordinal judgements, not measured — the *ranking direction* on
  each axis is defensible (DAC fast/compact, weathering slow/material-heavy), the exact 0–1 values are not.
- **L2**: four axes is a reduction; cost, social license, MRV (measurement/verification), and co-benefits
  are omitted and could shift the portfolio weighting.
- **L3**: a portfolio conclusion is axis-weight-dependent — a decision-maker who weights energy×grid
  heavily (fossil grid) leans free-energy; one who weights speed leans DAC. The card shows the trade, not a pick.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `thesis`, `convergence`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_020 (energy axis), H_022 (DAC niche), H_023 (abatement-first), H_A010/A011.
- **harness**: `tool/carbon_capture.py`.

## Verdict

**🟢 SUPPORTED** — 6/6 falsifiers PASS. Run `2026-06-27`:

```
H_021 — no single path dominates (portfolio)
  single dominating path? NONE
  best on energy     : artificial-leaf
  best on rate       : electric-DAC
  best on footprint  : electric-DAC
  best on permanence : electric-DAC
  electric-DAC     worst axis: energy
  weathering       worst axis: rate
  artificial-leaf  worst axis: footprint
  6/6 falsifiers PASS
VERDICT: SUPPORTED  (removal is a portfolio; 'is DAC THE path' is the wrong question)
```

Artifact: `state/H_021_portfolio-no-single-path_2026-06-27/result.json`. No path Pareto-dominates:
electric DAC owns rate + footprint + permanence but is worst on energy; the artificial leaf owns
energy but is worst on footprint; weathering is worst on rate. So "is electric DAC THE path?" is
mis-framed — the answer is a **portfolio matched to whichever axis a deployment weights highest**.
