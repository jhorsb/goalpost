# Audit #3 pre-run diff check — the failed first run, verbatim (D-053)

This file is the committed record of the **first, failed run** of the
independent diff check that phase8/PREREGISTRATION-AUDIT3.md mandates
("each diff independently checked") before any live call of audit #3.
D-053 summarised its outcome and noted the verdict table was "preserved
in the Codex session rollout (23:20:05 session)" — i.e. author-held.
The Sol re-verification flagged that as finding N3 (D-079,
phase9/SOL-DISPOSITIONS.md): the check's independence and verdicts were
not re-verifiable from committed evidence. This commit closes that gap.
Everything under "Verbatim record" below is unedited session output.

*Lint note: this file quotes historical, since-corrected phrasings and
verdicts; it is a record that quotes history and is deliberately not in
`tools/claims_lint.py`'s scanned surfaces, on the same rule that exempts
DECISIONS.md and phase9/\*.*

## Provenance

- **Run:** 2026-08-08, 22:18–22:31 UTC (23:18–23:31 BST; rollout
  filenames are local time).
- **Worker:** Codex CLI, model `gpt-5.6-sol`, reasoning effort `ultra`
  (recorded in the rollout's `turn_context`), provider openai,
  originator Claude Code, source vscode, cwd
  `/Users/jamiehorsburgh/Projects/goalpost`.
- **Structure:** one parent thread which spawned three read-only
  subagent threads and assembled their reports into the final verdict
  table. All four rollouts share the parent session id
  `019fe374-e72f-70b0-b473-f6d4420b78f5`.
- **What "independent" means here, mechanically:** a fresh Codex session
  with no conversation history, given only the mandate below; it read
  the four registered inputs itself (PREREGISTRATION-AUDIT3.md,
  item-selection.json, DIFFS.md, cases.yaml) under an enforced
  no-write/no-git constraint, and returned verdicts traceable to file
  lines. It is a different model lineage from the orchestrator that
  authored the briefs (Claude), not a human reviewer, and not
  organisationally independent of the project.
- **D-053's "23:20:05 session":** that timestamp names the first
  subagent thread (diffs 1–8). The assembled 16-row table is the parent
  thread's final message; the parent's rollout filename carries its
  start time, 23:18:37 BST. The citation resolves to this session tree.

Author-held rollout files (`~/.codex/sessions/2026/08/08/`), SHA-256 at
commitment time:

| Thread | Rollout file | SHA-256 |
|---|---|---|
| Parent (assembled table) | `rollout-2026-08-08T23-18-37-019fe374-e72f-70b0-b473-f6d4420b78f5.jsonl` | `e1110bc8b9a7fc513c91d959cfccc12aecb49895c7dda5842b9bea6fa85b9606` |
| `/root/audit_diffs_1_8` ("Aristotle") | `rollout-2026-08-08T23-20-05-019fe376-3f5c-7351-9082-50f8f15d28b5.jsonl` | `2eaeb72ca21f4fdef74cc5c93592babffa072b8666c2711ad66872c91db53e28` |
| `/root/audit_diffs_9_16` ("Ampere") | `rollout-2026-08-08T23-20-13-019fe376-5ebc-7e23-bf33-3055490caa8b.jsonl` | `af54432401faf884f5e31f662acfe40c1aecde712654f2b7e086678db46b8dde` |
| `/root/audit_globals` ("Avicenna") | `rollout-2026-08-08T23-20-18-019fe376-738f-7912-bf3f-67306c6b0631.jsonl` | `f5d029495e4736e83d5f5b9e5db5612625190448a2fe04184ac5c482e99073f4` |

Extraction: the mandate is the parent thread's user turn; the final
report is the parent's `task_complete.last_agent_message` (timestamp
2026-08-08T22:31:11Z); the subagent sections are their
`FINAL_ANSWER` inter-agent payloads, pulled from the JSONL by field
with no editing. One disclosed delta: the parent's raw final message
item embeds a seven-line Codex memory-citation markup block
(`<oai-mem-citation>`, citing MEMORY.md guidance to obey the no-git
constraint) between the verdict table and the invariants section; the
harness strips it from the rendered final answer, and it is omitted
below.

## Reading this table against D-053's "FAILED 8 of 16"

The assembled table marks **13 of 16 rows with at least one failing
column**; three rows pass all three columns (data-analyst-02 editS,
frontend-developer-02 editS, support-team-lead-02 editS). D-053's
"FAILED 8 of 16 diffs" is the set its own clauses (a) and (b) name:

