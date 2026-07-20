# Goalpost

**Goalpost measures whether an AI screening system's advice stays put.**

When an automated system screens a job application, three things come back:
a decision, the reasons for it, and — implicitly or explicitly — what the
candidate would need to change to succeed. Goalpost asks each system the
same question many times and measures how much each of those three parts
moves: **Decision Stability**, **Reason Stability**, and the headline,
**Recourse Stability**.

Imagine a sat-nav that always tells you *why* you haven't arrived — "you're
40 miles out" — but gives you contradictory directions every time you ask
how to get there. The explanation is consistent; the route is noise.
Goalpost measures whether an automated decision system is that sat-nav:
whether its "here's what you'd need to change" advice stays put, or whether
the goalposts move every time you look. The people most affected by these
systems — job applicants, loan applicants, benefits claimants — are exactly
the people who need explanations to be *actionable*, not decorative.

The method descends from an undergraduate Honours dissertation
(Horsburgh 2026) that found LLM-generated screening explanations were far
more stable in their *reasons* (Jaccard ≈ 0.89) than their *recourse
advice* (≈ 0.36) — a gap that persisted at temperature zero. Goalpost
generalises that instrument to audit any LLM screening configuration
end-to-end. See [METHODOLOGY.md](METHODOLOGY.md) for the lineage and every
deviation.

## What an audit produces

- **Transcripts** of every API call — the audit evidence, committed;
- **A one-page plain-language report** (Markdown + HTML): one headline
  number per system with spread, verbal anchors from a versioned artifact,
  and a "what this doesn't tell you" box;
- **Machine-readable metrics** (JSON) with full provenance on every number
  (corpus hash, config identity, version of every pipeline stage);
- **A comparison table** when auditing multiple systems, with tie-bands —
  overlapping spreads are never oversold as a ranking.

## Quickstart

```sh
git clone <this repo> && cd algorithmic-audit-tool
uv sync
cp .env.example .env        # add ONE credential — any provider, or none:
                            # Anthropic / OpenAI native, any OpenAI-compatible
                            # endpoint (OpenRouter, Together, Groq...), or a
                            # local Ollama (no key at all)
./goalpost.sh audit --config example.yaml --dry-run   # plan + cost, no calls
./goalpost.sh audit --config example.yaml             # live, hard budget cap
```

Every audit is resumable (`goalpost resume <audit-dir>`) and re-scoreable
offline for free — everything downstream of transcripts is a pure function
of files on disk.

## Cost guardrails

`--dry-run` prints the call plan and cost estimate before anything runs; a
hard `max_spend_usd` cap is enforced at block boundaries mid-flight; a
content-addressed cache makes re-runs and resumes free. The first full
validation run (3 models × 25 cases × 5 repeats) cost $0.28.

## Honest limitations

- **Repeat-stability is not accuracy.** A system can be perfectly
  consistent and perfectly wrong. Goalpost measures consistency only.
- **This is not a fairness audit.** Protected-attribute testing is
  deliberately out of scope for V1 — it deserves its own careful design,
  not a side door.
- **Normalisation does real work.** Reported stability depends on a
  committed, versioned synonym taxonomy; reports always show the
  raw → normalised → clustered ladder so that lift is visible, and every
  mapping is logged for human review.
- **Freeform mode is gated.** Auditing a system through a free-text
  extractor adds measurement noise; numbers are only reported when the
  extractor passes a pre-registered self-agreement gate, and then only as
  lower bounds.
- **Authorised targets only.** V1 audits configurations the operator
  controls (provider, model, prompt, parameters). Auditing third-party
  commercial products is out of scope pending terms-of-service review.

## Repo map

Method: [METHODOLOGY.md](METHODOLOGY.md) ·
extraction from the dissertation: [METHODOLOGY_EXTRACTION.md](METHODOLOGY_EXTRACTION.md) ·
design: [DESIGN.md](DESIGN.md) · decision log: [DECISIONS.md](DECISIONS.md) ·
validation results: [VALIDATION_NOTES.md](VALIDATION_NOTES.md) ·
delegation ledger: [DELEGATION.md](DELEGATION.md) ·
status: [STATUS.md](STATUS.md).

Private repository; no licence granted yet.
