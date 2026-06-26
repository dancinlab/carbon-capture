# carbon-capture

Engineering CO₂ capture-storage-conversion as a designed system rather than a single
adsorber — the **HEXA-CCUS** architecture. Carbon (Z=6) anchored, an 8-stage capture
pipeline spanning atomic to stellar scale, driving the energy/cost floor of pulling CO₂
out of the air toward its thermodynamic limit (≈20 kJ/mol) instead of today's ≈200 kJ/mol
wet-amine rigs.

## Structure

```
carbon-capture/
├─ src/              — source code
├─ state/            — all work artifacts (experiments · bench · verification), git-tracked
│                      n6-carbon-capture-spec.md = imported N6/HEXA-CCUS origin spec
├─ ARCHITECTURE.json — final architecture SSOT (JSON `children` tree, update-in-place)
├─ architecture.html — human viewer for the JSON (run `python3 serve.py`)
└─ CHANGELOG.md      — history (append-only)
```

## Rules

- Scope is the **capture-storage-conversion system**, not one sorbent: DAC single-stage
  rigs are the first instance, not the boundary — the 8-stage chain is the unit of design.
- Artifacts go under `state/` only (commons preserve-state). No scattered report/notes dirs.
- Code/design change → update `ARCHITECTURE.json` in lockstep; log in `CHANGELOG.md`.
- **Research before real measurement (실측전 research).** Before renting compute or running an
  expensive real measurement (DFT / sorbent screening / GPU pod / long bench), do a literature
  research pass FIRST — the answer may already be in the literature, or a cheap proxy may
  suffice. Only spend on real compute after research justifies it.

## Gotchas

- Imported origin docs under `state/` are seeds of record, NOT the SSOT (the live design
  SSOT is `ARCHITECTURE.json`). Distill from them into the tree; don't edit them to track
  current design:
  - `state/n6-carbon-capture-spec.md` — the deep spec from `dancinlab/hexa-grid`
    (CARBON-CAPTURE.md, ~17k lines).
  - `state/echoes-carbon-capture-excerpt.md` — the echoes-side surface entry
    (HEXA-Earth "Environment Toolkit" toolkit/closure rows + multilingual mirrors).