- **(a) three chronology-rule violations** — data-analyst-02 editC,
  frontend-developer-02 editC, frontend-developer-04 editC;
- **(b) five certification-line namings** adding an unregistered
  "certificate" — data-analyst-04 editS, frontend-developer-04 editS,
  project-manager-02 editC, project-manager-04 editC,
  support-team-lead-04 editS.

The other five rows carrying a failing column, not counted in that
summary: two education namings adding an unregistered "course"
(data-analyst-04 editC, support-team-lead-04 editC — the checker's own
adjudication offers a charitable "humanised" reading that downgrades
exactly these two, § 6 below); two implements-item failures on
date-only experience edits (project-manager-02 editS,
project-manager-04 editS, § 7 below); one coherence failure
(support-team-lead-02 editC). So D-053's headline count is a lossy
summary of the table, low under any strict column reading — the
committed record, not the summary, is authoritative.

All thirteen flagged rows were remediated by the same A2 regeneration:
the six experience arms (the three chronology violators plus
project-manager-02 editS, project-manager-04 editS and
support-team-lead-02 editC) are exactly the six rule-based exclusions
in phase8/EXCLUSIONS.md, and the naming rows were regenerated under the
tightened naming rule. The re-run check on the regenerated set returned
GATE PASS 10/10 (D-054).

---

## Verbatim record

### 1. The mandate (parent thread, user turn, 22:18:39 UTC)

<!-- VERBATIM BEGIN: parent user turn -->

<task>You are an independent, read-only verification checker for /Users/jamiehorsburgh/Projects/goalpost, mandated by phase8/PREREGISTRATION-AUDIT3.md's requirement that 'each diff independently checked.' Do NOT modify any file and do NOT run any git commands. This is verification only.

Read these files in full before answering:
- phase8/PREREGISTRATION-AUDIT3.md (the protocol, especially the dose table and the amendment log)
- phase8/item-selection.json (maps which advice item each edit must implement)
- phase8/DIFFS.md (the 16 diffs under review)
- corpora/causal-v1/cases.yaml (the generated arms)

For EACH of the 16 diffs in phase8/DIFFS.md, answer three questions:
1. implements-item: Does the edit implement exactly the named advice item (per item-selection.json) and NOTHING else (no extra unrelated changes)?
2. dose-correct: Is the dose correct per the pre-registration's dose table as amended (experience = +12 months added to the current-role start date, WITH the contiguity rule applied against the previous role's end date; certifications/education/skills/etc. = the stated verbatim templates from the pre-registration)? Check the amendment log in PREREGISTRATION-AUDIT3.md for any dose-table corrections that supersede the original table.
3. coherence: For the two placebo arms and all experience-dose edits, does the resulting CV in cases.yaml remain internally coherent — no date overlaps, no impossible chronology, no duplicated sections that a reader would flag as corrupt?

Also check these global invariants across corpora/causal-v1/cases.yaml:
- Every arm carries the identical as-of line: 'CV last updated: 1 September 2024.'
- Baseline arms differ from the starter-v1 originals ONLY by that as-of line (no other changes).
- The block-B file (the file containing the 16 edit arms) contains exactly those 16 edit arms and nothing else (no extra arms, no missing arms).

Flag anything questionable even if it arguably passes strict criteria — for example, an edit that interacts awkwardly with existing CV content (e.g. a case that already mentions the advised artifact/skill/certification before the edit is applied) is reportable even though it is not something you should fix.</task>

<structured_output_contract>
Produce a verdict table with exactly one row per diff (16 rows), columns in this order: diff id | implements-item (pass/fail) | dose-correct (pass/fail) | coherence (pass/fail) | notes.
The notes column must be terse but must name the specific file/line/field evidence for any fail or flag.
After the table, add a short section 'Global invariants' with pass/fail for: (a) uniform as-of line, (b) baseline arms differ only by as-of line, (c) block-B file contains exactly 16 edit arms.
After that, add a short section 'Flags worth reviewer attention' listing any pass-but-questionable items even if not strictly a fail.
Do not include any narrative outside these three sections. Do not propose fixes or edits — this is verification only.
</structured_output_contract>

<default_follow_through_policy>
Read all four listed files fully before starting. If a diff or arm referenced in DIFFS.md cannot be located in cases.yaml, or if item-selection.json is missing an entry for a diff, treat that as a fail for the relevant question and note the discrepancy explicitly rather than skipping it. Work through all 16 diffs; do not stop early or sample a subset.
</default_follow_through_policy>

