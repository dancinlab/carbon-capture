---
id: H_015
slug: storage-capacity
title: Geologic storage capacity is NOT the bottleneck — ~1e4 Gt global capacity is ~9× the 1095 Gt drawdown demand (≥100 yr at 100 Gt/yr); the binding constraints are energy (H_014) and air handling (H_013), not void space
domain: plant
status: supported
exploration_method: closed-form capacity-vs-demand ratio + injection-rate sanity
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_015 — Geologic storage capacity is sufficient

## Hypothesis

A common worry is "where does the CO₂ go?" — but **storage void is not the wall**.
Conservative global geologic storage estimates (~1e4 Gt CO₂ across saline aquifers,
depleted fields, basalt) are **~9× the 1095 Gt** needed for the H_009 420→280 ppm
drawdown, and at 100 Gt/yr that capacity lasts **≥100 years**. The binding
constraints upstream are **energy/net-negativity (H_014)** and **air handling
(H_013)** — not where to put it. (Permanence and injection-rate per-site remain real
engineering concerns, flagged in limits.)

## Why

`L4.plant` / `flow.store` route CO₂ to geologic injection; `L6` implies Gt-scale.
This card sizes capacity against demand so the verification record states plainly
which walls are real (energy, air) and which are not (void space) — break-walls:
don't mis-attribute the bottleneck.

## Predictions

- **P1**: capacity/demand `1e4 / 1095` ≥ 5× (comfortable headroom).
- **P2**: years of capacity at 100 Gt/yr ≥ 100.
- **P3**: even a pessimistic 1e3 Gt capacity still ≥ 0.5× the 1095 Gt demand (same order, not orders short).
- **P4**: demand itself (`ppm_to_gt_co2(140)`) matches H_009's 1095 Gt (consistency).

## Variables

- `capacity_central = 1e4 Gt`, `capacity_pessimistic = 1e3 Gt` — source: IPCC/IEA storage assessments, representative.
- `demand = ppm_to_gt_co2(140)` ≈ 1095 Gt — from H_009.
- `rate = 100 Gt/yr` — source: `L6.universal`.
- output: capacity/demand ratios; years of capacity; demand consistency.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `ppm_to_gt_co2`.
- **run script**: `state/H_015_storage-capacity_2026-06-27/run_H_015.py`
- **run cmd**: `python3 state/H_015_storage-capacity_2026-06-27/run_H_015.py`
- **artifacts**: `state/H_015_storage-capacity_2026-06-27/result.json`

## Criteria

- **C1**: P1–P4 hold → storage capacity is sufficient (not the bottleneck).
- **verdict_rule**: SUPPORTED = all falsifiers PASS.

## Falsifiers (pre-registered, measurable)

- **F-015-1**: capacity/demand (central) < 5 (storage not comfortably sufficient).
- **F-015-2**: years of capacity at 100 Gt/yr < 100 (capacity runs out within a century).
- **F-015-3**: pessimistic 1e3 Gt capacity < 0.5× demand (even same-order claim fails).
- **F-015-4** (bounds check): `ppm_to_gt_co2(0)` ≠ 0 (zero demand sanity).
- **F-015-5** (negative control): `ppm_to_gt_co2(280)` = 2× `ppm_to_gt_co2(140)` (linear demand).
- **F-015-6**: demand `ppm_to_gt_co2(140)` diverges from H_009 (`|demand − 1095| > 5 Gt`).

## Honest Limits

- **L1**: total static capacity ≠ usable/injectable capacity — practical capacity is reduced by
  injectivity, cap-rock integrity, pressure buildup, and basin access; the ~1e4 Gt is an upper estimate.
- **L2**: this card addresses *void volume*, NOT *injection rate per well* (12 wells in L4 is a
  separate per-site duty) nor *permanence/monitoring* (leakage over centuries) — both real, unmodeled.
- **L3**: mineralization (basalt, concrete) is a distinct, effectively unlimited but slower path; this
  card uses conventional storage figures and does not credit it.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `L4.plant`, `flow.store`, `L6.universal`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_009 (drawdown demand), H_013 (air wall), H_014 (energy wall).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**SUPPORTED** — 6/6 falsifiers PASS. Run `2026-06-27`. Verbatim stdout:

```
H_015 — geologic storage capacity vs demand
  drawdown demand (140 ppm) = 1095 Gt CO2  (H_009)
  central capacity 1e4 Gt   = 9.1x demand
  pessimistic 1e3 Gt        = 0.91x demand
  years at 100 Gt/yr        = 100
  [PASS] F-015-1
  [PASS] F-015-2
  [PASS] F-015-3
  [PASS] F-015-4
  [PASS] F-015-5
  [PASS] F-015-6
  6/6 falsifiers PASS
VERDICT: SUPPORTED  (storage void sufficient; not the bottleneck)
```

Artifact: `state/H_015_storage-capacity_2026-06-27/result.json`. Central geologic capacity
(~1e4 Gt) is 9.1× the 1095 Gt drawdown demand and lasts 100 years at 100 Gt/yr; even a
pessimistic 1e3 Gt is the same order (0.91×). Storage void is **not** the bottleneck — the
binding walls are energy/net-negativity (H_014) and air handling (H_013). (Per-site injection
rate and permanence/monitoring remain real engineering concerns, flagged in limits — they are
not void-capacity questions.)
