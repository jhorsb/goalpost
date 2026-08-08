# Pre-registration — audit #2, target `csa-screening-agent` (2026-08-08)

Committed BEFORE the first target transcript exists. Nothing below may be
revised after the first live SUT call; deviations require a new dated
entry in DECISIONS.md that says exactly what changed and why.

## Target

Pinned in `goalpost.upstream_csa` (sha `707e6ab`, content sha256
`195eee21…`, MIT). Three-stage chain mirrored in `goalpost.csa_client`
(D-036), quirks included; divergences disclosed there.

## The held-out extractor commitment (the D-027 fix, now protocol)

- **Extraction lens frozen as of this commit:** extractor v3
  (`EXTRACTOR_VERSION 3.0.0`, prompt hash per provenance) with
  `gpt-4.1-2025-04-14`. Declared fallback lens, also frozen: the same v3
  prompt with `gemma-4-31b` (Cerebras). Both lenses pre-date this target
  and neither was developed on any transcript of it.
- **No extraction-rule development on target transcripts.** If the gate
  fails on both declared lenses, the result is REPORTED AS WITHHELD.
  There will be no v4-extractor rebuild inside this audit. (Audit #1
  rebuilt its extractor mid-audit under D-012's permitted revision; the
  selection effect that created is what this protocol exists to prevent.)
- Self-agreement is measured on target transcripts as always — the gate
  is a measurement, not development.

## Decision-label mapping (fixed now, from the upstream's prompt text)

The pipeline's verdict vocabulary is "Strong Yes / Yes / Maybe / No"
(recommendation-stage prompt). The frozen extractor maps: recommends →
`accept`; recommends against → `reject`; neither → `unclear`. Expected
coercion: Strong Yes and Yes both → accept; No → reject; Maybe →
unclear. Consequences, accepted in advance:

- decision stability is measured at accept/reject/unclear granularity;
- a Strong Yes ↔ Yes flip does NOT count as a decision flip — measured
  decision instability is therefore a LOWER BOUND on verdict-tier
  instability;
- tier-level flips may additionally be examined descriptively from the
  raw transcripts, labelled as uncertified observation.

## Configuration

- Corpus: `corpora/starter-v1-csa` — starter-v1 with `job_spec_text`
  replaced by the frozen role requirements JSON
  (`phase7/job_requirements/`, transcribed once from the job specs;
  education keys omitted because no spec states education requirements —
  transcription does not invent). CV text and case ids unchanged.
- Conditions: N = 5 repeats × 25 cases. The pipeline hardcodes its own
  per-stage temperatures (0.0 / 0.0 / 0.3); the condition temperature is
  recorded as 0.3 (the verdict-carrying stage's value) and NOT forwarded.
- Served model (disclosed substitution): upstream pins
  `claude-3-5-sonnet-20241022`, which no provider serves (no claude-3.x
  in `/v1/models`, 2026-08-08). Substitute: **`claude-sonnet-4-5-20250929`**
  — same model class (Sonnet), the only Sonnet-class snapshot-pinned id
  currently served. The precise claim is therefore: an audit of the
  pipeline's design as served by a current same-class model.
- Canonicaliser: `gpt-4.1-2025-04-14`, taxonomy cv-screening v1.0.0
  (frozen, unchanged from audit #1).
- Budget cap: $10.00, block-boundary enforcement as always.

## What will be reported

Same ladder and gate machinery as audit #1 (D-012/D-023 thresholds
unchanged; no revisions remain). Headline basis: cluster level. All
claims subject to the gate; withheld means withheld.
