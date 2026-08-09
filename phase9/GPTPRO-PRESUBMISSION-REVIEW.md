# Pre-submission review — GPT-5.6 Sol Pro (2026-08-09)

*Provenance: obtained by the author prompting GPT-5.6 Sol Pro with the
paper PDF; relayed verbatim into the working session on 2026-08-09.
Adoption of its five blockers is recorded in DECISIONS.md D-073; every
adopted point was verified against the repository record before being
applied. The two earlier reviews by the same model (the A1 statistical
critique, D-052, and the seven-point pre-publication review, D-065) are
author-held session records — see the paper's Acknowledgements.*

---

Verdict
The work is ready to become a public, citable preprint. This exact release candidate still needs one final evidence-bound correction pass.
You do not need another experiment before publishing. The contribution is already substantial enough:

* a defined construct—same-input re-query stability of decisions, reasons and LLM-authored recourse;
* an exact certification rule rather than a vague "judge seems reliable" check;
* a real refusal pathway that withheld results three times;
* matched-control evidence;
* a preregistered causal extension;
* complete provenance and a public evidence repository.

The gate is now properly self-contained in the paper, including its Boolean condition and the important limitation that it certifies repeatable extraction, not semantic truth. The causal extension is also conceptually distinctive and clearly separated from mere stability measurement.
That is enough for arXiv. But I would not freeze and submit the current PDF until the following claims are corrected.
The remaining publication blockers
1. The control supports a weaker attribution than the drafts currently claim
The paper currently says:
"verdict-flipping belongs to the model"
"the reason–recourse gap and the valence amplification belong to the design"
The Substack uses the same "what belongs to the model/design" construction.
The control establishes that the chain is not necessary for verdict flipping: flips occurred in both the chained pipeline and the bare model. It does not prove that the chain has precisely zero effect on the probability or location of flips. Three cases versus four cases, with 25 cases per arm, cannot identify that.
Likewise, the larger reason–recourse gap and valence-flip rate are strongly associated with the chained design under the matched comparison, but "belong to the design" sounds fully causal.
A defensible replacement is:
Verdict instability occurred both with and without the chain, showing that the chain is not necessary for the phenomenon; this sample does not identify whether the chain changes its frequency. Under the matched model, host, corpus and reader, the chained configuration exhibited a substantially larger reason–recourse contrast and greater valence instability. I treat this as design-associated evidence rather than a clean causal estimate.
That preserves the actual result and removes an obvious reviewer target.
2. The causal hypothesis's effective denominator must be stated
The causal section reports eight borderline candidates and 220 runs, followed immediately by the conclusion that the consensus-versus-singleton hypothesis was not supported.
But the repository's adversarial audit found that the registered consensus-versus-singleton comparison was actually evaluable for only two retained cases. It also found that "14 of 20 advised edits" refers to 20 edit-by-block effect estimates generated from 10 valid edits, not 20 unique edits.
This distinction needs to appear in the paper, abstract, README and any public explainer.
Use something like:
The registered consensus-versus-singleton hypothesis was evaluable on two retained cases and did not meet its two-block replication criterion. Across ten valid advised edits evaluated in two independent blocks, 14 of 20 block-specific effect estimates were exactly zero against placebo; five of ten edits were zero in both blocks.
The abstract's current phrase—"most advised edits had zero measured effect"—should become:
"14 of 20 block-specific advised-edit effect estimates were zero."
The current wording is rhetorically cleaner, but it risks being read as 14 distinct interventions.
3. Measurement artifacts cannot simply be assumed to cancel
The drafts currently argue that whatever measurement artifact exists applies equally to the pipeline and control, making the difference attributable to the design.
The matched comparison is valuable, but the two architectures produce differently structured prose. The reader, normalisation grain and architecture can interact. A pipeline with four fixed headings is intrinsically easier to extract at topic level than unscaffolded bare-model prose. Therefore the artifacts do not necessarily enter both arms identically.
Replace "applies to both sides equally" with:
The matched control narrows several major confounds because model, host, corpus, settings and reader are held constant. It does not guarantee that architecture-specific output structure interacts identically with extraction and granularity, so the contrast is evidence of a design-associated effect rather than a fully identified causal quantity.
The valence comparison remains your strongest design result because it conditions on the same topic and asks whether its sign changes. That is much less vulnerable to the coarse-topic/fine-advice asymmetry.
4. Remove the remaining generation-wide generalisation
Near the end, the Substack says:
"verdict instability is a property of this generation of models"
Your evidence is that it appeared in every configuration you measured. That is notable, but eight selected configurations do not establish a property of the entire model generation.
Use:
"Verdict instability appeared in every configuration measured, including configurations run at temperature zero."
This is still strong, fully supported and much harder to dispute.
5. Reconcile the release surfaces
The public repository currently creates a few avoidable contradictions:

