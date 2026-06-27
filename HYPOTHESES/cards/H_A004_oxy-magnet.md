---
id: H_A004
slug: oxy-magnet
title: 🜂 ABSTRACT — magnetic removal of paramagnetic O₂ to concentrate CO₂ (likely falsified in gas phase — magnetic energy ≪ thermal by ~10³ at 10 T)
domain: process
status: falsified
tier: 🔴 FALSIFIED (graduated from 🜂 ABSTRACT by running the kernel)
exploration_method: imagination + magnetic-vs-thermal energy kernel (NOT run)
pre_register_frozen: false
deterministic: false
llm: conjecture
---

# 🜂 H_A004 — Oxygen magnet ("산소 자석")

## Concept

O₂ is strongly **paramagnetic**; CO₂ and N₂ are not. A magnetic gradient pulls O₂ aside, so the
remaining stream is *enriched* in CO₂ — a magnetic first cut with no sorbent, exploiting an axis
(magnetic susceptibility) nothing else uses.

## Falsifiable prediction (kernel — not run)

Magnetic energy density of gas-phase O₂ at B=10 T: `χ_vol·B²/(2μ₀) ≈ 1.9e-6·100/(2·4π·10⁻⁷) ≈ 76
J/m³`, versus thermal/pressure energy density ≈ **1e5 J/m³**. **Predict FALSIFIED in the gas phase:
magnetic energy is ~10³× below thermal motion at a strong 10 T field** — O₂ won't sort against
diffusion. Vindicated only for *liquid/condensed* O₂ (where magnetic separation is real) or
impractically high fields.

## Why novel (vs the verified H_0xx chain)

Separation by magnetic susceptibility — orthogonal to binding-energy (H_012), mass (H_A001), and charge.

## Verdict

**🔴 FALSIFIED** (gas phase) — graduated by running the kernel. Gas-phase O₂ magnetic/thermal energy
ratio at a strong 10 T = **7.5e-4 (~10³× too weak)** → magnetic sorting is overwhelmed by thermal
motion. Survives only for *condensed/liquid* O₂, not ambient air. Artifact: `result_H_A004.json`.

## Original conjecture (pre-run)

🜂 Imagination. No run, no verdict. Kernel suggests a gas-phase NEGATIVE; the idea survives only in a
cryo/condensed regime (links H_A002/altitude-still). Honest negative-space.
