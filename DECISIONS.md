# DECISIONS.md

Running log of assumptions, resolved ambiguities, and departures from the kickoff prompt. Ground-truth hierarchy: dissertation > kickoff prompt (scope/constraints/process) > logged judgement.

**Append-only from D-012 onward (author instruction, 2026-07-05):** new entries go at the end, lab-notebook rules. Entries D-001–D-011 predate the rule and keep their original (reverse-chronological) placement.

---

## 2026-07-05 — Phase 0

**D-001 · Kickoff summary vs. dissertation architecture (major).**
The kickoff prompt (§3) describes the study as "systems under test were given CVs against job specifications and asked to produce a decision, reasons, and recourse." The dissertation actually has an XGBoost model make the decision on synthetic *tabular* profiles, with an LLM translating frozen SHAP attributions into reasons + recourse. No CV documents, no job specs, no LLM-made decisions. The headline numbers (reason Jaccard 0.89, recourse 0.36, gap persists at T=0.0) are all **confirmed** but describe translation-layer repeat-stability. Per the hierarchy the dissertation wins on methodology; the kickoff remains authoritative on V1 scope, so the tool generalises the instrument to end-to-end LLM screening — recorded as translation gap G2 and to be stated plainly in METHODOLOGY.md. *Flagged at Phase 0 checkpoint.*

**D-002 · Cluster mapping tables unavailable in the PDF.**
§3.2.6 claims 8 feature + 8 action clusters; Appendix C enumerates 5 feature clusters and 0 action clusters. The exact mapping is the fidelity-critical core of the headline numbers and lives only in the dissertation's code repo. **Action requested from author: provide the honours-project Phase 2 code (cluster mappings + full prompt templates).** Interim default per gap G1.

**D-003 · EDI composite arithmetic inconsistency (dissertation-internal).**
Eq. 6 with Table 4 component means yields 0.278 (or 0.044 under a 1−overlap reading of D_rank); Table 4 reports 0.156. Not tool-blocking (EDI is Phase 1 / model-layer, out of V1 scope) but flagged to the author for awareness. See METHODOLOGY_EXTRACTION.md D4, plus internal inconsistencies D5–D9 there.

**D-004 · Git and repo hygiene.**
Repo initialised before any other work; dissertation PDF committed as the founding artifact (kickoff §8). Conventional commits throughout.

**D-005 · Full-text extraction method.**
PyMuPDF (available on system Python 3.9). LaTeX-produced PDF; extraction clean. Tables 4–9 spot-checked against rendered page images — exact matches; equations in Appendix A transcribed manually from render. No OCR needed.

**D-006 · V1 headline metrics (proposed, pending checkpoint).**
Fidelity and Arcade Score do not transfer to the tool's setting (no SHAP ground truth; Arcade demoted by the dissertation itself). Proposed V1 headlines: Recourse Stability Score, Reason Stability Score, Decision Stability, plus direction-flip rate. Gaps G7/G8.

**D-011 · Phase 1 design validated section-by-section (brainstorming process).**
Author decisions: elicitation = **both modes in V1** (structured contract default + freeform with pinned extractor); normaliser = **layered** (keywords → pinned-LLM fallback, logged/cached/promotable); corpus = **LLM-drafted then frozen** with content hashes. 24 author amendments folded in — highlights: asymmetric extractor gate (high stability reportable as lower bound at self-agreement ≥ 0.90; instability claims and the reason–recourse gap need +0.15 margin; agreement per item type); SUT identity split from Condition; elicitation mode in SUT identity; cache key includes repetition_index (repeats never cache hits); budget stops at block boundaries with breadth-balanced interleaving; taxonomy frozen per audit, promotion between audits, mixed-version comparisons hard-error; NOVEL singletons + published NOVEL rates; ranking eligibility floors + tie-bands; data-derived lay headline with committed anchors artifact; runner core added to never-delegate list; Phase 2 builds thin main-thread versions of delegable components. Full detail in DESIGN.md.

**D-010 · Phase 0 sign-off received; defaults accepted; code repo provided.**
Author approved all G1–G12 defaults ("defaults fine") and provided the honours-project code at `~/Projects/Honours_Notebooks/`. Phase 0 checkpoint closed.