<grounding_rules>
Every pass/fail verdict must be traceable to specific text you actually read in the named files (quote or closely paraphrase the relevant snippet in the notes when flagging a fail or a flag-worthy item). Do not infer intent beyond what the pre-registration document and item-selection.json state. If the dose table has been amended, cite the amendment log entry you relied on.
</grounding_rules>

<action_safety>
This is a strictly read-only task. Do not edit, create, or delete any file. Do not run git add/commit/checkout/reset or any other git command. Only use file-reading tools.
</action_safety>
<!-- VERBATIM END: parent user turn -->

### 2. Final assembled report (parent thread, final message, 22:31:11 UTC)

<!-- VERBATIM BEGIN: parent final message -->
## Verdict table

| diff id | implements-item (pass/fail) | dose-correct (pass/fail) | coherence (pass/fail) | notes |
|---|---|---|---|---|
| sc-data-analyst-02 — editC | fail | fail | fail | Date edits do not add named “tableau experience”; Tableau remains only in the prior role. A1 requires exclusion, but arm creates `July 2021 – March 2021`. [diff:5](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:5), [protocol:104](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:104), [A1:162](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:162), [arm:96](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:96) |
| sc-data-analyst-02 — editS | pass | pass | pass | Sole addition exactly instantiates the skills template. Flag: `CLOUD_SKILL` maps to “statistical skills,” already echoed by “Foundational knowledge of statistics.” [selection:5](/Users/jamiehorsburgh/Projects/goalpost/phase8/item-selection.json:5), [protocol:103](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:103), [arm:126](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:126) |
| sc-data-analyst-04 — editC | pass | fail | pass | Artifact fixed as `advanced analytics training`, but arm adds unregistered `course`; not the verbatim named-course substitution. [protocol:100](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:100), [protocol:105](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:105), [diff:47](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:47), [arm:246](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:246) |
| sc-data-analyst-04 — editS | pass | fail | pass | Artifact is `relevant degree or certification`; arm adds unregistered `certificate`. Existing BSc makes the generic new claim potentially duplicative. [protocol:102](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:102), [diff:61](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:61), [arm:276](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:276) |
| sc-frontend-developer-02 — editC | pass | fail | fail | Current role contains the CI/CD item, but A1 requires prior-role adjustment/exclusion. `March 2020 – Present` overlaps the `July 2020 – Feb 2021` internship; moving its end to February 2020 would make it non-positive. [diff:75](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:75), [A1:162](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:162), [arm:423](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:423) |
| sc-frontend-developer-02 — editS | pass | pass | pass | Sole addition exactly matches the registered soft-skills sentence. [protocol:108](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:108), [diff:92](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:92), [arm:462](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:462) |
| sc-frontend-developer-04 — editC | pass | fail | fail | Only registered date fields change, but A1 requires exclusion: prior role becomes `June 2021 – April 2021`, an inverted duration. [diff:106](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:106), [protocol:104](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:104), [arm:618](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:618) |
| sc-frontend-developer-04 — editS | pass | fail | pass | Artifact is `accessibility standards`; arm adds unregistered `certificate`. Flag: skills still say “learning WCAG 2.1.” [protocol:102](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:102), [diff:132](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:132), [arm:657](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:657) |
| sc-project-manager-02 — editC | pass | fail | pass | Artifact is `project management certification`; arm adds unregistered `certificate`. Existing APM PMQ is simultaneously “expected completion August 2024,” creating near-duplication. [protocol:102](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:102), [diff:146](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:146), [arm:798](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:798) |
| sc-project-manager-02 — editS | fail | pass | pass | Named item is “quantified achievements,” but only dates change; existing quantified bullets are untouched. May 2020/April 2020 is positive and contiguous under A1. [diff:160](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:160), [A1:162](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:162), [arm:832](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:832) |
| sc-project-manager-04 — editC | pass | fail | pass | Artifact is `advanced project management certification`; arm adds unregistered `certificate`, producing `certification certificate`. [protocol:102](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:102), [diff:186](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:186), [arm:968](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:968) |
| sc-project-manager-04 — editS | fail | pass | pass | Named item is “senior project lead experience,” but edit merely extends an `Assistant Project Manager` role whose duties remain “supported/assisted.” June 2020/May 2020 satisfies A1 chronology. [diff:200](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:200), [A1:162](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:162), [arm:1002](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:1002) |
| sc-support-team-lead-02 — editC | pass | pass | fail | September 2022/August 2022 satisfies A1, but unchanged profile says “8 months in a supervisory role”; pinned as-of date makes amended tenure approximately two years. [diff:226](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:226), [A1:162](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:162), [arm:1138](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:1138) |
| sc-support-team-lead-02 — editS | pass | pass | pass | Sole addition exactly instantiates the skills template. Flag: “technical depth” is vague for selected `PROGRAMMING_PRACTICE`. [selection:91](/Users/jamiehorsburgh/Projects/goalpost/phase8/item-selection.json:91), [protocol:103](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:103), [arm:1172](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:1172) |
| sc-support-team-lead-04 — editC | pass | fail | pass | Artifact fixed as `education alignment`, but arm adds unregistered `course`; not the verbatim named-course substitution. [protocol:105](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:105), [diff:268](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:268), [arm:1308](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:1308) |
| sc-support-team-lead-04 — editS | pass | fail | pass | Artifact is `formal certifications`; arm adds unregistered singular `certificate`, producing malformed `formal certifications certificate`. [protocol:102](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:102), [diff:282](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:282), [arm:1342](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:1342) |

