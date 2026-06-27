# Changelog

All notable changes to carbon-capture. Append-only; newest on top.

## 2026-06-27 — third hypothesis batch (H_010–H_013): process/storage/sorbent/plant physics

- Four pre-registered hypotheses (each 6/6 falsifiers) deepening the *real-physics* thread —
  these reframe the DAC walls as engineering, not thermodynamic ceilings (goal: 고갈시까지 심화):
  - **H_010** tsa-regeneration-heat 🟢 SUPPORTED — the 200→20 kJ/mol gap is mostly TSA sensible
    heat (~100 kJ/mol; exactly ~200 at working-capacity 0.5 mol/kg), ∝ 1/working-capacity →
    the mechanism behind the H_002 headroom; levers = working capacity + heat recovery.
  - **H_011** sc-co2-compression 🟢 SUPPORTED — 12 MPa pipeline compression ~11.9 kJ/mol (0.62×
    the capture floor), and 12 MPa is correctly supercritical (> Pc 7.38 MPa); ln-pressure scaling exact.
  - **H_012** sorbent-binding-optimum 🟢 SUPPORTED — Sabatier window ~45–55 kJ/mol: θ(40)≈0.004
    (weak fails at 400 ppm), θ(60)≈0.93 (strong fills but owes E_ads back at regeneration).
  - **H_013** plant-air-throughput 🟢 SUPPORTED — 1 Mt/yr = 250× Climeworks (checks), binding duty
    is air handling ~1.3e12 m³/yr; flue gas (12% CO₂) needs 286× less → DAC's wall is moving air.
- Harness +4 primitives: `regeneration_sensible_heat`, `isothermal_compression_work`,
  `langmuir_coverage`, `air_volume_per_ton_co2`.
- `REGISTRY.jsonl`: +4 (all 🟢; now 13 total). Cards `H_010..H_013` + run/`result.json` under `state/`.
- `ARCHITECTURE.json` lockstep: `verification` node → 13 verdicts; `L1.process` (sensible-heat
  mechanism) and `L4.plant` (compression + air-handling) updated with their verified physics.

## 2026-06-27 — second hypothesis batch (H_007–H_009) via /afg

- Three more pre-registered hypotheses across the upper stack (each 6/6 falsifiers, deterministic):
  - **H_007** chip-adc-resolution 🟢 SUPPORTED — a 12-bit (σ) ADC quantizes 420 ppm into 103-ppb
    steps, ~6.7 bits short of the ~18.7 needed for ppb sensing; reachable only via a ~4 ppm span or
    sigma-delta. (`σ = 12-bit → ppb over ambient` refuted.)
  - **H_008** transmute-energy-floor 🟢 SUPPORTED — CO₂→solid-carbon reduction floor is 32.8 GJ/ton-C
    (8.94 GJ/ton-CO₂) = 20× the capture thermodynamic floor, so conversion is the energy-dominant step;
    $1M/ton × 1 Mt/yr = $1000B/yr ≈ 1000× the graphene market. ("free value bonus at scale" refuted.)
  - **H_009** planetary-scale 🟡 PARTIAL — 140 ppm = 1095 Gt CO₂, /12 yr = 91 Gt/yr (mass-coherent with
    the ~100 Gt/yr claim), but real-DAC energy ~900 EJ/yr > global primary (~600 EJ/yr) and ocean
    re-equilibration needs ~2× more → gated on the H_001/H_002 efficiency thesis.
- Harness (`tool/carbon_capture.py`): added `bits_for_resolution` (H_007), `carbon_reduction_energy_floor`
  (H_008), `ppm_to_gt_co2` (H_009) + constants `M_C`, `DH_F_CO2`, `GT_CO2_PER_PPM`.
- `REGISTRY.jsonl`: +3 lines (🟢×2, 🟡×1; now 9 total). Cards `H_007..H_009` + run/`result.json` under `state/`.
- `ARCHITECTURE.json` lockstep: `verification` node now lists 9 verdicts; `convergence.records` extended
  with the H_007–H_009 numerology failures; `L3.chip` / `L5.transmute` flagged with their verified limits.

## 2026-06-27 — first hypothesis batch (H_001–H_006) generated + verified

