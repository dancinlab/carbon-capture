# Changelog

All notable changes to carbon-capture. Append-only; newest on top.

## 2026-06-27 — repo scaffold

- Initialized `dancinlab/carbon-capture` mirroring the `dancinlab/lumen` / `dancinlab/rtsc`
  skeleton: `src/`, `state/`, `ARCHITECTURE.json` + `architecture.html` viewer + `serve.py`,
  `CLAUDE.md`, `CHANGELOG.md`, `.gitignore`, `.harness/`.
- Imported the HEXA-CCUS origin spec from `dancinlab/hexa-grid` (`CARBON-CAPTURE.md`,
  ~17k lines) into `state/n6-carbon-capture-spec.md` as the seed of record.
- Authored `ARCHITECTURE.json` SSOT: 7-level HEXA-CCUS stack (L0 sorbent → L6 universal),
  n=6 lattice (φ=2 · τ=4 · σ=12 · J₂=24), distilled from the imported spec.