## Global invariants

- (a) Uniform as-of line — **pass**. All 40/40 main arms contain exactly one identical pinned line; block B is likewise 16/16. [first arm](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:3), [last arm](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:1339)
- (b) Baselines differ only by as-of line — **pass**. All 8/8 baseline CVs equal their starter-v1 originals after removing that prefix; other fields match, aside from the expected `__baseline` arm-ID suffix. [baselines](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:3), [originals](/Users/jamiehorsburgh/Projects/goalpost/corpora/starter-v1/cases.yaml:437)
- (c) Block-B inventory — **pass**. Exactly 16 unique `editC`/`editS` arms, no extras or omissions; every object matches its main-file counterpart. [first](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases-blockB.yaml:3), [last](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases-blockB.yaml:517)
- Placebo coherence — **pass**. All eight neutral and eight credential placebos are exact single-line appends to coherent baselines, with no duplicated sections or chronology changes. [templates](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:75), [example arms](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:33)

## Flags worth reviewer attention

- `sc-data-analyst-02 editS`: `CLOUD_SKILL` resolves to “statistical skills,” already represented in the profile and SKILLS section. [selection:5](/Users/jamiehorsburgh/Projects/goalpost/phase8/item-selection.json:5), [arm:126](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:126)
- `sc-frontend-developer-02 editC` and `sc-frontend-developer-04 editC`: their existing bullets still qualify the advised experience as “limited exposure” and “not a full-scale design system.” [CI/CD arm](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:423), [design-system arm](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:618)
- `sc-frontend-developer-02 editS`: the exact registered sentence is free-floating and has no role or project attribution. [arm:462](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:462)
- `sc-support-team-lead-02 editS`: “technical depth” is not a concrete programming practice or technology, despite being the mechanically selected artifact. [diff:252](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:252)
- The neutral placebo is called a “length control,” but its fixed addition is 64 characters while treatment deltas range from −3 to +95 characters. [protocol:78](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:78), [diffs](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:5)
- First Aid at Work is absent from the selected advice, but is plausibly outcome-relevant for construction project-manager cases whose specifications require health-and-safety familiarity. [placebo rule](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:80), [job specification](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:720)
<!-- VERBATIM END: parent final message -->

### 3. Subagent FINAL_ANSWER — `/root/audit_diffs_1_8` ("Aristotle"), 22:22:48 UTC

<!-- VERBATIM BEGIN: audit_diffs_1_8 FINAL_ANSWER -->
Message Type: FINAL_ANSWER
Task name: /root
Sender: /root/audit_diffs_1_8
Payload:
Read-only audit completed; no Git or writes.

| Diff | Implements item | Dose-correct | Coherent |
|---|---|---|---|
| sc-data-analyst-02 editC | **FAIL** | **FAIL** | **FAIL** |
| sc-data-analyst-02 editS | **PASS?** | **PASS** | **PASS?** |
| sc-data-analyst-04 editC | **PASS** | **PASS** | **PASS** |
| sc-data-analyst-04 editS | **PASS?** | **FAIL** | **PASS?** |
| sc-frontend-developer-02 editC | **PASS?** | **FAIL** | **FAIL** |
| sc-frontend-developer-02 editS | **PASS** | **PASS** | **PASS?** |
| sc-frontend-developer-04 editC | **PASS** | **FAIL** | **FAIL** |
| sc-frontend-developer-04 editS | **PASS?** | **FAIL** | **PASS?** |

