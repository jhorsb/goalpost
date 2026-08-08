# Pre-registration — audit #3: causal recourse validity (2026-08-08)

**Status: REGISTERED, NOT RUN.** Committed before any audit-#3 measurement
exists. Nothing below may be revised after the first live call of this
audit; deviations require a dated DECISIONS.md entry stating what changed
and why, before results are reported.

## Question

Audits #1–#2 measured whether a screening system's advice *repeats*. This
audit measures whether it *works*, and whether advice drawn from different
runs of the same system on the same candidate differs in measured
effectiveness. The claim under test, stated before data:

> H1 (differential effectiveness): for at least one selected case, two
> advice items produced by different runs on the identical CV differ in
> placebo-adjusted effectiveness by ≥ 3/5.

Existence-level claims only, as throughout this project. No rate claims.

## System under test

The audit-#1 pipeline design exactly as previously measured:
`hs-resume-screener` served by `gpt-oss-120b` on Cerebras
(`params.pipeline: hs-resume-screener`, upstream sha `49dc41a…`), at its
as-shipped T=0.7. Chosen because its recourse is **candidate-directed**
(improvement recommendations); target #2 is ineligible — its advice
addresses the recruiter and cannot be implemented as a CV edit.

## Corpus: `corpora/causal-v1` (derived; fixes D-050 before it can bite)

Derived deterministically from `starter-v1` by a committed script:
1. Restrict to the selected cases (below).
2. Prepend to each CV a single pinned line: `CV last updated: 1 September
   2024.` — the as-of date the corpus's relative dates were authored
   against. This freezes the date semantics that D-050 showed drifting;
   the same line appears in every arm, so it cannot differentiate them.
3. No other change.

## Case selection (mechanical, over committed evidence)

Rule, frozen: every `starter-v1` **borderline-band** case whose committed
audit-#1 record (`realtarget-hs-screener-002-gptoss`) shows modal decision
`reject` OR modal agreement < 1.0. Applying the rule today yields **8
cases** (recorded so the rule cannot drift): sc-data-analyst-02,
sc-data-analyst-04, sc-frontend-developer-02, sc-frontend-developer-04,
sc-project-manager-02, sc-project-manager-04, sc-support-team-lead-02,
sc-support-team-lead-04.

## Advice-item selection (mechanical, per case)

From the case's five committed audit-#1 runs, at the cluster level of the
frozen taxonomy:

- **CONSENSUS item:** the advice cluster appearing in the most runs
  (tie → alphabetical by cluster id).
- **SINGLETON item:** an advice cluster appearing in exactly one run
  (fewest-runs; tie → alphabetical). If no singleton exists, the
  least-frequent non-consensus cluster.

This pairing operationalises the lottery question directly: the advice
everyone gets versus the advice one run happened to produce.

## Arms (per case; N = 5 runs each, as-shipped settings)

1. **BASELINE** — causal-v1 CV, unedited.
2. **PLACEBO** — one appended line of comparable length implementing no
   advice: `Interests: long-distance walking; member of a local book
   club.` (identical text every case; controls for any-edit and
   length effects).
3. **EDIT-C** — consensus item implemented.
4. **EDIT-S** — singleton item implemented.

640 pipeline stages ≈ free-tier SUT; extraction ≈ paid. Budget cap
**$10.00**, block-boundary enforcement as always.

## Edit protocol (the part an adversary attacks; frozen dose table)

Edits are appended or minimally substituted lines implementing exactly one
advice cluster at a **fixed, stated dose**. Doses for the recourse
taxonomy's clusters:

| cluster | dose (verbatim template) |
|---|---|
| certification | add: `CERTIFICATIONS: <named cert from the advice>, completed August 2024.` |
| skills / tools | add under SKILLS: `<named skill> — working proficiency, used in production since 2023.` |
| experience | change current-role start date 12 months earlier (dose: +12 months, stated in the diff) |
| education | add: `Currently enrolled: <named course>, part-time, completing 2025.` |
| portfolio / evidence | add: `Portfolio: <artefact named in the advice> available at portfolio.example.invalid.` |
| domain exposure | add to current role bullets: `Supported <named domain> projects in collaboration with the <domain> team.` |
| communication / soft skills | add: `Delivered monthly findings presentations to non-technical stakeholders.` |
| other / NOVEL clusters | nearest template above; mapping recorded in the diff |

Rules: one item per edit; smallest text change the template allows; no
rewriting of existing content beyond the experience date; **every diff
committed before the first measurement run**; each diff independently
checked (Codex, checklist: implements the named item, nothing else,
correct dose) with the check logged in DELEGATION.md.

## Outcomes and analysis (frozen)

- Per arm: acceptance count /5, from the decision field of the frozen
  extraction lens (v3; primary reader gpt-4.1, declared fallback gemma —
  both certified for decisions at 1.000 on this system's prose).
- **Effectiveness of an edit** = accept(edit)/5 − accept(PLACEBO)/5.
- **Differential effectiveness (per case)** = |effect(EDIT-C) −
  effect(EDIT-S)|. H1 is supported if ≥ 3/5 for at least one case;
  the full distribution is reported either way.
- Gate: identical D-012 machinery; decisions require lens decision
  self-agreement ≥ 0.90 measured on this audit's own transcripts. If both
  declared lenses fail: WITHHELD, final.
- Secondary, exploratory (labelled as such, no claims): post-edit advice
  recorded; baseline-vs-committed-audit-#1 decision comparison quantifies
  the as-of-line's own effect.

## Pre-named confounds and their controls

- *We author the edits* → frozen dose table, pre-committed diffs,
  independent mechanical check, all diffs published.
- *Any edit might shift verdicts regardless of content* → placebo arm is
  the comparator, not baseline.
- *Advice underspecifies magnitude* → fixed doses above; results are
  claims about advice **at these stated doses** only.
- *Stochastic outcomes* → effectiveness is a /5 rate, never a boolean;
  n=5 granularity is disclosed in every figure.
- *Corpus date drift (D-050)* → as-of line pinned in all arms.

## What this audit does NOT claim

No rate claims beyond the 8 cases; no claim that any advice is good or
bad career guidance; no fairness or accuracy claims; no claims about the
upstream author (same anonymity and disclosure norms as audits #1–#2 —
the response window and D-024 apply unchanged).
