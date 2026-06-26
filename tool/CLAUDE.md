# tool — shared runnable harness for HYPOTHESES

Repo-root machinery that `HYPOTHESES/` hypothesis cards run against. Anima-parity:
shared, reusable code lives here in `tool/`; per-hypothesis run scripts and their
`result.json` live under `state/<hX>_.../` and import from here.

## Key files

- `carbon_capture.py` — deterministic, stdlib-only (`math`) primitives for the
  CO2 capture-storage-conversion (HEXA-CCUS) problem:
  - `min_separation_work(x_co2, temp_k)` — Sherwood/thermodynamic floor `R·T·ln(1/x)`.
  - `energy_headroom(current, floor)` — reduction factor to the separation floor.
  - `capacity_ratio(target, baseline)` — sorbent working-capacity improvement.
  - `cost_ratio(baseline, target)` / `annual_capacity_ratio(...)` — cost & scale-up factors.
  - `Falsifier` + `evaluate(metrics, falsifiers)` — pre-registered falsifier ledger.

## Rules

- **No hidden constants / fitting** — every input is explicit and documented so a
  card's falsifiers evaluate against returned numbers.
- **Deterministic** — no randomness, no network, $0 local. Same input → same output.
- **Pure & reusable** — functions here are shared across cards; hypothesis-specific
  parameters belong in the `state/<hX>/run_*.py` script, not here.

## Gotcha

- Import path: run scripts insert `tool/` on `sys.path` via a repo-root-relative
  path, so they run from anywhere (`python3 state/<hX>/run_*.py`).
