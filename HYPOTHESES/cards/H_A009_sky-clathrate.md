---
id: H_A009
slug: sky-clathrate
title: 🜂 ABSTRACT — capture CO₂ by forming a selective clathrate hydrate (CO₂ caged in water ice); phase boundary does the selecting, but 400-ppm formation pressure likely needs pre-concentration
domain: process
status: falsified
tier: 🔴 FALSIFIED (graduated from 🜂 ABSTRACT by running the kernel)
exploration_method: imagination + hydrate-stability kernel (NOT run)
pre_register_frozen: false
deterministic: false
llm: conjecture
---

# 🜂 H_A009 — Sky clathrate ("하늘 얼음 우리")

## Concept

Form a **CO₂ clathrate hydrate** — CO₂ molecules caged inside a water-ice lattice — at modest cold
and pressure. The cage geometry *selectively* admits CO₂ over N₂, so capture becomes a
**crystallization**, and the same hydrate is a stable storage phase (links H2 ABYSS-ICE / H_015).

## Falsifiable prediction (kernel — not run)

CO₂ hydrate is stable at ~1 °C only above ~1.2 MPa *at pure-CO₂ partial pressure*; at the **400-ppm
partial pressure** the hydrate stability line (Clausius-Clapeyron) demands far higher total pressure
or far lower temperature. **Predict: direct hydrate formation from ambient air is not feasible without
pre-concentration** (the dilute partial pressure is the kill), but post-concentration hydrate STORAGE
is attractive. Vindicated as a *storage* phase even if not a *capture* phase.

## Why novel (vs the verified H_0xx chain)

Separation/storage by a *phase boundary*, not a sorbent surface (H_012) or a geologic seal (H_015) —
a crystallization axis untouched by the chain.

## Verdict

**🔴 FALSIFIED** (air-capture) — graduated by running the kernel. CO₂ hydrate stability at the 400-ppm
partial pressure needs ~**−74 °C** → a clathrate cannot form directly from ambient air without
pre-concentration. The *capture-from-air* path is refuted; the **storage phase** (post-concentration
hydrate / abyss-ice) remains viable. Artifact: `result_H_A009.json`.

## Original conjecture (pre-run)

🜂 Imagination. No run, no verdict. Kernel splits it: capture-from-air likely NEGATIVE, storage likely
viable. Promote to H_0xx only if the hydrate stability line is actually computed.