* The README says Audit #1 was run "exactly as shipped," although the model pin was retired and the paper correctly describes a disclosed substitute.
* The README's Audit #3 description treats 14/20 as 20 separate edits rather than 20 block-specific estimates.
* The README says three audits of published screening tools; more precisely, it is three audits across two published tools, with the third being a causal follow-up on the first.
* The README says Python 3.12, while the package metadata currently permits Python 3.11 and above.
* `CITATION.cff` still describes the paper as a draft whose arXiv identifier remains to be added, and it has no archived DOI yet.

The paper's summary table also splits awkwardly across pages 7 and 8, with the Audit #1 row beginning on one page and continuing on the next. Prevent the row split, add a numbered caption, and avoid leaving the final reference alone on a nearly empty page. These are not scientific defects, but the first arXiv version should look deliberate.
What is now genuinely citable
The most citable part is not the figure 0.448. It is the protocol architecture:
A stability claim extracted by an LLM is certified only when the reader's own measured self-agreement clears a preregistered bar, with a stricter margin where extraction noise could manufacture apparent instability; otherwise, the result is published as withheld.
The exact rule,
[
\operatorname{certified}(s,a)
\iff
a\geq0.90 \land
\left(s\geq0.85 \lor a-s\geq0.15\right),
]
gives future researchers something concrete to adopt, modify, criticise or benchmark.
Other highly citable contributions are:

* treating withheld as a first-class audit result;
* separating decision, reason, recourse and valence stability;
* making elicitation mode part of system identity;
* comparability walls for cross-system displays;
* endpoint pinning in stability audits;
* testing whether an LLM system's own advice has causal effect when implemented;
* publishing the instrument's refusal and correction history alongside its successful findings.

The refusal record is especially persuasive because it demonstrates that the gate had consequences rather than being added retrospectively as ceremonial methodology.
The publication sequence that maximises citationability

1. Make the five corrections above and rerun the repository's claim-binding, freshness and stale-copy checks. Freeze the exact commit used to produce the paper.
2. Create a numbered GitHub release and archive it through Zenodo. Zenodo's GitHub integration can archive releases and mint a DOI; GitHub's `CITATION.cff` support then presents a "Cite this repository" entry when the metadata is populated.
3. Keep two distinct citation objects:
   * the paper, cited through its arXiv identifier;
   * the instrument and evidence release, cited through its Zenodo DOI.
The paper should be the preferred citation for the method and findings. The software DOI should be cited when someone uses Goalpost itself or depends on the archived evidence.
4. Submit the protocol to arXiv with `cs.CY` as the primary category and request a `cs.LG` cross-list. `cs.CY` fits the governance, contestability and public-policy contribution; `cs.LG` fits the robustness and evaluation-methodology contribution. ArXiv's taxonomy supports that division, although final classification and cross-listing remain subject to moderation.
5. Submit source rather than only the PDF where practical. ArXiv prefers TeX/LaTeX source for TeX-generated work, and new submitters may also encounter category-endorsement requirements.
6. Publish the Substack once the arXiv identifier and software DOI exist. Put a citation box immediately beneath the opening note:

Horsburgh, J. (2026). Goalpost: A Certification-Gated Protocol for Auditing the Stability of LLM Screening Decisions, Reasons, and Recourse. arXiv:XXXX.XXXXX. Software and evidence: Zenodo DOI.
This prevents the public write-up from circulating without a stable scholarly object for readers to cite.
Add a keywords line to the paper as well:
Keywords: LLM auditing; algorithmic recourse; repeatability; automated hiring; contestability; explanation stability; LLM-as-judge.
Will it actually get citations?
No publication can guarantee citations. But this has a credible route to them because it offers both:

* a specific empirical phenomenon—decision-attached advice that changes under identical re-querying; and
* a portable methodological object—certifying an LLM-based measuring instrument before permitting it to make instability claims.

The portable method is the more promising citation engine. Researchers working on LLM-as-judge reliability, algorithmic recourse, AI auditing, automated hiring, contestability and nondeterministic systems can cite the certification gate even when they are not studying CV screening.
My call is therefore:
Hold the current build, make one final non-experimental correction pass, archive the release, and submit. Do not delay v1 for more models, more targets or human-rating experiments. Those belong in the next paper.