Material findings:

- **All three experience edits violate the amended exclusion rule.** The dose requires preserving chronology and excluding cases where the adjusted prior role becomes non-positive or collides with education (`PREREGISTRATION-AUDIT3.md:100-105`).
  - data-analyst-02 editC creates `July 2021 – March 2021`; it also moves the current role into the 2017–2021 education period (`DIFFS.md:5-27`; `cases.yaml:93-98`). It does not substantively add “tableau experience”: Tableau belongs to the now-invalid prior role, not the lengthened current role.
  - frontend-developer-02 editC changes only the current start, leaving a March 2020–Present role overlapping the July 2020–Feb 2021 internship and 2018–2020 education (`DIFFS.md:75-90`; `cases.yaml:420-425`). Applying the required prior-end adjustment would produce Feb 2020 before the internship’s July 2020 start, so the case should be excluded. The existing CI/CD bullet still says exposure is “limited,” hence implements-item is only an operational pass.
  - frontend-developer-04 editC creates `June 2021 – April 2021` and overlaps 2018–2021 education (`DIFFS.md:106-130`; `cases.yaml:615-620`). It does lengthen the role containing design-component-library work, but should have been excluded.

- **Both certification edits fail the “named cert from the advice” requirement** (`PREREGISTRATION-AUDIT3.md:102`):
  - data-analyst-04 editS claims the tautological, non-named credential “relevant degree or certification certificate” (`DIFFS.md:61-73`; `cases.yaml:273-278`).
  - frontend-developer-04 editS claims the generic/non-named “accessibility standards certificate” (`DIFFS.md:132-143`; `cases.yaml:654-659`).
  These weakly implement the topic but not a credible named credential; coherence passes only in the narrow no-contradiction sense.

Pass-but-questionable flags:

- data-analyst-02 editS exactly follows the skills template, but “statistical skills” is semantically mismatched to selected cluster `CLOUD_SKILL` and sits beside “Foundational knowledge of statistics,” weakening internal consistency (`item-selection.json:2-15`; `DIFFS.md:31-44`; `cases.yaml:123-128`).
- data-analyst-04 editC follows the education template, but “advanced analytics training course” is generic rather than a recognisable named course (`DIFFS.md:47-59`; `cases.yaml:243-248`).
- frontend-developer-02 editS exactly matches the soft-skills dose, but the free-floating “findings presentations” claim has no role/project attribution and is weakly contextualised for frontend work (`DIFFS.md:92-104`; `cases.yaml:459-464`).

The selected consensus/singleton clusters match `item-selection.json`, and the eight `DIFFS.md` edits are faithfully present in `cases.yaml`; the defects are in dose validity and substantive/coherence quality, not corpus transcription.
<!-- VERBATIM END: audit_diffs_1_8 FINAL_ANSWER -->

### 4. Subagent FINAL_ANSWER — `/root/audit_diffs_9_16` ("Ampere"), 22:22:35 UTC

<!-- VERBATIM BEGIN: audit_diffs_9_16 FINAL_ANSWER -->
Message Type: FINAL_ANSWER
Task name: /root
Sender: /root/audit_diffs_9_16
Payload:
Read-only audit complete; no Git commands or file changes.