**D-009 · G1/G3/G5/G12 resolved from author's code (see METHODOLOGY_EXTRACTION.md §14).**
Real taxonomy is **7 feature clusters + 8 action clusters** (PDF said 8+8; Appendix C listed 5). Full v2 prompt, policy-lens texts, and contradiction keyword lists recovered verbatim. Jaccard: sets are IDs **without** direction, all-pairs mean, empty∧empty=1.0, unmatched IDs pass through as singleton clusters, candidate→condition aggregation is an unweighted mean. Parser is token-anchored balanced-delimiter JSON extraction, not regex. Goalpost's normaliser will inherit this machinery with a fresh committed taxonomy (the honours keyword lists seed it, extended for CV-document content); deviations from the honours taxonomy get logged.
Nuances for METHODOLOGY.md honesty: baseline lens has an empty contradiction-keyword list (its 0% rate is structural); fairness keywords are education-tier proxies + gender/ethnicity (not "age" as the PDF implies); candidate selection was a seeded random sample, not curated to span the SHAP distribution; a `prompt_nudge` condition dimension exists in code but is unmentioned in the PDF.

**D-008 · Cross-extraction reconciliation complete.**
Fresh-context sub-agent independently extracted the fidelity-critical items; zero content conflicts with the primary extraction, same internal inconsistencies found independently. Six additional unspecified items adopted into the extraction doc (§11), one consequential enough to become gap G12 (Jaccard set identity). Cross-extraction committed as evidence at `extraction/CROSS_EXTRACTION.md`.

**D-007 · Proxy echo / policy contradiction deferred to V2.**
The dissertation's contradiction metric keyword-matches protected-attribute terms; the kickoff (§5, §9.5) rules protected-attribute machinery out of V1. V1 keeps only direction-flip contradiction. Gap G9.

---

**D-012 · Pre-registered extractor-threshold protocol; slice runs both modes (2026-07-05, author instruction at Phase 1 sign-off).**
The extractor self-agreement thresholds (reportability at self-agreement ≥ 0.90; +0.15 margin over measured stability for instability claims and the reason–recourse gap) are design constants chosen by judgement, not derived from data. Protocol: they may be revised **at most once**, **only before any reportable audit is run**, **only on the basis of the Phase 2 slice's calibration data**, with the rationale logged here; any subsequent report that relies on the revised thresholds must disclose both the original and revised values. Accordingly, the Phase 2 vertical slice runs **both elicitation modes**: structured to prove the spine end-to-end, freeform to generate the calibration data this protocol depends on.

**D-013 · Environment: Python pinned to 3.12; macOS UF_HIDDEN vs Python 3.14 (2026-07-05).**
Python 3.14's `site.addpackage` skips `.pth` files carrying the macOS `UF_HIDDEN` file flag; something on this machine (most likely iCloud Documents sync) asynchronously flags freshly written files under `~/Documents`, so the editable-install `.pth` was intermittently ignored and `goalpost` became unimportable between runs. Root-caused via `site.py` source + `ls -lO` (both `.pth` files flagged `hidden`). Fix: `.python-version` pinned to 3.12 (no such check) and `pythonpath = ["src"]` added to pytest config so the test suite never depends on editable-install state. Worth knowing for any future 3.14 project under `~/Documents`.

