---
id: H_A001
slug: carbon-centrifuge
title: 🜂 ABSTRACT — gas-centrifuge separation of CO₂ by molecular mass (44 vs 28/32), ~7 stages to concentrate from 400 ppm, but throughput energy is the wall
domain: process
status: abstract-unverified
tier: 🜂 ABSTRACT
exploration_method: imagination + closed-form separation-factor kernel (NOT run)
pre_register_frozen: false
deterministic: false
llm: conjecture
---

# 🜂 H_A001 — Carbon centrifuge ("탄소 원심 고리")

## Concept

Spin air in an ultracentrifuge / orbital ring and let CO₂ (M=44) migrate radially away from
N₂ (28) and O₂ (32), like isotope enrichment — **no sorbent, no thermal swing**. A cascade of
stages concentrates the trace 400-ppm CO₂ toward a useful stream.

## Falsifiable prediction (kernel — not run)

Separation factor per stage `α = exp(ΔM·v²/(2RT))`. At rim speed v≈600 m/s, ΔM=16 g/mol,
T=298 K: `α ≈ exp(1.16) ≈ 3.2` per stage → `ln(2400)/ln(3.2) ≈ 7` stages to go 400 ppm → near-pure.
**The separation factor is fine; the kill criterion is the energy to spin planetary air volumes
(H_013: ~1.3e6 m³/ton) — predict it lands far ABOVE the 19.3 kJ/mol floor (likely 10²–10³×).**
Falsified-as-practical if stage energy ≫ floor; vindicated only if a passive spin source (orbital,
Coriolis) supplies the rotation for free.

## Why novel (vs the verified H_0xx chain)

The whole verified chain separates by *chemistry* (binding energy, H_012). This separates by
*mass alone* — an axis no sorbent uses, immune to humidity (H_016) and degradation.

## Honest status

🜂 Imagination. No run, no verdict. The kernel suggests separation is easy but throughput energy
kills it on Earth — a clean negative-space result that reinforces why air-handling (H_013) is the
real DAC wall. Promote to H_0xx only if actually modeled.
