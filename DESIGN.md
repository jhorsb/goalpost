# DESIGN.md — Goalpost V1

**Status:** validated section-by-section with the author (2026-07-05); Phase 1 checkpoint artifact.
**Lineage:** generalises the dissertation's Drift Arcade metric machinery (see `METHODOLOGY_EXTRACTION.md`, esp. §14) to end-to-end LLM screening audits. Where this design departs from the honours implementation, the departure is stated.

---

## 1. Architecture

A five-stage pipeline with a frozen boundary between every stage. Each stage consumes only the previous stage's on-disk artifact, writes its own, and stamps its version into it. Chain of custody, not a monolith.

```
corpus (frozen, hashed)
   → perturbation engine → variants/ (frozen derived artifact,
   |                        deterministic from corpus + seed + config)
   → runner       → transcripts/  (JSONL evidence: every scored run's
                                   inputs and outputs; internal stage
                                   calls and retries are not itemised)
   → parser       → runs/         (StructuredRun records)
   → normaliser   → normalised/<version>/ (canonical sets + mapping log)
   → metrics      → metrics/<version>/    (per-case + aggregate JSON)
   → reporter     → report/       (lay page, technical appendix, comparison)
```

Design consequences:

- **Transcripts are the evidence locker.** Raw request/response, usage, cost, seeds, timestamps. Everything downstream is a pure function of files on disk: re-parse, re-normalise, re-score, re-render — offline and free. Improved normaliser next year ⇒ re-score old transcripts; the report states which normaliser version produced which number.
- **Two elicitation modes** enter at the runner and converge at the parser's output schema:
  - `structured` — operator's screening prompt + Goalpost's output contract (v2-style structured tail). Deterministic parsing; no second LLM in the measurement path.
  - `freeform` — operator's prompt untouched; a pinned, different-model **extractor** converts prose to the same StructuredRun schema. Every downstream record carries `extracted: true` + extractor config hash, and every freeform number is accompanied by an empirical **extractor self-agreement score** (§4.4) — a flag alone is not enough.
- **Elicitation mode is part of SUT identity** (§2). No cross-mode comparison renders without an explicit banner.
- **Provenance tuple on every reported number:** (corpus hash, variant config+seed, sut_id incl. mode, condition, runner/parser/normaliser/taxonomy/metrics/report versions).

### Approaches considered (elicitation — the deepest fork)
1. **Output contract only** — dissertation-faithful, deterministic, but can't audit prompts the operator can't modify.
2. **Pinned extractor only** — audits deployed reality, but rests the whole metric on a second model.
3. **Both modes (chosen, author decision)** — structured as default, freeform behind a mode flag with the self-agreement gate (§4.4) making its numbers honest. Cost: two parser paths and a validation burden, accepted for coverage.

## 2. Data model

All pydantic, fully typed. Explicit lineage keys everywhere — **no positional joins**.

| Model | Key fields |
|---|---|
| `Case` | `case_id`, cv_text, job_spec_text, `content_hash` |
| `Variant` | `case_id`, `perturbation_class`, seed, derived text, `content_hash`. First-class sibling of Case: metrics group identical-input vs perturbed-input without special-casing |
| `SUTConfig` | provider, model (pinned snapshot, §7), params, prompt template (hashed), **elicitation_mode**. `sut_id` = short hash over all five |
| `Condition` | temperature, N repeats, seed policy. **Separate from SUT identity** — a field on records and a first-class metrics grouping axis (the T=0 finding is a within-SUT claim) |
| `TranscriptRecord` | `transcript_id`, `sut_id`, condition, **case/variant content hash, `repetition_index`**, request, response, usage, cost, derived per-repetition provider seed, provider-returned model/fingerprint, timestamps, `runner_version` |
| `StructuredRun` | `run_id`, **`transcript_id`**, decision, `reasons[] = {reason_id, direction, note}`, `recourse[] = {action_id, description}` (honours two-field schema — the model coins a short slug; the normaliser operates on the slug, falls back to description), parse status, refusal flag, `extracted: bool` + extractor config hash, `parser_version` |
| `NormalisedRun` | **`run_id`**, three-level sets (raw/normalised/clustered) per item type, `taxonomy_version`, `normaliser_version` |
| `MappingRecord` | item raw → normalised → cluster, `source: rule\|llm\|passthrough`, rule or prompt hash, **all cluster hits on multi-hit items** (first wins for scoring; rest surfaced in taxonomy review) |
| `ProvenanceTuple` | attached to every aggregate number (§1) |

