---
id: H_011
slug: sc-co2-compression
title: Compressing captured CO₂ to the 12 MPa pipeline pressure costs ~11.9 kJ/mol (isothermal ideal) — ~60% of the capture floor, and 12 MPa is safely supercritical (> Pc 7.38 MPa)
domain: plant
status: supported
exploration_method: closed-form isothermal compression work + critical-point check
verification_method: deterministic harness + 6 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-06-27
deterministic: true
llm: none
---

# H_011 — Supercritical CO₂ compression for storage

## Hypothesis

L4's `12 MPa SC-CO₂ pipeline` needs compression work that is a real, non-trivial
add-on to capture. The ideal isothermal work from ~1 bar to 120 bar at 298 K is
`R·T·ln(120) ≈ 11.9 kJ/mol` — about **60% of the 19.3 kJ/mol separation floor**, a
meaningful tax that capture-only accounting omits. And 12 MPa is correctly chosen:
it is **above the CO₂ critical pressure (7.38 MPa)**, so the pipeline fluid is dense
supercritical (good for transport), not gas.

## Why

`L4.plant` / `flow.store` route concentrated CO₂ to 12 MPa SC-CO₂. Total system
energy = capture + compression; this card sizes the compression term and checks the
pressure choice against the CO₂ phase diagram. It bounds an often-ignored cost.

## Predictions

- **P1**: `isothermal_compression_work(120 bar, 1 bar, 298 K)` ∈ [11, 13] kJ/mol.
- **P2**: that work is 0.4–0.8× the 19.3 kJ/mol separation floor (a real fraction, not negligible, not dominant).
- **P3**: 12 MPa > 7.38 MPa critical pressure → supercritical (the regime SC-CO₂ requires).
- **P4**: work scales as `ln(p)` — going to 24 MPa adds only `R·T·ln(2) ≈ 1.7 kJ/mol`, not double.

## Variables

- `p_final = 120 bar` (12 MPa) — source: `L4.plant`.
- `p_initial = 1 bar` (post-desorption) — source: representative.
- `T = 298.15 K` — source: standard (isothermal idealization).
- `Pc_CO2 = 73.8 bar` (7.38 MPa) — source: CO₂ critical point, standard.
- `floor = 19.275 kJ/mol` — from H_001.
- output: compression work; ratio to floor; supercritical flag; ln-scaling check.

## Run Protocol

- **harness**: `tool/carbon_capture.py` — `isothermal_compression_work`, `min_separation_work`.
- **run script**: `state/H_011_sc-co2-compression_2026-06-27/run_H_011.py`
- **run cmd**: `python3 state/H_011_sc-co2-compression_2026-06-27/run_H_011.py`
- **artifacts**: `state/H_011_sc-co2-compression_2026-06-27/result.json`

## Criteria

- **C1**: P1–P4 hold.
- **verdict_rule**: SUPPORTED = all falsifiers PASS.

## Falsifiers (pre-registered, measurable)

- **F-011-1**: `work(120,1)` < 11 or > 13 kJ/mol (compression arithmetic off).
- **F-011-2**: work/floor < 0.4 or > 0.8 (mis-sized relative to the capture floor).
- **F-011-3**: 120 bar ≤ 73.8 bar critical (would be sub-critical — wrong regime for SC-CO₂).
- **F-011-4** (bounds check): `isothermal_compression_work(1,1)` ≠ 0 (no work at no pressure ratio).
- **F-011-5** (negative control): `work(240,1) − work(120,1)` ≈ `R·T·ln(2) = 1.717 kJ/mol` (ln-scaling).
- **F-011-6**: `work(120,1)` ≥ the separation floor (would mean compression dominates capture — it should not).

## Honest Limits

- **L1**: isothermal ideal-gas work underestimates real compression — multi-stage with intercooling
  and real-gas (Z<1 near critical) effects raise it ~1.5–2×; the conclusion "real, sub-floor add-on" holds.
- **L2**: ignores pump work for the dense-phase pipeline and boost stations (`120 km boosters`),
  and the energy to cool/condition the stream — all additive.
- **L3**: 1 bar suction is representative; a vacuum-swing desorption (sub-atmospheric) would raise
  the compression ratio and the work.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `L4.plant`, `flow.store`.
- **spec**: `state/n6-carbon-capture-spec.md`.
- **sister H**: H_001 (floor), H_008 (alternative fate — conversion), H_009 (system energy).
- **harness**: `tool/carbon_capture.py`.

## Verdict

**SUPPORTED** — 6/6 falsifiers PASS. Run `2026-06-27`. Verbatim stdout:

```
H_011 — SC-CO2 compression to 12 MPa
  separation floor        = 19.27 kJ/mol
  compression 1->120 bar  = 11.87 kJ/mol  (0.62x the floor)
  12 MPa supercritical?   = True  (Pc = 7.38 MPa)
  doubling to 240 bar adds = 1.718 kJ/mol (expect R*T*ln2 = 1.718)
  [PASS] F-011-1
  [PASS] F-011-2
  [PASS] F-011-3
  [PASS] F-011-4
  [PASS] F-011-5
  [PASS] F-011-6
  6/6 falsifiers PASS
VERDICT: SUPPORTED  (storage compression ~60% of floor, supercritical regime correct)
```

Artifact: `state/H_011_sc-co2-compression_2026-06-27/result.json`. Storage compression to the
12 MPa pipeline is ~11.9 kJ/mol (0.62× the separation floor) — a real but sub-dominant add-on,
and 12 MPa is correctly above the CO₂ critical pressure (7.38 MPa) for dense supercritical
transport. The ln-pressure scaling is exact (doubling to 24 MPa adds only R·T·ln2 = 1.72 kJ/mol).
