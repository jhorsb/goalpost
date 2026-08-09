# Pre-registration — audit #3: causal recourse validity (2026-08-08)

*Post-run status note (2026-08-09, D-054; annotation only — no
registration content below is altered): this audit has since been
EXECUTED under the frozen registration. The pre-run status line below
says "amended once"; it predates amendment A2 (D-053, also pre-first-
call). The in-file amendment log (A1, A2) at the end of this file is
authoritative. Attribution note (D-078): the "external review" behind
A1 was a model-based review — GPT-5.6 Sol Pro, prompted by the author —
recorded here so "external" is not read as "human".*

**Status: REGISTERED, NOT RUN. Amended once (2026-08-08, D-052) —
before any measurement existed — in response to external review; the
amendment log is at the end of this file.** Nothing below may be revised
after the first live call of this audit; deviations require a dated
DECISIONS.md entry stating what changed and why, before results are
reported.

## Question

Audits #1–#2 measured whether a screening system's advice *repeats*. This
audit measures whether it *works*, and whether advice drawn from different
runs of the same system on the same candidate differs in measured
effectiveness. The claim under test, stated before data:

> H1 (differential effectiveness): for at least one selected case, the
> consensus-item and singleton-item arms differ by ≥ 3/5 in acceptance
> rate, **in the same direction, in each of two independent 5-run
> blocks**.

H1 is a direct edit-vs-edit contrast (the placebo algebraically cancels
from any C−S difference; it grounds the per-item effectiveness numbers,
not the differential — this is intended). Under the worst-case null
(both arms Binomial(5, 0.5), no true difference) a single-block ≥3/5
differential occurs with probability 0.109 — family-wise ≈60% over 8
cases, which would certify noise. The replication requirement brings this
to 0.006 per case, ≈4.7% family-wise (exact binomial computation in the
D-052 record). Existence-level claims only, as throughout. No rate
claims.

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

## Arms (per case; as-shipped settings)

1. **BASELINE** (5 runs) — causal-v1 CV, unedited.
2. **PLACEBO-NEUTRAL** (5 runs) — appended: `Interests: long-distance
   walking; member of a local book club.` (any-edit and length control).
3. **PLACEBO-CREDENTIAL** (5 runs) — appended, same section and template
   as treatment edits but content unrelated to any advice given:
   `CERTIFICATIONS: First Aid at Work certificate, completed August
   2024.` Controls for credential-shaped-content-in-credential-sections
   effects. If this arm moves verdicts as much as advised credentials do,
   the advice content is doing nothing — reportable either way.
4. **EDIT-C** (2 × 5-run blocks) — consensus item implemented.
5. **EDIT-S** (2 × 5-run blocks) — singleton item implemented.

35 runs/case × 8 cases = 280 pipeline executions (free-tier SUT);
extraction paid. Budget cap **$10.00**, block-boundary enforcement as
always. Per-item effectiveness uses PLACEBO-CREDENTIAL as primary
comparator for credential-section doses and PLACEBO-NEUTRAL otherwise.

## Edit protocol (the part an adversary attacks; frozen dose table)

Edits are appended or minimally substituted lines implementing exactly one
advice cluster at a **fixed, stated dose**. Doses for the recourse
taxonomy's clusters:

| cluster | dose (verbatim template) |
|---|---|
| certification | add: `CERTIFICATIONS: <named cert from the advice>, completed August 2024.` |
| skills / tools | add under SKILLS: `<named skill> — working proficiency, used in production since 2023.` |
| experience | current-role start date 12 months earlier AND the immediately previous role's end date moved to the month before the new start (chronology preserved; both changes stated in the diff). If this would make the previous role's duration non-positive or collide with its start or with education dates, the case is excluded from experience-dose edits **by rule**, recorded. |
| education | add: `Currently enrolled: <named course>, part-time, completing 2025.` |
| portfolio / evidence | add: `Portfolio of <artefact named in the advice> available on request.` (no URL — a placeholder domain telegraphs fictionality and would create an artefactual penalty) |
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
- **Differential effectiveness (per case)** = accept(EDIT-C)/5 −
  accept(EDIT-S)/5, computed per block. H1 is supported if, for at least
  one case, |differential| ≥ 3/5 **with the same sign in both blocks**;
  the full distribution (all blocks, all cases) is reported either way.
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

## Amendment log

**A2 (2026-08-08, D-053, still pre-first-call; triggered by the mandated
independent diff check, which FAILED 8 diffs).** No measurement exists;
the first derivation was defective, not the design. (1) **Exclusion rule
implemented as specified:** an experience-dose edit is invalid if the
adjusted previous-role duration becomes non-positive, or the new
current-role start falls inside any other role's dates or the education
period. Cases failing this are excluded from experience-dose edits by
rule and recorded; H1's family is the cases retaining BOTH valid edits
(family shrinkage only lowers the false-positive rate). (2) **Naming
rule tightened, still mechanical:** if the most frequent raw slug is
generic (contains "relevant"/"additional", equals the cluster name, or
names no concrete artifact), fall back to the most frequent concrete slug
in that case+cluster; if none exists, use the job spec's own
"(desirable)" credential line for the role. Trailing
"certification/qualification" is stripped before templating (no
"certification certificate"). (3) Diffs regenerated and the FULL 16-diff
independent check re-run before any live call — the gate that caught
this stays in force.

**A1 (2026-08-08, D-052, pre-first-call; external review, author-relayed).**
(1) H1 gained a same-sign replication requirement across two independent
blocks — the original single-block ≥3/5 criterion had a ≈60% family-wise
false-positive rate under the worst-case null (reviewer's arithmetic,
verified exactly). (2) H1 restated as a direct C-vs-S contrast; the
placebo's algebraic cancellation from the differential acknowledged as
intended. (3) PLACEBO-CREDENTIAL arm added (same-section, same-template,
irrelevant-content control). (4) Experience dose gained a chronology
rule + rule-based exclusion. (5) Portfolio dose URL removed
("available on request"). Runs 640→280 stages… corrected: 20→35
runs/case; budget cap unchanged.