On-disk layout (nothing mutated in place; `normalised/` and `metrics/` are version-keyed):

```
audits/<audit-id>/
  config.yaml                    # resolved, defaults expanded
  corpus/  variants/
  transcripts/<sut-id>/          # includes extractor + canonicaliser calls:
                                 #   full TranscriptRecords, through the cache
  runs/<sut-id>/
  normalised/<normaliser-version>/<sut-id>/   (+ mapping_log.jsonl)
  metrics/<metrics-version>/
  report/
```

Failures are data: refusals, parse failures, and validation failures flow into metrics with explicit denominators (§4) — never silently dropped.

## 3. Normaliser (scientific core — main thread)

Three deterministic-first sub-stages; every item logged.

1. **Text normalisation** — honours rules verbatim: lowercase, non-alphanumeric → `_`, collapse repeats, dedupe.
2. **Keyword taxonomy** — committed YAML, separate `reason_taxonomy` / `recourse_taxonomy`, versioned (semver + content hash, **hash validated against `taxonomy_version` at config time**). Seeded from the honours tables (7 feature / 8 action clusters, `METHODOLOGY_EXTRACTION.md` §14.1), extended for CV-document content. Honours matching semantics kept: split on `_`, first cluster with a token hit, list order significant.
3. **Pinned LLM canonicaliser** — only for items no rule matched. Different provider/model from every SUT in the audit (config-validation hard error otherwise). Committed prompt; classifies into an existing cluster or `NOVEL:<slug>`. T=0, content-addressed cache on (item text, taxonomy version, canonicaliser config): first mapping wins, is logged, and reruns are deterministic by construction. Canonicaliser calls are full TranscriptRecords through the cache.

Rules with teeth:

- **Taxonomy frozen per audit.** Promotion of accepted LLM mappings into the keyword tables happens *between* audits only, bumping `taxonomy_version`. Comparisons across mixed taxonomy versions hard-error; the remedy is re-normalising all SUTs under the newest version (free, from transcripts).
- **NOVEL items score as normalised-text singletons.** NOVEL rate published per SUT per item type; material NOVEL-rate differences flagged in comparison reports; sustained NOVEL accumulation triggers a "taxonomy may be missing a cluster" warning.
- **`goalpost taxonomy review`** renders all LLM mappings + a stratified rule-mapped sample (including multi-hit items) for human spot-check and promotion.

### Approaches considered
1. **Keywords only** — fully auditable, zero LLM, but coverage gaps on open text systematically deflate Jaccard: the tool would fabricate instability. Rejected as scientifically unsafe alone.
2. **LLM canonicaliser only** — best coverage, but the whole metric rests on a second model. Rejected.
3. **Layered (chosen)** — deterministic spine, LLM touches only leftovers, mappings logged/cached/promotable; the taxonomy hardens over time and the LLM's share shrinks.

## 4. Metrics module (scientific core — main thread; pure functions, zero I/O)

Per (SUT, condition, case), over N repeats:

- **Decision Stability** — modal-decision agreement rate. Refusal and parse-failure rates always beside it, with the full denominator chain (attempted / parsed / scored).
- **Reason & Recourse Stability** — mean pairwise Jaccard over all C(N,2) **same-decision pairs** (primary; all-pairs as labelled secondary; discarded-pair fraction reported). Computed at all three ladder levels; **headline = clustered** (the honours headline level, confirmed in Phase 0); the full ladder ships in every report with **per-item-type normaliser lift**, so taxonomy asymmetry cannot silently manufacture the reason–recourse gap. Honours conventions kept: sets of IDs without direction, empty∧empty = 1.0, singleton pass-through.
- **Opposite-direction rate** — Goalpost v0.2 definition, at raw,
  normalised and cluster levels: same-decision scored-run pairs only; a
  shared topic is scorable only when both runs give it one unambiguous binary
  direction (`positive` or `negative`); opposite signs / unambiguous shared-topic comparisons, with
  numerator, denominator, ambiguous exclusions and contributing-run-pair
  count explicit. A case needs ≥3 contributing run-pairs to aggregate.
  Goalpost v0.1's distinct-topic reversal incidence remains labelled legacy;
  the dissertation record did not specify its denominator.
- **Perturbation robustness** — same metrics grouped over variants; **never pooled** with identical-input repeat-stability. Decision-flip-under-immaterial-edit rate is a first-class output.
- **Coverage companions** — emptiness rate and mean set size beside *every* stability number; headlines driven by empty∧empty pairs are flagged. Coverage is undefined, not zero, when there are no scored runs; pair fractions are undefined when there are no run-pairs.
- **Effective n_pairs** — reported per case; cases below a minimum are excluded from aggregates and listed with reasons.
- **Aggregation** — case → condition unweighted mean, with median/IQR and per-case distributions.