| Diff | Implements item | Dose | Coherence | Finding |
|---|---|---|---|---|
| `sc-project-manager-02 editC` | Pass, questionable | Pass | Pass, questionable | Literal “project management certification” implementation, but the added “project management certification certificate” is not an identifiable credential and sits beside an APM PMQ already “expected completion August 2024.” [DIFFS.md:146](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:146), [cases.yaml:798](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:798) |
| `sc-project-manager-02 editS` | **Fail** | Pass | Pass | Named item is “quantified achievements,” but the edit only changes employment dates; no achievement is added or quantified. Chronology is correctly preserved: May 2020 start, April 2020 previous end. [DIFFS.md:160](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:160), [cases.yaml:832](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:832) |
| `sc-project-manager-04 editC` | Pass, questionable | Pass | Pass, questionable | Literal implementation, but “advanced project management certification certificate” is generic and tautological rather than a named credential. [DIFFS.md:186](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:186), [cases.yaml:968](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:968) |
| `sc-project-manager-04 editS` | **Fail** | Pass | Pass | Extending tenure as an **Assistant Project Manager** does not implement the named “senior project lead experience.” June 2020/May 2020 chronology is correct. [DIFFS.md:200](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:200), [cases.yaml:1002](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:1002) |
| `sc-support-team-lead-02 editC` | Pass | Pass | **Fail** | Correctly extends leadership tenure and preserves chronology, but the CV still says “8 months in a supervisory role” while the amended September 2022 start implies about two years as of 1 September 2024. [DIFFS.md:226](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:226), [cases.yaml:1138](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:1138) |
| `sc-support-team-lead-02 editS` | **Fail** | Pass, literal | **Fail** | “Technical depth — working proficiency” names no programming practice, technology, or concrete skill. It mechanically follows the skills template but does not substantively implement `PROGRAMMING_PRACTICE` and is not a coherent CV skill claim. [DIFFS.md:252](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:252), [cases.yaml:1172](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:1172) |
| `sc-support-team-lead-04 editC` | Pass, questionable | Pass | Pass, questionable | Exact education template, but “education alignment course” is a generic category rather than a recognisable named course. [DIFFS.md:268](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:268), [cases.yaml:1308](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:1308) |
| `sc-support-team-lead-04 editS` | Pass, questionable | Pass | Pass, questionable | Literal implementation, but “formal certifications certificate” does not identify any actual certification and awkwardly converts a plural category into a fictitious-sounding credential. [DIFFS.md:282](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:282), [cases.yaml:1342](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:1342) |

The amended experience-dose rule is at [PREREGISTRATION-AUDIT3.md:104](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:104). All three audited experience-date edits satisfy its arithmetic and chronology requirements; their failures are item validity or resulting coherence, not dose mechanics.
<!-- VERBATIM END: audit_diffs_9_16 FINAL_ANSWER -->

### 5. Subagent FINAL_ANSWER — `/root/audit_globals` ("Avicenna"), structural invariants, 22:25:49 UTC

<!-- VERBATIM BEGIN: audit_globals FINAL_ANSWER 1 -->
Message Type: FINAL_ANSWER
Task name: /root
Sender: /root/audit_globals
Payload:
Read-only audit complete. No files changed and no Git command was run.

Results:

- PASS — as-of invariant. All 40 arms in [cases.yaml](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml) and all 16 block-B edit arms begin with exactly `CV last updated: 1 September 2024.` and contain it once. Main evidence is at `cases.yaml` lines 6, 36, 66 … 1342; block-B evidence at `cases-blockB.yaml` lines 6, 36, 66 … 520. This matches the registered rule at [PREREGISTRATION-AUDIT3.md:41](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:41).

- PASS — baseline derivation. For all eight selected cases, after accounting for the expected `__baseline` case-ID suffix, `cv_text == pinned-line + starter-v1 cv_text`; role, strength band, and job spec are identical. Each CV delta is exactly 36 characters. Baselines are at `cases.yaml` lines 3, 153, 303, 498, 693, 863, 1033, 1203; originals at `starter-v1/cases.yaml` lines 437, 576, 794, 944, 1167, 1312, 1537, 1678.

- PASS — block-B inventory. The file is [cases-blockB.yaml](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases-blockB.yaml). It has exactly the expected 16 unique IDs: eight selected cases × `editC`/`editS`, with no missing IDs, extras, or duplicates. IDs occur at lines 3, 33, 63, 93, 123, 162, 201, 240, 279, 313, 347, 381, 415, 449, 483, 517. Every complete block-B object exactly matches its corresponding edit arm in `cases.yaml`.

- PASS — placebo construction and duplication. For every selected case, `placN` is exactly baseline plus the registered interests sentence, and `placC` is exactly baseline plus the registered First Aid sentence; metadata/job specs are unchanged. Each template occurs exactly eight times, once per case. There are no duplicate full CVs across the 40 main arms. Evidence for the intended templates is [PREREGISTRATION-AUDIT3.md:75](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:75); corpus occurrences are `cases.yaml` lines 38/68, 188/218, 347/386, 542/581, 732/766, 902/936, 1072/1106, 1242/1276.

Important failures/interactions:

- FAIL — three experience edit arms violate the exclusion/chronology rule at [PREREGISTRATION-AUDIT3.md:104](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:104):

  - `sc-data-analyst-02__editC` changes the previous role to `July 2021 – March 2021`, an inverted/non-positive duration: [DIFFS.md:23](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:23).
  - `sc-frontend-developer-02__editC` moves the current role start to March 2020 but leaves the previous internship at July 2020–February 2021, creating overlap. Moving its end to February 2020 as the protocol requires would make that role non-positive, so this case should have been excluded: [DIFFS.md:75](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:75), [cases.yaml:420](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:420).
  - `sc-frontend-developer-04__editC` changes the previous role to `June 2021 – April 2021`, also inverted/non-positive: [DIFFS.md:123](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:123).

