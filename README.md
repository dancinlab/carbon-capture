# carbon-capture

Engineering CO₂ capture-storage-conversion as a **designed multi-scale system** —
the **HEXA-CCUS** architecture — instead of a single adsorber. Carbon (Z=6) anchored,
an 8-stage chain (L0–L7) spanning atomic sorbent to planetary control. The scope is the
**capture-storage-conversion system**, not one sorbent: today's DAC single-stage rigs are
the first instance, not the boundary.

## The thesis

> Capture cost and energy are framed as fixed ceilings ("DAC is just expensive"). This
> repo's origin spec reaches a different conclusion:

**Capture cost/energy is an engineering-and-volume problem, reopenable down to a
thermodynamic floor — not a physics ceiling.**

```
Framing claim                     carbon-capture verdict (HEXA-CCUS spec)
─────────────────────────         ───────────────────────────────────────
"DAC is fundamentally expensive"  →  separation work has a FLOOR, not a wall
                                     (W_min = RT·ln(1/x_CO2) ≈ 19.4 kJ/mol ≈ J₂−τ = 20)
"~200 kJ/mol is the cost"        →  wet-amine sits 10× above floor (σ−φ headroom)
"captured CO₂ is waste"          →  CO₂ is feedstock → graphene/CNT ($0 → ~$1M/ton)
```

- **Energy floor** — `W_min ≈ 20 kJ/mol` (= J₂−τ); current wet-amine ≈ 200 kJ/mol leaves
  a `σ−φ = 10×` reduction band.
- **Cost floor** — CAPEX reopenable toward `$24/ton (= J₂)` vs Climeworks ≈ $600/ton.
- **Waste-to-value** — captured carbon converts to graphene/CNT/diamond/C60, flipping
  value from $0/ton to ~$1M/ton.

## The 7-level stack (n=6 lattice: φ=2 · τ=4 · σ=12 · J₂=24)

```
L0 HEXA-SORBENT    material   — top-6 MOFs, all CN=6 octahedral · target 48 mmol/g
L1 HEXA-PROCESS    process    — TSA 6-stage · PSA 12-bed · energy target 20 kJ/mol  ← bottleneck
L2 HEXA-REACTOR    core       — honeycomb hexagonal · 6 reactor types · 12 ton/day/module
L3 HEXA-CHIP       chip       — RISC-V N6 6-stage pipeline · ppb-level sensing
L4 HEXA-PLANT      system     — DAC farm + SC-CO2 pipeline + geologic injection · 1 Mt/yr
L5 HEXA-TRANSMUTE  conversion — CO₂ → diamond / graphene / CNT / C60
L6 HEXA-UNIVERSAL  planetary  — 36 hubs · 6 subsystems · 420 → 280 ppm in σ=12 years
```

## Structure

```
carbon-capture/
├─ src/              — source code
├─ state/            — all work artifacts (experiments · bench · verification), git-tracked
│                      n6-carbon-capture-spec.md = imported HEXA-CCUS origin spec
├─ ARCHITECTURE.json — final architecture SSOT (JSON `children` tree, update-in-place)
├─ architecture.html — human viewer for the JSON (run `python3 serve.py`)
└─ CHANGELOG.md      — history (append-only)
```

## Provenance

The origin spec (`state/n6-carbon-capture-spec.md`) was imported from
`dancinlab/hexa-grid` (`CARBON-CAPTURE.md`), surfaced as the **HEXA-CARBON-CAPTURE**
("Air Vacuum") entry in the `dancinlab/echoes` Environment Toolkit. This repo extracts it
into its own campaign — the live design SSOT is `ARCHITECTURE.json`; the imported spec is
the seed of record, not the SSOT.

## Viewing

```
python3 serve.py        # serve on :8000, open architecture.html
```
