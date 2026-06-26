---
id: H_005
slug: honeycomb-geometry
title: Among the only regular polygons that tile the plane (n=3,4,6), the hexagon minimizes wall length per unit channel area — but it is NOT the global minimum (n→∞ / circle is lower)
domain: reactor
status: supported
exploration_method: closed-form P/√A for regular n-gons
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_005 — Honeycomb reactor geometry

## Hypothesis

For a monolith reactor partitioned into equal-area channels, wall material per
unit flow area scales as `P/√A = 2·√(n·tan(π/n))` for a regular n-gon channel.
**Among the three regular polygons that tile the plane without gaps (n = 3, 4, 6),
the hexagon (n = 6) is the strict minimum** — the closed-form statement behind
the honeycomb conjecture (Hales 2001) and the L2 HEXA-REACTOR geometry choice.
The honest caveat: hexagon is *not* the unconstrained minimum — `P/√A` keeps
falling for n = 12 (3.586) toward the circle limit `2√π = 3.545`; those shapes
just cannot tile. So the correct claim is **"best space-filling cell," not "best
cell."**

## Why

`L2.reactor` cites "honeycomb hexagonal geometry (Hales 2001 optimal)." This card
verifies the precise sense in which it is optimal (space-filling) and pre-empts
the over-claim that a hexagon beats all shapes — which a naïve sweep falsifies
(n=12 is lower). It is the one HEXA-CCUS geometry claim that is genuine math, so
getting its scope exactly right matters for honesty.

## Predictions

- **P1**: `P/√A(6)` < `P/√A(4)` < `P/√A(3)` (hexagon best among tilers; ordering 6<4<3).
- **P2**: `P/√A(6)` ≈ 3.722.
- **P3**: `P/√A(12)` < `P/√A(6)` (a 12-gon has LESS wall — hexagon is not the global min).
- **P4**: `P/√A(n) → 2√π ≈ 3.545` as n grows (monotone approach to the circle limit).

## Variables

- tiling set: `n ∈ {3, 4, 6}` — the only regular polygons that tile the plane.
- comparison: `n = 12`, `n = 1000` (→ circle limit), `circle = 2√π`.
- output: `P/√A` for each n; the argmin over the tiling set; whether n=12 beats n=6.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `perimeter_area_ratio`.
- **run script**: `state/H_005_honeycomb-geometry_2026-06-27/run_H_005.py`
- **run cmd**: `python3 state/H_005_honeycomb-geometry_2026-06-27/run_H_005.py`
- **artifacts**: `state/H_005_honeycomb-geometry_2026-06-27/result.json`

## Criteria

- **C1**: argmin of `P/√A` over {3,4,6} is n=6 AND n=12 < n=6 (both the claim and its honest limit).
- **verdict_rule**: SUPPORTED = all falsifiers PASS (hexagon is the tiling-min AND the global-min caveat is confirmed).

## Falsifiers (pre-registered, measurable)

- **F-005-1**: argmin of `P/√A` over the tiling set {3,4,6} is NOT n=6.
- **F-005-2**: ordering `P/√A(6) < P/√A(4) < P/√A(3)` violated.
- **F-005-3** (anti-overclaim, expected NOT to trigger): `P/√A(12)` ≥ `P/√A(6)` — if this held,
  the hexagon WOULD be the global min; it is not, so the falsifier passes by confirming 12<6.
- **F-005-4** (bounds check): `P/√A(1000)` < `2√π = 3.5449` (limit must be approached from above, never crossed).
- **F-005-5** (negative control): `P/√A(4)` ≠ 4.0 (a unit-area square has perimeter 4 exactly — closed-form anchor; any drift signals a formula bug).
- **F-005-6**: `perimeter_area_ratio(2)` does not raise (n<3 is not a polygon — must be rejected, guarding the domain).

## Honest Limits

- **L1**: idealized 2-D cross-section — ignores wall thickness, manufacturability, pressure
  drop, and the 3-D entrance/exit effects that drive real monolith design.
- **L2**: "wall per area" is a material-economy proxy, not the actual reactor objective
  (mass transfer, ΔP, thermal mass) — a hexagon optimal for wall material may not be optimal
  for those, so "optimal geometry" is scoped to the cited material-minimization sense only.
- **L3**: the honeycomb conjecture proves hexagons optimal among ALL partitions (not just
  regular polygons); this card only checks the regular-polygon slice, which is sufficient to
  confirm the claim's direction but not the full theorem.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `L2.reactor`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_006 (n=6 as predictor — this is its strongest *confirming* case).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**SUPPORTED** — 6/6 falsifiers PASS. Run `2026-06-27`. Verbatim stdout:

```
H_005 — honeycomb reactor geometry
  P/sqrt(A): n=3 4.5590  n=4 4.0000  n=6 3.7224  (tilers)
  P/sqrt(A): n=12 3.5863  n=1000 3.5449  circle 3.5449
  argmin over tilers {3,4,6} = n=6  (hexagon best space-filling cell)
  honest limit: n=12 (3.5863) < n=6 (3.7224) -> hexagon NOT the global min
  [PASS] F-005-1
  [PASS] F-005-2
  [PASS] F-005-3
  [PASS] F-005-4
  [PASS] F-005-5
  [PASS] F-005-6
  6/6 falsifiers PASS
VERDICT: SUPPORTED
```

Artifact: `state/H_005_honeycomb-geometry_2026-06-27/result.json`. Real math: the hexagon is
the strict minimum-wall cell **among the three regular polygons that tile the plane** (3.722 <
square 4.0 < triangle 4.559). The pre-registered honest limit held — n=12 (3.586) beats the
hexagon, so the hexagon is the best *space-filling* cell, **not** the global minimum (the
circle limit 2√π = 3.545 is lower but does not tile). This is the one lattice number that
stands on genuine geometry — and it stands *without* needing {2,4,12,24} (feeds H_006 P3).