- Generated and ran the first 6 pre-registered hypotheses (each 6/6 falsifiers, deterministic,
  stdlib-only). Verdicts (verbatim stdout pasted in each card, `result.json` under `state/`):
  - **H_001** separation-floor 🟢 SUPPORTED — `W_min(420 ppm) = 19.275 kJ/mol`, monotone-rising
    as air gets more dilute; flue ~3.7× easier; near-pure → ~0.
  - **H_002** energy-headroom 🟢 SUPPORTED — headroom 10.4×(spec)/20×(Climeworks 8.8 GJ/ton)/
    7.8×(next-gen), all inside the pre-registered 3–30× band, none < 1×.
  - **H_003** sorbent-capacity-bound 🟢 SUPPORTED (target refuted) — 48 mmol/g (= J₂·φ) = 211% CO₂
    by sorbent mass, 4.8× best-case / 32× in-condition → physically unreachable.
  - **H_004** cost-floor 🟡 PARTIAL — 25× gap learning-curve-plausible (~16 doublings @ 18% LR),
    but the $24/ton (= J₂) endpoint sits below the $50/$100 reference floors (unverified-optimistic).
  - **H_005** honeycomb-geometry 🟢 SUPPORTED — hexagon is the min-wall cell among plane-tiling
    regular polygons {3,4,6}; honest limit held (n=12 lower → not the global min).
  - **H_006** n6-numerology-predictor 🟢 SUPPORTED (skeptic holds) — 3/6 lattice→target identities
    physically implausible + physics-blind relabel matches 5/5 → the n=6 lattice is a decorative
    label, not a predictor.
- Harness (`tool/carbon_capture.py`): added `co2_mass_fraction` (gravimetric bound, H_003) and
  `perimeter_area_ratio` (honeycomb P/√A, H_005); `M_CO2` constant.
- `HYPOTHESES/REGISTRY.jsonl`: 6 registry lines (tiers 🟢×5, 🟡×1). Cards `H_001..H_006` + run
  scripts/`result.json` under `state/H_00*_2026-06-27/`.
- `ARCHITECTURE.json` lockstep: `convergence.records[numerology-not-physical]` (verify lattice
  numbers against physics before goal-setting); `L0.sorbent` 48 mmol/g flagged unreachable;
  `thesis.cost-floor` $24/ton flagged optimistic; `verification` node lists the 6 verdicts.

## 2026-06-27 — import echoes provenance excerpt

- Added `state/echoes-carbon-capture-excerpt.md`: the echoes-side surface entry for carbon
  capture (HEXA-Earth "Environment Toolkit" toolkit + closure rows, multilingual mirrors,
  + concrete-mineralization cross-link), imported from `dancinlab/echoes` README. Seed of
  record alongside the deep `state/n6-carbon-capture-spec.md`; CLAUDE.md gotcha updated.

## 2026-06-27 — hypothesis-verification system

- Scaffolded `HYPOTHESES/` (anima-parity): `CLAUDE.md`, empty `REGISTRY.jsonl`,
  `cards/_TEMPLATE.md` (domains sorbent…system). Ready for the first pre-registered card.
- Added repo-root shared harness `tool/carbon_capture.py` (stdlib-only): Sherwood
  separation floor `min_separation_work`, `energy_headroom`, capacity/cost/annual ratios,
  + `Falsifier`/`evaluate` ledger. Smoke-test reproduces the spec: W_min(420 ppm) ≈
  19.27 kJ/mol ≈ J₂−τ, and the 24×/25×/250× n=6 ratios. `tool/CLAUDE.md` folder guide.
- `ARCHITECTURE.json`: added the `verification` node (HYPOTHESES + tool) in lockstep.

## 2026-06-27 — repo scaffold

- Initialized `dancinlab/carbon-capture` mirroring the `dancinlab/lumen` / `dancinlab/rtsc`
  skeleton: `src/`, `state/`, `ARCHITECTURE.json` + `architecture.html` viewer + `serve.py`,
  `CLAUDE.md`, `CHANGELOG.md`, `.gitignore`, `.harness/`.
- Imported the HEXA-CCUS origin spec from `dancinlab/hexa-grid` (`CARBON-CAPTURE.md`,
  ~17k lines) into `state/n6-carbon-capture-spec.md` as the seed of record.
- Authored `ARCHITECTURE.json` SSOT: 7-level HEXA-CCUS stack (L0 sorbent → L6 universal),
  n=6 lattice (φ=2 · τ=4 · σ=12 · J₂=24), distilled from the imported spec.
