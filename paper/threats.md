# Threats — the hardest reviewer questions

*Five questions a reviewer versed in these literatures would ask of WRITEUP.md
v4, each with the evidence this repo holds against it — or the honest absence.
Compiled 2026-08-06.*

---

## T1 — "This isn't recourse. Recourse has validity conditions; you measured word overlap."

A recourse-literature reviewer (Karimi, Ustun lineage) will say: recourse is
defined by a guarantee — follow the advice and the decision flips. Goalpost
never tests whether any recommendation, if followed, would change the verdict;
it measures Jaccard overlap of extracted advice slugs across repeats.

**Evidence in repo:** `metrics.py` confirms the charge is factually right:
recourse stability is set-overlap of `action_id` slugs, no validity check
anywhere in the pipeline. **Honest absence:** nothing in the repo measures
recourse validity, and nothing claims to — but the write-up borrows the word
"recourse" with its literature weight attached. Mitigation available: the
consistency-is-necessary-for-validity argument (advice that differs on every
query cannot carry a guarantee, whatever its content), plus one explicit
sentence renaming the construct precisely. The counter is *a priori*, not
measured — say so.

## T2 — "The reason–recourse gap is a granularity artifact."

Reasons are counted at four fixed rubric headings; advice at individual
recommendations. Coarse buckets match more easily. An XAI reviewer will say an
unknown share of 0.534 is measurement resolution, not behaviour.

**Evidence in repo:** The control gives the differential argument (target
0.537 vs bare-model 0.106 under the same reader and headline grain — the
match narrows resolution confounds, though it cannot guarantee the two
architectures' prose interacts identically with extraction; the ~0.43
difference is design-associated evidence). The corrected direction metric is
reported at raw, normalised and cluster levels and is explicitly not treated
as granularity-robust: its matched common-case contrast is +0.120 raw but only
+0.010 cluster. **Residual weakness:** the
two sides are still measured at different resolutions, and no repo experiment
quantifies how much of the *absolute* gap granularity accounts for (e.g.
re-scoring reasons at sub-heading granularity). The write-up says "cannot
explain the distance"; a reviewer may ask for the number.

## T3 — "Your extractor is an LLM judge, and that literature says judges are noisy. Your gate rests on n=25, k=3."

An LLM-as-judge reviewer (Shi et al. lineage) will note: judge reliability
estimates carry sampling noise, and D-022 itself records self-agreement
estimates swinging 0.66–0.95 as sample composition shifted. The certified
0.932 clears 0.90 — measured how confidently?

**Evidence in repo:** The strongest process story in the piece: thresholds
pre-registered before any audit (D-012), never revised; gate basis ruled at
the claim's level on a widened 25-case sample (D-023); the gate refused three
times, including refusing the author's target finding (D-024) and exposing the
lens's own selection effect on control data (D-028); both bases disclosed at 3
decimals in every report. **Residual weakness:** no confidence intervals on
self-agreement estimates; the cluster-basis ruling (D-023) was made after
seeing that the raw basis would withhold the finding — pre-registered-adjacent,
not pre-registered. The record is honest about this; the write-up should be too
if pressed.

## T4 — "You measured a free-tier serving host, not a design. Aggregator/quantisation variance could be your 'instability'."

D-017 itself concedes the point in principle: routing and serving variance can
masquerade as model instability. The certified audit ran gpt-oss-120b on
Cerebras (free tier, then paid), not a first-party pinned snapshot with
fingerprints.

**Evidence in repo:** D-017 policy (first-party preferred, routing disclosed);
crucially, the bare-model control (D-028) ran the *same model on the same
host* — so serving noise is a shared exposure for the design-associated
gap claim: narrowed as a confound, though
independent stochastic runs do not cancel it by construction. **Honest absence:**
the *absolute* stability numbers (0.448, 0.968) are host-inclusive — the repo
cannot separate model-inherent from serving-infrastructure noise, and no
cross-host replication of the target exists. Atil et al.'s finding that
non-determinism persists across deployments helps, but doesn't quantify this
host.

## T5 — "n=25, one pipeline, a double model substitution — what population does any claim generalise to?"

The audited artifact isn't the deployed original (its pinned model is retired
industry-wide); the serving model was substituted; 25 fictional CVs; one
target.

**Evidence in repo:** The write-up's scope discipline is its defence, and it's
documented as deliberate: existence claims only, no rate claims (D-024);
claims scoped to "the pipeline's prompt-and-chain design as served by a current
open model," substitution disclosed as itself a governance finding; D-032's
line-by-line scope audit removed four overclaims. The wider pattern (seven of
eight configurations and five of six base-model families show at least one
scored verdict flip) is presented as hedged inference, not universal claim.
**Residual weakness:** the design-class
claim ("chained rubric designs manufacture explanation stability without
guidance stability") rests on one pipeline and one control — a reviewer can
fairly ask for a second chained target before "design category" language fully
earns itself. The write-up's "Next: more targets" concedes this; expect the
question anyway.