### 4.4 Extractor self-agreement (freeform mode)
Computed **per item type** (reasons vs recourse — differential extraction difficulty must not fabricate the gap), on a stratified sample of responses, k=3 uncached extractions each (cache bypass via nonce); agreement = mean Jaccard of extracted sets.

**Gate (asymmetric by design):** extractor noise *preferentially* attenuates observed stability, though it can also inflate overlap (D-065) — the asymmetry is a conservative choice, not an identity. Therefore:
- **High-stability claims** are reportable whenever self-agreement ≥ 0.90 (certified estimates under the committed reader; the earlier "lower bound" framing is retracted — see D-065).
- **Instability claims and the reason–recourse gap** additionally require self-agreement to exceed the measured stability by ≥ 0.15; otherwise the report prints the agreement score and withholds the claim.

## 5. Reports (Jinja2 → Markdown + HTML; JSON alongside)

**Page one — lay report** (union rep / journalist): what was tested in plain words; the headline as a **data-derived statistic** ("ask this system twice and, when the decision comes back the same, on average only 1 in 3 of its recommendations appears both times"), not an adjective — verbal anchor bands come from a **committed, versioned anchors artifact** stamped into every report; the sat-nav paragraph; one sentence each for reason-vs-recourse, decision stability, and **decision flips under immaterial edits** (above the fold); a "what this doesn't tell you" box (repeat-stability ≠ accuracy ≠ fairness; freeform numbers are extractor-mediated certified estimates, agreement score shown); a **minimal provenance stamp** (audit id, date, tool + anchors versions) so cropped screenshots stay traceable.

**Technical appendix:** full three-level ladder with per-item-type lift; taxonomy granularity (cluster count + members); coverage companions; denominator chain and exclusions; NOVEL rates; extractor self-agreement per item type; per-class perturbation breakdowns; per-case distribution strips; provenance tuple; resolved config.

**Comparison report (2+ SUTs):** one row per SUT × condition. **Eligibility floors:** SUTs enter the ranked table only if they clear coverage / denominator / NOVEL thresholds; the rest are listed unranked with reasons. Overlapping-IQR rows render as **tie-bands**, not strict order. Mixed taxonomy versions hard-error; cross-mode rows bannered; material NOVEL-rate differences flagged inline. Tone throughout: measured, non-adversarial — measurements with conditions, never verdicts about vendors.

## 6. Config & CLI

One YAML (`example.yaml` works out of the box against the starter corpus):

```yaml
audit_id: example-audit
corpus: corpora/starter-v1/
output_dir: audits/
budget: {max_spend_usd: 5.00}
perturbations: {enabled: false, classes: []}
taxonomy: {path: taxonomies/cv-screening-v1.yaml, version: "1.0.0+<hash>"}
canonicaliser: {provider: anthropic, model: <pinned>, ...}   # ≠ any SUT model
extractor:     {provider: anthropic, model: <pinned>, ...}   # ≠ any SUT model
conditions: [{temperature: 0.0, repeats: 5}, {temperature: 0.7, repeats: 5}]
suts:
  - name: example-screener
    provider: openai
    model: <pinned snapshot>
    elicitation_mode: structured
    prompt_template: prompts/example_screener.txt
```

CLI (typer): `goalpost audit --config X [--dry-run] [--resume <id>] [--max-spend N]`, `goalpost report <id>`, `goalpost taxonomy review <id>`, `goalpost corpus generate` (Phase 3). Secrets via env only; config validation runs before any network call.

## 7. Runner, cost model, and integrity guarantees (runner core — main thread)

- **Cache key includes case/variant content hash + `repetition_index`.** Repeats are never cache hits — a cache-collapsed repeat would fabricate perfect stability. Named regression test.
- **Per-repetition provider seeds** derived deterministically (audit seed, sut, condition, case, repetition_index) and recorded; never relied on for the stability claim.
- **Pinned model snapshots required** where the provider offers them; floating aliases produce a hard warning. Provider-returned model/fingerprint recorded per transcript; **intra-audit fingerprint drift flagged** in the report.
- **Budget enforcement at block boundaries** — block = all N repeats of one SUT × condition × case. No partial blocks (they corrupt pair denominators). Named regression test for block-boundary semantics.
- **Breadth-balanced interleaving** across SUTs, so a mid-audit budget stop leaves comparable coverage per SUT. Incomplete audits render with a banner + explicit missing-block list; `--resume` fills missing blocks only.
- `--dry-run` prints the full call plan (calls, est. tokens, est. cost per SUT and total) and exits. Costs per call recorded in transcripts; running total auditable.
- Bounded concurrency, retry/backoff (honours discipline: it used concurrency 2, 30 s timeout, 2 retries).

