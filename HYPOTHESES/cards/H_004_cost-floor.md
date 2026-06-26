---
id: H_004
slug: cost-floor
title: The 25× capture-cost reduction ($600→$24/ton) is within historical learning-curve precedent, but the $24/ton (=J₂) endpoint is below credible near-term engineering floors — PARTIAL
domain: plant
status: partial
exploration_method: closed-form ratio + Wright's-law learning-curve comparison
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_004 — Capture cost floor & learning curve

## Hypothesis

Two separable claims:
(a) the **reduction factor** from Climeworks (~$600/ton) to the spec target
($24/ton = J₂) is **25×**, and a 25× cumulative cost decline is well inside what
deployment learning curves have delivered for analogous modular hardware (solar PV
fell >100× over its history) — so the *direction and magnitude* are credible;
(b) the **absolute endpoint** $24/ton sits **below credible near-term floors**
(DOE DAC target ~$100/ton; widely cited long-run aspiration ~$50/ton), so the
specific $24 number is unverified-optimistic. Net: **PARTIAL**.

## Why

`thesis.cost-floor` and `L4.plant` assert CAPEX ≈ $24/ton. Cost is downstream of
energy (H_002) but adds CAPEX, O&M, and learning effects. This card asks whether
the *gap* is real (yes) without endorsing the *exact floor* (not shown).

## Predictions

- **P1**: `cost_ratio(600, 24)` = 25.0× exactly.
- **P2**: a 25× decline needs `log(25)/log(1/(1-LR))` doublings; at an 18 % learning
  rate (LR, typical modular hardware) that is ≤ 17 capacity doublings — historically
  attainable. Predict required doublings ≤ 20.
- **P3**: $24/ton < $50/ton (long-run aspiration) and < $100/ton (DOE near-term) — i.e.
  the endpoint is below both reference floors → flagged unverified, not SUPPORTED.
- **P4**: the *gap to a defensible target* ($600 → $100 DOE) is ≥ 6× — real and large
  even on the conservative endpoint.

## Variables

- `baseline = 600` $/ton (Climeworks today) — source: spec.
- `target = 24` $/ton (`J₂`) — source: spec.
- `doe_target = 100` $/ton — source: U.S. DOE Carbon Negative Shot, representative.
- `aspiration = 50` $/ton — source: commonly cited DAC long-run figure, representative.
- `LR = 0.18` (learning rate per doubling) — source: modular-hardware learning-curve literature, representative.
- output: `cost_ratio`, required doublings for 25×, gap to DOE target.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `cost_ratio` (+ inline learning-curve math).
- **run script**: `state/H_004_cost-floor_2026-06-27/run_H_004.py`
- **run cmd**: `python3 state/H_004_cost-floor_2026-06-27/run_H_004.py`
- **artifacts**: `state/H_004_cost-floor_2026-06-27/result.json`

## Criteria

- **C1**: P1, P2, P4 hold (gap real, learning-curve-plausible) AND P3 holds (endpoint below
  reference floors) → verdict PARTIAL by construction.
- **verdict_rule**: SUPPORTED only if the endpoint ALSO clears a credible floor (it will not);
  FALSIFIED if the gap or learning-curve claim collapses; else PARTIAL.

## Falsifiers (pre-registered, measurable)

- **F-004-1**: `cost_ratio(600,24)` ≠ 25.0 (arithmetic of the headline ratio wrong).
- **F-004-2**: required doublings for 25× at LR=0.18 > 20 (learning-curve route implausibly long).
- **F-004-3** (gap reality): gap `600/100` < 3 (gap to even the DOE target too small to matter).
- **F-004-4** (endpoint check, expected to TRIGGER → forces PARTIAL): `target` ≥ `aspiration`
  (24 ≥ 50) — if the endpoint were already at/above the aspiration floor it would be credible;
  it is below, so this falsifier *does not* trigger and the endpoint stays flagged-optimistic.
- **F-004-5** (bounds check): `cost_ratio` with `target ≤ 0` raises (guards divide-by-zero).
- **F-004-6** (negative control): `cost_ratio(x, x)` = 1.0 for any x (no spurious reduction when baseline=target).

## Honest Limits

- **L1**: learning rate, DOE target, and aspiration are representative external figures, not
  measured here — the doublings count moves with LR (a 10 % LR needs ~30 doublings).
- **L2**: cost is not pure energy — CAPEX/O&M/financing dominate DAC today and are not modeled;
  the learning-curve argument is an analogy, not a bottom-up cost model.
- **L3**: $/ton depends on energy price, capacity factor, and CO₂ sale/credit value — a
  high-value conversion path (H_005-adjacent, L5 transmute) changes the economics entirely.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `thesis.cost-floor`, `L4.plant`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_002 (energy headroom), H_006 (is "24 = J₂" predictive?).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**PARTIAL** — 6/6 falsifiers PASS, but the $24/ton endpoint does not clear a credible
reference floor, so the card resolves to PARTIAL by its pre-registered rule. Run `2026-06-27`:

```
H_004 — capture cost floor & learning curve
  cost_ratio(600 -> 24)        = 25.0x
  doublings for 25x at LR=18%   = 16.2
  gap to DOE $100/ton           = 6.0x
  endpoint $24 clears $50 floor : False
  [PASS] F-004-1
  [PASS] F-004-2
  [PASS] F-004-3
  [PASS] F-004-4
  [PASS] F-004-5
  [PASS] F-004-6
  6/6 falsifiers PASS
VERDICT: PARTIAL  (gap real & learnable; $24/ton endpoint unverified-optimistic)
```

Artifact: `state/H_004_cost-floor_2026-06-27/result.json`. The **direction** is sound: a 25×
cost decline needs only ~16 capacity doublings at an 18% learning rate (historically routine
for modular hardware), and the gap to even the conservative DOE $100/ton target is 6×. But the
specific **$24/ton (= J₂) endpoint sits below** both the $50 aspiration and $100 DOE floors —
unverified-optimistic. Honest split: chase the gap, don't bank the exact number.