- Pass-but-questionable — the neutral placebo is described as a “length control,” but it always adds 64 characters while treatment deltas range from −3 to +95 characters. It is an any-edit control, but not a matched-length control.

- Pass-but-questionable — First Aid at Work is absent from the selected advice, so the credential placebo meets the literal “unrelated to advice” condition. However, it is plausibly outcome-relevant for both construction project-manager cases: their job specs explicitly require health-and-safety familiarity, e.g. `sc-project-manager-02` at [cases.yaml:720](/Users/jamiehorsburgh/Projects/goalpost/corpora/causal-v1/cases.yaml:720). It is therefore not clearly a content-neutral credential placebo for those cases.

- Pass-but-questionable — both placebo additions are intentionally identical across all eight cases. No full-arm duplication exists, but any idiosyncratic semantic effect of “long-distance walking/book club” or “First Aid at Work” is shared across every case rather than averaged over multiple placebo contents.

- Additional treatment interaction: `sc-project-manager-02__editC` appends a generic “project management certification certificate, completed August 2024” immediately after an existing APM PMQ expected in August 2024, creating near-duplication/possible inconsistency: [DIFFS.md:146](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:146).

Material commands used, all read-only:

```sh
wc -l phase8/PREREGISTRATION-AUDIT3.md phase8/item-selection.json phase8/DIFFS.md corpora/causal-v1/cases.yaml
wc -c phase8/PREREGISTRATION-AUDIT3.md phase8/item-selection.json phase8/DIFFS.md corpora/causal-v1/cases.yaml
nl -ba phase8/PREREGISTRATION-AUDIT3.md
nl -ba phase8/item-selection.json
nl -ba phase8/DIFFS.md
nl -ba corpora/causal-v1/cases.yaml | sed -n '<chunk ranges>p'
rg -l --glob '!corpora/causal-v1/cases.yaml' 'sc-data-analyst-02__editC|__editC' .
find corpora/causal-v1 -maxdepth 1 -type f -print
rg -n '^- case_id:' corpora/causal-v1/cases.yaml corpora/causal-v1/cases-blockB.yaml
rg -n '^- case_id: .*__baseline$' corpora/causal-v1/cases.yaml
rg -n '^- case_id: sc-(data-analyst|frontend-developer|project-manager|support-team-lead)-(02|04)$' corpora/starter-v1/cases.yaml
rg -n '^## .* — edit[CS] ' phase8/DIFFS.md
rg -n 'Interests: long-distance walking|CERTIFICATIONS: First Aid at Work' corpora/causal-v1/cases.yaml
awk '/cv_text: "CV last updated:/{print FNR ":" substr($0,1,62)}' corpora/causal-v1/cases.yaml
awk '/cv_text: "CV last updated:/{print FNR ":" substr($0,1,62)}' corpora/causal-v1/cases-blockB.yaml
```

A read-only Python/PyYAML structural check loaded all four requested files in full plus the starter and block-B YAMLs, then checked exact ID sets, uniqueness, full-object equality, pinned prefixes, baseline equality, placebo equality, and duplicate CV counts. Its final output was:

```text
counts 40 16 8
main_set True main_unique True
block_set True block_unique True block_matches_main True
asof_main True asof_block True
baselines_prefix_only True
placN_exact True placC_exact True
full_cv_duplicate_groups 0 placebo_template_counts 8 8
```
<!-- VERBATIM END: audit_globals FINAL_ANSWER 1 -->

### 6. Subagent FINAL_ANSWER — `/root/audit_globals`, naming adjudication, 22:28:18 UTC

<!-- VERBATIM BEGIN: audit_globals FINAL_ANSWER 2 -->
Message Type: FINAL_ANSWER
Task name: /root
Sender: /root/audit_globals
Payload:
Adjudication: under a strict preregistration reading, all seven lines fail exact dose correctness.

Why:

- [PREREGISTRATION-AUDIT3.md:100](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:100) labels these “verbatim template[s].”
- [DIFFS.md:3](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:3) fixes the named artifact mechanically as the selected raw slug, humanised.
- Each relevant heading and `Dose:` line then records that artifact without the extra noun. For example, `project management certification` is fixed at [DIFFS.md:146](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:146), but the generated line uses `project management certification certificate` at line 157.

