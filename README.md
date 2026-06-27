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
  a `σ−φ = 10×` reduction band. ✅ verified (H_001/H_002: floor 19.3 kJ/mol, headroom ~10×).
- **Cost floor** — CAPEX reopenable toward Climeworks ≈ $600/ton. 🟡 the 25× gap is
  learning-curve-plausible, but the `$24/ton (= J₂)` endpoint is verification-flagged
  optimistic — below the $50/$100 reference floors (H_004).
- **Waste-to-value** — captured carbon converts to graphene/CNT/diamond/C60, flipping
  value from $0/ton to ~$1M/ton.

## The 7-level stack (n=6 lattice: φ=2 · τ=4 · σ=12 · J₂=24)

```
L0 HEXA-SORBENT    material   — top-6 MOFs, all CN=6 octahedral · 48 mmol/g target 🔴 unreachable (H_003)
L1 HEXA-PROCESS    process    — TSA 6-stage · PSA 12-bed · energy target 20 kJ/mol  ← bottleneck
L2 HEXA-REACTOR    core       — honeycomb hexagonal · 6 reactor types · 12 ton/day/module
L3 HEXA-CHIP       chip       — RISC-V N6 6-stage pipeline · ppb-level sensing
L4 HEXA-PLANT      system     — DAC farm + SC-CO2 pipeline + geologic injection · 1 Mt/yr
L5 HEXA-TRANSMUTE  conversion — CO₂ → diamond / graphene / CNT / C60
L6 HEXA-UNIVERSAL  planetary  — 36 hubs · 6 subsystems · 420 → 280 ppm in σ=12 years
```

## Verification (pre-register → falsify → run → verdict)

A hypothesis-verification system (anima-parity) tests the spec's claims with deterministic,
stdlib-only falsifiers — separating **real physics** from **n=6 numerology** without
tune-to-green. 13 cards so far (each 6/6 falsifiers PASS):

```
H_001 separation-floor      🟢 SUPPORTED   floor 19.275 kJ/mol, monotone in dilution
H_002 energy-headroom       🟢 SUPPORTED   ~10×(spec)·20×(Climeworks)·7.8×(next-gen)
H_003 sorbent-capacity      🟢 SUPPORTED   48 mmol/g = 211% sorbent mass → target REFUTED
H_004 cost-floor            🟡 PARTIAL     25× gap learnable; $24/ton endpoint optimistic
H_005 honeycomb-geometry    🟢 SUPPORTED   hexagon = min-wall tiler (not the global min)
H_006 numerology-predictor  🟢 SUPPORTED   3/6 lattice→target identities physically impossible
H_007 chip-adc-resolution   🟢 SUPPORTED   12-bit ADC ~7 bits short of ppb sensing
H_008 transmute-energy      🟢 SUPPORTED   CO₂→C reduction 20× capture floor; $1M/ton not Mt-scale
H_009 planetary-scale       🟡 PARTIAL     100 Gt/yr mass-coherent; ~900 EJ/yr energy + ocean walls
H_010 tsa-regeneration      🟢 SUPPORTED   sensible heat ~100 kJ/mol = the headroom mechanism
H_011 sc-co2-compression    🟢 SUPPORTED   ~11.9 kJ/mol to 12 MPa (supercritical OK)
H_012 sorbent-binding-opt   🟢 SUPPORTED   Sabatier optimum ~50 kJ/mol (coverage vs regen)
H_013 plant-air-throughput  🟢 SUPPORTED   ~1.3e12 m³ air/yr at 1 Mt/yr (flue 286× less)
H_014 net-negativity        🟢 SUPPORTED   fossil grid futile; breakeven 0.40 kgCO₂/kWh
H_015 storage-capacity      🟢 SUPPORTED   void ~9× demand → not the bottleneck
H_016 humidity-coload       🟢 SUPPORTED   air carries 37–170× more H₂O than CO₂
H_017 reference-match       🟢 SUPPORTED   harness PREDICTS measured Mg-MOF-74 DAC data
H_018 systems-ref-match     🟢 SUPPORTED   harness PREDICTS measured Gen3 energy/cost
H_019 synthesis-frontier    🟢 SUPPORTED   frontier 12.3× ABOVE the 2nd-law floor (capstone)
H_020 nnr-figure-of-merit   🟢 SUPPORTED   free-energy paths 13–90× over electric DAC (NOVEL metric)
H_021 portfolio-no-winner   🟢 SUPPORTED   no path wins all 4 axes → removal is a portfolio
H_022 dac-niche-concentrated 🟢 SUPPORTED  electric = point-source (flue 286× less air), not dilute air
H_023 abatement-before-removal 🟢 SUPPORTED clean kWh displaces fossil first while grid > 0.67 kg/kWh
H_024 two-frontiers         🟢 SUPPORTED   DAC leads MATURITY frontier, not EFFECTIVENESS frontier
```

**"The impressive frontier was electric DAC, wasn't it?"** — yes, and H_024 shows why that's only
half true: electric DAC leads the **engineering-maturity** frontier (most deployed, the 12.3× ladder
H_017–H_019 validated) but **trails the effectiveness-per-active-energy frontier** on a fossil grid
(argmax flips to the artificial leaf). H_017–H_019 measured maturity and over-broadly called it "the"
frontier — an honest self-correction (their numbers stand). "Most advanced" ≠ "most effective now".

