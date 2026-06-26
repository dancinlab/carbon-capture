# Changelog

All notable changes to carbon-capture. Append-only; newest on top.

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