**D-014 · Provider-agnostic endpoints; no single-lab dependency (2026-07-06, author instruction).**
The author rejected any hard dependency on one AI lab or one API key. Resolution: a `ModelEndpoint` abstraction (provider, model, base_url, api_key_env) is now the unit the whole tool speaks. Native `anthropic` and `openai` adapters remain, plus `openai_compatible` against any base_url — which covers OpenRouter (one key, every lab's models: the natural route for multi-vendor comparison audits), Together/Groq/Mistral/DeepSeek/xAI, and local runtimes (Ollama, vLLM, LM Studio) with **no key at all**. `base_url` joins SUT identity (same model name on two endpoints = two SUTs). Per-model `pricing` overrides in config let free/local endpoints cost 0.0 while unknown paid models stay conservatively priced — budget enforcement never underestimates by accident. Back-compat kept for the string `canonicaliser_model`/`extractor_model` config forms. Example configs committed for all three credential situations (`example.yaml`, `examples/openrouter.yaml`, `examples/ollama.yaml`). Slice demo now requires any ONE of: an Anthropic key, an OpenAI key, an OpenRouter (or similar) key, or a locally installed Ollama.

**D-015 · First live run (slice-live-openai, 2026-07-06): environment root cause, one real bug, first calibration data.**
(1) *Environment:* the repo lives under iCloud-synced `~/Documents`; iCloud both flags fresh files UF_HIDDEN (D-013) and evicts rarely-touched files — the first live attempt hung minutes deep in a `read()` syscall while the interpreter imported from an evicted `.venv` file. Fix: venv relocated to `~/.venvs/goalpost` (outside the synced tree) via `UV_PROJECT_ENVIRONMENT` in `goalpost.sh`, which also uses `PYTHONPATH=src` instead of the editable-install `.pth`. **Recommendation to author: move the repo itself to `~/Projects`** — transcripts are audit evidence and should not live where a sync service can evict or mutate flags on them.
(2) *Bug found by the live run:* sha256-derived seeds exceeded signed int64; OpenAI 400s on seeds > 2^63−1. Fixed test-first (mask to 63 bits).
(3) *Run facts:* 30 calls, $0.0095 actual (est. $0.0295), both modes, N=5, T=0.0, gpt-4o-mini SUT / gpt-4.1-mini extractor+canonicaliser. All 10 SUT calls parsed cleanly, zero refusals; normaliser: 79 rule / 31 LLM / 0 NOVEL mappings.
(4) *First calibration data for the D-012 threshold protocol:* extractor self-agreement measured at reasons **0.58**, recourse **0.87** (k=3, gpt-4.1-mini) — both below the pre-registered 0.90 reportability bar. Under the pre-registered gate, this slice's freeform numbers are NOT reportable; options (author decision, revisable at most once per D-012): a stronger extractor model, extractor prompt iteration, and/or threshold revision. No revision made.
(5) *Substantive observation (single case, N=5 — not a claim):* structured mode at T=0.0 showed decision stability 1.00, reason cluster Jaccard 1.00, recourse cluster Jaccard 0.585 — a reason–recourse gap directionally consistent with the dissertation, on a 2026 model, at the cluster level; raw-level recourse was 0.27.
(6) The recorded structured transcripts are committed as a permanent offline replay fixture (`tests/test_live_replay.py`).

**D-016 · Repo relocated; extractor calibration closed without threshold revision (2026-07-06, author instructions).**
(1) Repo moved from iCloud-synced `~/Documents` to `~/Projects/algorithmic-audit-tool`; git history intact; full suite green post-move. Evidence no longer lives where a sync service can evict or flag it.
(2) Calibration rerun (`slice-live-002-gpt41-extractor`, $0.0321): with **gpt-4.1-2025-04-14** as extractor, self-agreement = reasons **1.00**, recourse **0.956** — both clear the pre-registered 0.90 gate. Per D-012 the thresholds stand unrevised; the one permitted revision remains unused. gpt-4.1 (or stronger) is the recommended pinned extractor default; gpt-4.1-mini is documented as insufficient (0.58/0.87).
(3) Replication note (single case, N=5): structured-mode gap reproduced — decision 1.00 / reason cluster 1.00 / recourse cluster 0.538 (first run 0.585). Freeform recourse read 1.0 through the new extractor with small extracted sets (mean size ~1.4 previously) — a reminder that coverage companions must be read beside every stability number.

**D-017 · SUT endpoint policy: first-party direct keys preferred over aggregators (2026-07-26).**
Prompted by OpenRouter payment failure but adopted on merit: aggregators route requests across backend hosts (potentially differing quantisations/deployments run-to-run), which for a *repeat-stability* instrument is a measurement confound — router variance could masquerade as model instability. Policy: SUTs use first-party endpoints (pinned snapshots + provider fingerprints) wherever available; aggregator endpoints are acceptable for long-tail model coverage only, with routing explicitly disclosed in the report. This revises the emphasis of the D-014-era OpenRouter recommendation; the endpoint layer itself is unchanged. Current key set: OpenAI (funded), Google AI Studio + Groq (free tiers, pending), Anthropic (pending small credit).

**D-018 · Cross-lab hardening from live failures (2026-07-26).**
The Gemini/Claude runs exposed and fixed, test-first: (1) `send_seed`
endpoint option — Google's OpenAI-compat shim 400s on `seed`; (2)
block-level error containment in the runner — provider failures (e.g.
RESOURCE_EXHAUSTED) now yield missing-blocks + recorded errors instead of
crashing the audit; (3) canonicaliser mappings persist via the on-disk
cache across resumes (design §3 promise now actually held; the Claude
resume had re-paid ~$0.1 of mappings). Claude (Haiku 4.5) measured: gap
+0.291, decision 0.984, with 11/125 parse failures — first material
contract non-compliance observed; queued: contract-tuning pass and a
cross-audit comparison renderer. Gemini blocked on account billing state
(prepay, zero credits), not tool capability.

**D-021 · Real-target audit complete (realtarget-hs-screener-002-gptoss, 2026-07-27).**
Target: published open-source 4-agent screening pipeline (pinned SHA 49dc41a, prompts runtime-fetched + hash-verified, never committed — unlicensed upstream). Served model: gpt-oss-120b on Cerebras free tier — a disclosed double substitution (upstream pins llama3-70b-8192, retired industry-wide; Groq's llama-3.3 ran 4/25 cases before its 100k/day cap; Cerebras serves no Llama on this account). The audit therefore measures the pipeline's *prompt and chain design* on a current open-weights model, not the unrunnable original deployment. Quota walls crossed via block containment + resume (3 passes; hourly request quota). OpenAI-side spend across passes ≈ $0.51; SUT spend $0 (free tier; author's $5 Cerebras credit to be reconciled against dashboard).
Findings: (1) **decision instability on a real pipeline** — 3/25 cases changed hiring verdict across 5 identical runs at the pipeline's own default temperature (worst case 0.6 agreement); decision-level extractor self-agreement 1.000, so this claim passes the gate on any reading. (2) Reason/recourse extraction reliability on this pipeline's sprawling prose sits at the gate boundary (see D-022). (3) The upstream's dead model pin is itself a finding: the published tool's exact deployed form is no longer runnable anywhere.

**D-022 · Gate-level question is now live and decisive (author decision pending).**
Final full-corpus self-agreement (10-case stratified sample, k=3): decision 1.000; reasons raw 0.740 / cluster 0.881; recourse raw 0.887 / cluster 0.920. Measured (unreported) aggregates: reason cluster 0.805, recourse cluster 0.456 IQR [0.32, 0.57]. Under the pre-registered raw-basis gate: reasons AND recourse withheld. Under a cluster-basis gate: recourse 0.456 becomes reportable (0.920 ≥ 0.90; margin 0.46 ≥ 0.15); reasons stays withheld (0.881 < 0.90) — so the reason–recourse *gap* claim is unreportable for this target either way. Sampling honesty: self-agreement estimates ranged 0.66–0.95 across passes as the sample composition shifted with completing blocks — n=10, k=3 estimates carry real noise, which any gate-basis decision must acknowledge. Reporter continues to gate on the pre-registered raw basis until the author rules.

**D-023 · Gate basis: cluster level, decided on a widened sample (2026-07-27, author decision).**
Author ruled: gate at the level the claim is made (cluster), after re-measuring self-agreement on a larger sample. Sample widened 10→25 cases (k=3; 75 fresh measurements): decision 1.000; reasons raw 0.787 / cluster 0.904; recourse raw 0.785 / cluster 0.902. Thresholds remain 0.90/+0.15, untouched (D-012's one revision still unused). Under the cluster basis: **recourse stability 0.456 is reportable** (0.902 ≥ 0.90; instability margin 0.446 ≥ 0.15); **reason stability 0.805 stays withheld** (margin 0.099 < 0.15), so the reason–recourse gap claim remains unreportable for this target. Both bases are disclosed in every report (raw beside cluster, 3 decimals so boundary proximity is visible: 0.902 clears a 0.90 bar by 0.002 — stated, not hidden). Old flat-only metrics files gate on the raw basis unchanged.
Known accounting gap found in passing: self-agreement extractor calls are not added to the audit's total_cost_usd (the resume printed $0.00 while ~$0.4 of measurement ran); fix queued.

**D-024 · Public write-up drafted; target-identity and disclosure policy (2026-07-27, author editorial direction).**
WRITEUP.md v1 drafted from the template. Editorial rules adopted: (1) lead with the full-confidence lay finding (verdict flips on identical inputs), recourse 0.456 second as a lower bound with the 0.902-vs-0.90 boundary shown at 3 decimals, the withheld reason/gap claim told precisely — the gate ruled on extractor reliability (0.904, margin short by 0.051), not on the finding's reality, so extractor improvement + re-run is legitimate and pre-registered-consistent; (2) n=25 supports existence claims only — "verdict instability was observed", no rate claims; (3) claims scoped to "the pipeline's prompt-and-chain design as served by a current open model" (double substitution disclosed; upstream's pinned model retired industry-wide — itself a named governance finding); (4) the target is described as a design category, not named, in the prose — it is a small individual open-source project, the point is the category; full identification stays pinned in the audit evidence; professional norm adopted: courteous disclosure to the audited party before publication; (5) the ~$0.51 cost stated. Queued next: hardened reason-extractor + re-run to resolve the withheld claim either way; disclosure note to upstream author before any publication.