### Cost model (order of magnitude)
Starter corpus ~25 cases × 2 conditions × 5 repeats = 250 calls per SUT per mode; at small-model rates (~$0.01–0.05/call with CV-sized prompts) ≈ **$2.50–12.50 per SUT**, plus extractor (freeform only, ~1 call per SUT call) and canonicaliser (leftovers only, cents). Conservative defaults: 1 SUT, structured mode, `max_spend` $5. Phase 2 slice: 1 case × 1 SUT × N=5 ≈ **under $0.50 live**.

## 8. Testing strategy

Strict TDD; the Iron Law holds across every delegation boundary (RED written and committed by me before any brief goes out).

- **Metrics:** golden-file tests (honours-derived cases: empty∧empty, singleton pass-through, same-decision filtering, known Jaccard values) + property tests (bounds, symmetry, permutation invariance).
- **Named integrity regressions:** seed-per-repetition; cache-never-hits-repeats; block-boundary budget semantics; mixed-taxonomy hard error; canonicaliser≠SUT validation.
- **Provider adapters:** recorded fixtures only; full suite passes offline in a fresh clone. One opt-in live smoke test (`GOALPOST_LIVE_TESTS=1`), never default.
- **Phase 2 slice as permanent fixture:** its recorded transcripts are committed and replayed end-to-end in tests forever; Phase 3 Codex RED tests are partly derived from them.

## 9. Delegation plan