Thus the placeholder should contain the recorded artifact, not the artifact plus newly authored content:

- Five certification failures: lines 72, 143, 157, 197, and 293 add `certificate`.
- Two education failures: lines 58 and 279 add `course`.

The intended strict substitutions would be, for example:

```text
CERTIFICATIONS: project management certification, completed August 2024.
Currently enrolled: advanced analytics training, part-time, completing 2025.
```

There is a charitable alternative reading: “humanised” is undefined, and adding a category noun can be viewed as grammatical completion of `<named cert>` or `<named course>`. Under that reading, the education forms are reasonably grammatical and could be marked pass-but-questionable. The certification forms are substantially weaker: four produce tautological or malformed phrases such as `certification certificate` or `certifications certificate`, and none identifies an actual named certification.

Recommended audit classification:

- Five certification lines: strict fail, not merely questionable.
- Two education lines: strict fail under locked artifact fidelity; if the project explicitly treats grammatical noun completion as part of “humanised,” downgrade only these two to pass-but-questionable.
- None of the seven is a clean, unambiguous pass from these files alone.

Command used:

```sh
nl -ba phase8/PREREGISTRATION-AUDIT3.md | sed -n '94,109p'
nl -ba phase8/DIFFS.md | sed -n '1,75p'
nl -ba phase8/DIFFS.md | sed -n '128,202p'
nl -ba phase8/DIFFS.md | sed -n '264,294p'
```
<!-- VERBATIM END: audit_globals FINAL_ANSWER 2 -->

### 7. Subagent FINAL_ANSWER — `/root/audit_globals`, experience/implements adjudication, 22:29:11 UTC

<!-- VERBATIM BEGIN: audit_globals FINAL_ANSWER 3 -->
Message Type: FINAL_ANSWER
Task name: /root
Sender: /root/audit_globals
Payload:
The protocol requires both conditions:

1. The selected cluster determines the frozen dose family ([PREREGISTRATION-AUDIT3.md:63](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:63), lines 96–109).
2. The resulting edit must also “implement[] the named item” ([PREREGISTRATION-AUDIT3.md:111](/Users/jamiehorsburgh/Projects/goalpost/phase8/PREREGISTRATION-AUDIT3.md:111)). DIFFS line 3 and each heading identify that named item as the selected raw artifact, humanised.

Therefore cluster-family compliance alone is insufficient.

Recommended adjudication:

- `EXPERIENCE_GAIN: tableau experience` — FAIL. The edit only extends dates; it adds no Tableau experience to the affected current role. The unchanged prior role already mentions Tableau. [DIFFS.md:5](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:5)

- `experience: quantified achievements` — FAIL. The edit changes dates only. It neither adds nor strengthens quantified achievements; the existing quantified bullets are unchanged. [DIFFS.md:160](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:160)

- `EXPERIENCE_GAIN: senior project lead experience` — FAIL. Extending tenure as an `Assistant Project Manager` does not substantively implement senior-project-lead experience; title and duties remain unchanged. [DIFFS.md:200](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:200)

- `CLOUD_SKILL: statistical skills` — PASS, but taxonomy-questionable. The selected raw artifact is explicitly and exactly added using the skills/tools dose: `statistical skills — working proficiency...` [DIFFS.md:31](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:31). The semantic mismatch between `CLOUD_SKILL` and `statistical skills` belongs to the frozen taxonomy/mapping, not this edit’s implementation.

- `PROGRAMMING_PRACTICE: technical depth` — PASS, but substantively weak. The exact selected artifact is explicitly added using the skills/tools template at [DIFFS.md:252](/Users/jamiehorsburgh/Projects/goalpost/phase8/DIFFS.md:252). “Technical depth” is vague and not a concrete programming practice, but the frozen dose permits an asserted skill rather than requiring evidence; marking this a strict failure would add a concreteness rule absent from the preregistration.

Bottom line: fail the three experience rows because the chosen dose does not express their named artifact; pass the two skills rows because they explicitly substitute the mechanically selected artifact into the prescribed template, while flagging their upstream taxonomy/semantic quality.

Command used:

```sh
nl -ba phase8/PREREGISTRATION-AUDIT3.md | sed -n '61,73p;94,115p'
nl -ba phase8/item-selection.json | sed -n '1,17p;61,100p'
nl -ba phase8/DIFFS.md | sed -n '1,45p;146,184p;186,224p;226,266p'
```
<!-- VERBATIM END: audit_globals FINAL_ANSWER 3 -->
