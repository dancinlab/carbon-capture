# Research pass — 실측전 research before H_017+ (2026-06-27)

Literature pass (`sidecar research arxiv|web|fetch`) over the `HYPOTHESES.dry-boundary`
open questions, BEFORE spending on any DFT / sorbent-screening / GPU. Purpose: see
whether the literature already answers them, or a cheap proxy suffices (carbon-capture
CLAUDE.md "실측전 research" rule). Conclusion up front: **the literature CONFIRMS the
closed-form harness and justifies NO expensive new compute yet** — remaining gaps are
data-ingestion, not derivation.

## Queries run

- arxiv `direct air capture CO2 sorbent` (n=6)
- arxiv `direct air capture energy regeneration temperature swing` (n=4)
- arxiv `metal organic framework CO2 capture screening metrics` (n=4, no hits)
- web `direct air capture cost per ton 2030 DOE target Climeworks` (n=5)
- fetch `arxiv.org/abs/2501.04825` (Intrinsic Direct Air Capture)

## Findings → impact on the verified hypotheses

### 1. Cost — confirms H_004 (🟡 $24/ton optimistic), strongly
- **Climeworks Generation 3 (2024) targets, by 2030**: ~**$250–350/ton captured**, total
  **$400–600/ton net removal** — an ~50 % cut vs today, via "doubles capacity per module,
  halves energy consumption, increases material lifetime."
  (carboncapturejournal.com, carbonherald.com, climeworks.com/news/2024-year-in-review)
- Impact: even the industry leader's *aggressive 2030* captured-cost goal ($250–350) is
  **~10× the spec's $24/ton (= J₂)**. H_004's "endpoint unverified-optimistic" is validated
  by primary source; no verdict change, citation added.

### 2. Energy — confirms H_002 / H_010 (energy is the lever, being attacked exactly so)
- Climeworks Gen3 explicitly "**halves energy consumption**" as the cost driver → matches
  H_010's claim that regeneration energy (sensible heat ∝ 1/working-capacity) is THE lever,
  and H_002's finite-headroom thesis.
- **Intrinsic Direct Air Capture** (McDannald et al., arXiv:2501.04825, 2025): derives a
  **thermodynamic upper bound on CO₂ captured per energy** and a purity limit from intrinsic
  material properties, applied to **11 660 MOFs**. This is the rigorous academic analog of our
  `tool/carbon_capture.py` floors. Key published insights that VALIDATE our framing:
  - "what matters is the **relative change in uptake along the cycle**" (= working capacity),
    "**selectivity at any one point does not matter**" → exactly H_010 + H_012's thesis.
  - "**start cold** — CO₂ uptake diverges from N₂ at lower T" → consistent with H_012's
    binding-vs-temperature optimum.
- Impact: our closed-form floors are a simplified but directionally-correct proxy for the
  published thermodynamic-bound method. (reference-match: their metric is the open answer key.)

### 3. Water / regeneration mode — confirms H_016 L2 (water as resource, sign can flip)
- **Vacuum Moisture Swing DAC** (Sinyangwe et al., arXiv:2606.26438, 2026) and moisture-driven
  DAC systems (arXiv:2508.02650, 2508.04547) present **low-thermal, water-managed** capture that
  reversibly releases CO₂ on humidity change — sidestepping the H_010 high-temperature sensible-heat
  penalty entirely.
- Impact: directly confirms H_016's pre-registered Limit L2 ("moisture-swing sorbents desorb CO₂
  on wetting; for those water is a resource, not only a parasite"). An active, real research path.

### 4. MOF screening — the open question is being addressed by autonomous labs / datasets
- **Reproducible Sorbent Materials Foundry** (McDannald et al., arXiv:2207.12467, 2022) and the
  11 660-MOF database above show MOF screening is now ML/autonomous-lab + public-dataset driven —
  a **cheap proxy** (published property tables) exists short of running our own DFT.

## Decision (the point of 실측전 research)

- **No DFT / GPU / sorbent-screening spend is justified now.** The literature already answers the
  qualitative open questions and CONFIRMS the harness on every axis we tested (cost optimism,
  energy-as-lever, working-capacity-not-selectivity, water-as-resource).
- **Remaining gaps are data-ingestion, not derivation**: tightening H_003's representative ~1.5
  mmol/g and adding a sorbent-cost/cycle-life hypothesis would need ingesting a public MOF
  property dataset (e.g. the 11 660-MOF table) or Climeworks disclosures — a $0 data task, not
  new compute. That is the natural H_017+ entry point IF pursued.
- Net: the closed-form dry boundary stands; research moved two PARTIAL/limit items from
  "asserted" to "literature-confirmed" without spending.

## Sources (solicited; provenance only — not the SSOT)

- arXiv:2501.04825 — Intrinsic Direct Air Capture (thermodynamic CO₂/energy upper bound, 11 660 MOFs).
- arXiv:2606.26438 — Vacuum Moisture Swing DAC (low-thermal, water-managed).
- arXiv:2508.02650 / 2508.04547 — moisture-driven DAC demonstrations.
- arXiv:2207.12467 — Reproducible Sorbent Materials Foundry (autonomous MOF screening).
- arXiv:2211.00787 — Water-stable / hydrophobically-encapsulated MOFs for ambient-air + wet-flue CO₂.
- Climeworks Gen3 cost targets (2030: $250–350/ton captured, $400–600/ton net) —
  climeworks.com/news/2024-year-in-review; carboncapturejournal.com; carbonherald.com; esgtoday.com.