**"Is electric DAC the right path?"** (the H_020 implication) → three verified answers: (H_021)
no path dominates all of energy/rate/footprint/permanence, so it's a **portfolio** not a winner;
(H_022) electric capture is **mis-targeted not wrong-tech** — point-source/flue (286× less air) is
its niche, dilute air on a fossil grid is not; (H_023) while the marginal grid plant emits >0.67
kgCO₂/kWh, a clean kWh **avoids more by displacing fossil than DAC removes** — abatement before removal.

**The novel result (H_020):** since no *mechanism* is new, the novelty is a **method** — a unified
cross-family figure of merit (net CO₂ per *active grid* energy on a realistic fossil grid). On it,
free-energy paths overwhelmingly dominate electric DAC: **enhanced weathering 13×, passive
moisture-swing 44×, artificial leaf 90×** — because electric DAC's net removal collapses on a dirty
grid (H_014) while free-energy paths are grid-independent. Honest: the gap shrinks to ~5× on a clean
grid, and it is the *energy* axis only (DAC still wins on rate/footprint).

**Beyond the frontier (H_019 capstone):** composing every verified primitive into one total-energy
model shows the current research best (Climeworks Gen3, 1500 kWh/ton) sits **12.3× above the
irreducible thermodynamic floor (122 kWh/ton)** — and the *entire* gap is the addressable
regeneration sensible-heat term. The synthesis prescribes the route to the floor: high working
capacity + heat recovery (→222) + swing-mode/conversion path (→128 kWh/ton). A forward design
target with a verified component decomposition, ~6–12× below today's best.

**Closed-form harness exhausted at H_016** (16 cards: 14 🟢 / 2 🟡). Every spec claim numerically
falsifiable from thermodynamics/arithmetic at $0 is covered. A *실측전 research* literature pass
(`state/research-pass-2026-06-27.md`) over the remaining questions **confirms the harness and
justifies no expensive compute**: Climeworks' own 2030 target (~$250–350/ton captured) is ~10× the
spec's $24/ton (validates H_004); arXiv:2501.04825 derives the same thermodynamic CO₂/energy bound
across 11,660 MOFs (validates H_010/H_012); moisture-swing DAC confirms H_016's water-as-resource
limit. The remaining gaps (real sorbent uptake, cycle-life, bottom-up CAPEX) are **$0
data-ingestion of public datasets**, not new compute.

**Frontier crossed (H_017 materials + H_018 systems):** that data-ingestion step is now done. The
closed-form harness **predicts measured reality from first principles** on both axes — *materials*
(H_017: bare Mg-MOF-74 at 34.3 kJ/mol → θ≈4e-4 at DAC vs ≈0.09 at flue, matching <1 vs 3.67 mmol/g;
48 mmol/g = 24× measured best) and *systems* (H_018: Gen3's confirmed 1500 kWh/ton → headroom 12.3×,
breakeven 0.667 kg/kWh = 1.67× the 9 GJ/ton value, $24/ton = 12.5× below the 2030 $300/ton target).
The self-contained floors are validated against measured data. The remaining frontier (H_019+, still
$0 data-ingestion) is per-sorbent kinetics/cycle-life/CAPEX line items; expensive DFT/GPU stays unjustified.

Two honest threads: (1) the **real physics** wins (floor, headroom + its sensible-heat
mechanism, honeycomb, compression, binding optimum, air-handling) hold *without* invoking
{2,4,12,24} — and they reframe the DAC walls as engineering/investment (working capacity, heat
recovery, fan power), not thermodynamic ceilings. (2) The **n=6 numerology** attaches equally
clean identities to impossible targets (48 mmol/g, $24/ton, 12-bit→ppb, $1M/ton-at-scale, 100
Gt/yr) — so every lattice-derived number must clear a physics bounds-check first
(`ARCHITECTURE.json` → `convergence.records`).

- `HYPOTHESES/` — `REGISTRY.jsonl` + one rich card per hypothesis (`cards/H_*.md`). The verified
  `H_0xx` verified chain (19) + a graduated `H_A*` track (11 SF-origin cards whose falsifiable kernels
  were **all run** — 모두 검증 — landing 2 🟢 / 3 🟡 / 6 🔴). The 6 negatives (centrifuge KE 644× floor,
  CO₂ frost −143°C, laser bond 28× floor, gas-phase O₂ magnet, naive photoswitch, air-clathrate) are the
  negative space; survivors: enhanced weathering + artificial leaf (🟢), vortex/electro-swing/breathing
  concrete (🟡). Full landscape in `state/sf-brainstorm-2026-06-27.md`. A prior-art audit
  (`state/novelty-check-2026-06-27.md`) found **0/11 mechanisms genuinely novel** — all are existing
  research fields; the novel contribution is the *unified falsifiable verification*, not the ideas.
- `tool/carbon_capture.py` — shared deterministic harness (separation floor, headroom,
  gravimetric bound, honeycomb P/√A, falsifier ledger).
- `state/H_*/` — per-hypothesis run script + `result.json`.

## Structure

```
carbon-capture/
├─ src/              — source code
├─ HYPOTHESES/       — pre-register → falsify → run → verdict (REGISTRY.jsonl + cards/H_*.md)
├─ tool/             — shared deterministic harness (carbon_capture.py)
├─ state/            — all work artifacts (experiments · bench · verification), git-tracked
│                      n6-carbon-capture-spec.md = imported HEXA-CCUS origin spec
│                      H_*_<date>/ = per-hypothesis run + result.json
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