**Never delegated (main thread):** metrics module; normaliser (rules, taxonomy content, canonicaliser prompt); both elicitation designs (output contract, extractor prompt); extractor validation analysis; **runner core** (block scheduling, seed derivation, interleaving, budget stops, resume — glassware is delegable, protocol isn't) including extractor/canonicaliser invocation plumbing; corpus content decisions; every judgement-bearing document.

**Codex lanes** (briefs in `delegation/codex/task-NN-*.md`; branch `codex/task-NN-*`; lifecycle + quality notes in `DELEGATION.md` — the vendor-comparison notes are a deliverable): report templating + HTML/CSS; CLI ergonomics + `--dry-run` presentation; content-addressed cache layer (repetition-index rule shipped as RED test); retry/backoff; fixtures tooling; packaging (uv, entry points); corpus generator implementation once schemas/invariants are specced. Brief format per kickoff §4b: context paragraph, exact contracts, committed RED tests, file-touch allowlist, no-new-deps, definition of done, return format. Incoming diffs reviewed line-by-line as untrusted; full suite before merge.

**Sub-agents:** provider-docs lookups at build time; fresh-context review agent over each phase's full diff before checkpoint; Phase 3 parallel workstreams only where state is disjoint — never two agents in one module.

**Phase mapping:** Phase 2 = thin main-thread versions of everything, including the delegable components (the slice is the spine). Phase 3 = orchestration: I build normaliser/metrics/runner-core hardening; Codex briefs harden the glassware against RED tests partly derived from the slice's recorded transcripts.

## 10. Stack

Python 3.11+, pydantic v2 throughout, typer CLI, uv for env/deps, Jinja2 for reports, pytest. Provider adapters: thin uniform interface over Anthropic / OpenAI / OpenAI-compatible endpoints; model strings only in config; **current provider API shapes verified via docs lookup at build time, not assumed**.

---

## 11. Amendment changelog (design-dialogue record)

The design was presented in seven sections and validated one at a time (2026-07-05). Every author amendment, attributed to the section it modified — raw material for the write-up's methodology section. All are integrated in the body above; this is the record of what the dialogue changed.

**Section 1 — Architecture (4):**
1. Freeform extractor must carry an *empirical self-agreement score* reported alongside anything it touched, not a bare `extracted` flag; unreportable freeform numbers withheld (gate later refined by S3-1).
2. Perturbation engine appears explicitly in the pipeline; variants materialised as a frozen derived artifact, deterministic from corpus + seed + config.
3. Elicitation mode is part of SUT identity — first-class field everywhere; no cross-mode comparison without explicit flagging.
4. Version-stamping generalised: every stage writes its version into its artifact; full provenance tuple on every reported number.

**Section 2 — Data model (5 + 1 question resolved):**
1. Explicit lineage keys on every record (transcript: case/variant hash + repetition_index + condition; run: transcript_id; normalised: run_id); no positional joins.
2. SUT identity (provider, model, prompt hash, mode) split from Condition (temperature, seeds, N); condition is a field and a metrics grouping axis — the T=0 finding is a within-SUT claim.
3. Extractor calls get full TranscriptRecord treatment and go through the cache.
4. Failures flow into metrics with explicit denominators; refusal/parse-failure rates reported.
5. Version-keyed output directories extended to `normalised/`.
6. *Author query resolved:* bare-text recourse was the assistant's simplification; the honours two-field schema (`{action_id, description}`, reasons `{reason_id, direction, note}`) adopted.

**Section 3 — Metrics (3):**
1. Extractor gate inverted (asymmetric): extractor noise *preferentially* manufactures instability (it can also inflate overlap — the asymmetry is a conservative choice, not an identity; D-065), so each measured stability `s` is reportable when reader self-agreement `a ≥ 0.90` and either `s ≥ 0.85` or `a − s ≥ 0.15`; reasons and recourse are tested separately and a gap requires both components to pass, not a third margin on the arithmetic difference. Self-agreement is computed per item type (reasons vs recourse), stratified sample, k=3 uncached — differential extraction difficulty must not fabricate the gap.
2. Coverage companions (emptiness rate, mean set size) printed beside every stability number; headlines driven by empty∧empty pairs flagged.
3. Per-case effective n_pairs reported; minimum enforced for inclusion in aggregates; exclusions listed.

**Section 4 — Normaliser (3 + 2 notes):**
1. Reason–recourse gap reported at all three ladder levels with per-item-type normaliser lift published — taxonomy asymmetry must not manufacture the finding. (Phase 0 confirmation: honours headline was cluster-level.)
2. Taxonomy frozen per audit; promotion between audits only; mixed-taxonomy comparisons hard-error — remedy is re-normalising all SUTs under the newest version.
3. NOVEL items score as normalised-text singletons; NOVEL rate published per SUT per item type; material NOVEL-rate differences flagged in comparisons.
4. *Note:* canonicaliser calls become TranscriptRecords through the cache.
5. *Note:* all cluster hits on multi-hit items logged and surfaced in taxonomy review.

**Section 5 — Reports (3 + 1 note):**
1. Ranking eligibility floors — SUTs enter the ranked table only if they clear coverage/denominator/NOVEL thresholds; others listed unranked with reasons; overlapping-IQR rows render as tie-bands, not strict order.
2. Verbal anchor bands become a committed, versioned artifact stamped into every report; the lay headline uses a data-derived statistic ("ask twice; when the decision comes back the same, on average only 1 in 3 recommendations appears both times"), not an adjective.
3. Perturbation results added to all renderings — per-class breakdowns in the appendix, an above-the-fold lay line for decision flips under immaterial edits, and a lay sentence for plain decision stability.
4. *Note:* page one carries a minimal provenance stamp (audit id, date, tool + anchors versions) so cropped screenshots stay traceable.

**Section 6 — Config/CLI/cost/testing (3 + 1 note):**
1. Cache key includes case/variant hash + repetition_index — repeats must never be cache hits; provider seeds derived per repetition and recorded; extractor self-agreement cache bypass via nonce.
2. Pinned model snapshots required where available; floating aliases hard-warned; provider-returned model/fingerprint recorded per transcript; intra-audit fingerprint drift flagged.
3. Budget enforcement at block boundaries only (block = all N repeats of one SUT × condition × case); breadth-balanced interleaving across SUTs; incomplete audits banner with explicit missing-block list.
4. *Note:* taxonomy content hash validated against `taxonomy_version` at config time.

**Section 7 — Delegation (2):**
1. Runner core (block scheduling, seed derivation, interleaving, budget stops, resume) joins the never-delegate list — "glassware is delegable, protocol isn't" — with named regression tests for seed-per-repetition and block-boundary semantics; extractor/canonicaliser invocation plumbing explicitly main-thread.
2. Phase 2 builds thin main-thread versions of the delegable components; Phase 3 Codex briefs harden them against RED tests partly derived from the slice's recorded transcripts.

**Post-sign-off (D-012):** extractor thresholds (0.90 / +0.15) pre-registered — revisable at most once, only before any reportable audit, only on slice calibration data, rationale logged, both values disclosed thereafter. The slice runs both elicitation modes to generate that calibration data.
