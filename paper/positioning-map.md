# Positioning map — where Goalpost sits

**DRAFT — mapping only. The final related-work paragraph is the author's.**
*Compiled 2026-08-06 from the verified reading list (`reading-list.md`). Numbers
in brackets refer to its ranking.*

---

## What each literature establishes

**Algorithmic recourse & its robustness** [3, 5, 6, 7, 4]
Recourse is a formal, guarantee-bearing object: an action set that flips a fixed
model's decision (Ustun [5]), surveyed and unified by Karimi et al. [3]. The
robustness branch showed those guarantees die on contact with deployment: model
updates and distribution shifts invalidate prescribed recourse (Rawal [7]), the
first robust generator and invalidation-probability bounds followed (ROAR [6]),
and the survey of the branch [4] taxonomises robustness by *cause of change* —
model shift, input perturbation, noisy human execution. **In every formulation,
instability requires a perturbation. The unperturbed case is trivially stable by
construction — because the decision-maker is deterministic.**

**Explanation stability** [10, and cut item Slack]
Robustness — similar inputs, similar explanations — is a named desideratum that
LIME/SHAP-era methods fail (Alvarez-Melis & Jaakkola [10]); explanations can
even be adversarially decoupled from behaviour (Slack et al.). This literature
measures attribution vectors over *neighbouring* inputs; free-text explanations
at *identical* inputs are outside its instruments.

**LLM output consistency** [8, 11]
LLMs are non-deterministic even at "deterministic" settings, pervasively and for
systems-level reasons unlikely to go away (Atil [8]); the LLM-as-judge
literature has begun naming *repetition stability* as a reliability construct
for evaluators (Shi [11]). This field measures *answer agreement* — it has not
connected re-query variance to recourse, contestability, or the affected
individual.

**LLM screening audits** [9]
External audits of LLM resume screeners exist and are publishing now (Castleman
[9]) — measuring validity and demographic bias against constructed ground
truth. Consistency appears as an aside (flip rates), never as the audited
property, and reasons/recourse are not measured at all.

**Audit methodology** [12, and cut item Raji]
Structured audit frameworks exist at governance/model/application layers
(Mökander [12]) and as internal end-to-end process (Raji). The application
layer — behavioural audits of deployed LLM systems with pre-registered
protocols and evidence chains — is described far more than it is instrumented.

## Where the gap sits

Each field holds two of the three needed pieces:

| Field | Has | Lacks |
|---|---|---|
| Recourse robustness | recourse formalism + perturbation analysis | a stochastic decision-maker; the identical-input case |
| Explanation stability | instability-of-explanations result | free-text/LLM setting; recourse; identical inputs |
| LLM consistency | identical-input instability at T=0 | decision/reason/recourse decomposition; the affected-person framing |
| LLM screening audits | domain + audit framing | stability as the audited property |
| Audit methodology | protocol norms (pre-registration, evidence) | a working instrument for this property |

The unoccupied square: **re-query (behavioural) stability of decision-attached,
LLM-authored reasons and recourse, measured as an audit with a gated
measurement layer.** The two nearest 2026 neighbours confirm the square is
live but unclaimed: Lee [1] measures repeated-generation consistency of LLM
advice (no decision, no decomposition, no audit protocol); Dong [2] does
recourse *against* an LLM predictor (recourse computed, not uttered).

## Candidate framing sentences (DRAFT — pick, cut, or rewrite)

1. "The recourse-robustness literature asks whether advice survives a change in
   the model; we ask whether it survives *nothing at all* — the same system,
   the same input, asked again."
2. "Goalpost extends recourse robustness into the LLM era, where the
   perturbation that invalidates recourse is no longer an external shift but
   the decision pipeline's own sampling noise: invalidation-by-generation
   rather than invalidation-by-update."
3. "Where explanation-robustness asks that similar inputs yield similar
   explanations, an LLM-mediated screener fails the degenerate case: identical
   inputs yield explanations that keep their topics and flip their meaning."
4. "We connect three literatures that have not met: recourse robustness
   (which assumes deterministic decision-makers), LLM non-determinism (which
   never reaches the affected individual), and algorithmic auditing (which
   supplies the protocol) — into a single measured property: whether the
   goalposts hold still."

## Flagged formalism conflicts (flag only — do not resolve in the write-up)

- **"Recourse"**: Karimi/Ustun recourse is validity-bearing (following it flips
  the decision). Goalpost's recourse-stability measures overlap of *extracted
  advice utterances* and never tests validity. Consider one explicit sentence
  distinguishing "recourse validity" (their axis, unmeasured here) from
  "recourse consistency" (your axis).
- **"Robustness" vs "stability"**: Alvarez-Melis robustness is a local-Lipschitz
  property over input space; Goalpost stability is set-Jaccard over repeats at
  a point. Same word family, different mathematics.
- **Agreement metrics**: Atil's TARa@N is exact-agreement over N runs; your
  Decision Stability is modal-agreement rate over N=5. Close but not identical
  — a reviewer will check.
- **"Reason stability" at the target's own four-heading granularity** has no
  counterpart in the attribution-stability literature, which works at feature
  granularity — the write-up's granularity caveat is also a formalism gap.
