# WRITEUP_TEMPLATE.md — skeleton for the public piece

Working title options:
- *"I asked N AI screening systems the same question five times. The advice
  changed; the reasons didn't."*
- *"Moving goalposts: measuring whether AI hiring advice stays put"*

Target: non-specialist publication or personal blog; a reader who has never
seen a Jaccard index should finish it. Every number below slots in from a
committed audit's metrics JSON — nothing hand-copied.

---

## 1. Cold open — the sat-nav (≈150 words)

The sat-nav paragraph (README/report verbatim). Then the stakes in one
line: the people most affected — job applicants, loan applicants, benefits
claimants — need explanations to be *actionable*, not decorative.

## 2. What I did (≈200 words)

- "I built an open instrument, Goalpost, from my Honours research on
  explanation drift." One sentence on the dissertation finding, with the
  honest bridge: *the original study measured an AI explaining a fixed
  decision; this tool measures the AI making and explaining its own.*
- The experiment, in one breath: `[N_SUTS]` systems × `[N_CASES]` fictional
  CVs × `[N_REPEATS]` identical runs each, temperature zero, everything
  recorded. Total cost: `[$COST]` — "auditability is cheap; opacity is a
  choice."

## 3. The headline table (the one visual most readers take away)

| System | Decision kept | Reasons stable | Advice stable |
|---|---|---|---|
| `[SUT_1]` | `[D_1]` | `[REASON_1]` | `[RECOURSE_1]` |
| … | | | |

Lay caption pre-drafted: *"Ask `[SUT_X]` twice and, when the decision
comes back the same, on average only
`[FRACTION]` of its recommendations appears both times."*

## 4. What it means (≈250 words)

- The asymmetry: systems are steadier about *why* than about *what to do*.
- The temperature-zero point, in lay terms: this isn't a randomness dial
  left up — it persists with the dial at zero.
- If observed: decisions themselves flipped on identical inputs `[K]` times
  in `[TOTAL]` runs — one sentence, not oversold.
- The contestability frame: advice that moves can't be acted on, and a
  rejection you can't act on is harder to meaningfully contest.

## 5. The uncertainty box (pre-drafted; keep intact)

> **What this measurement is not.** It is not an accuracy or fairness
> audit: a system can give perfectly consistent and perfectly wrong
> answers, and consistency is all I measured. The CVs are fictional by
> design. The numbers depend on a published synonym-grouping step — I
> report the ungrouped numbers alongside (they are never higher, and
> for nearly every system lower). These are measurements of specific configurations I set up and
> controlled, on specific dates, with the full transcripts published; they
> are not claims about any vendor's product as deployed. And comparisons
> with my original 2026 study are directional only — the study measured a
> different (narrower) pipeline.

## 6. Comparison to the dissertation (≈150 words)

The 2026 study: reasons 0.89, advice 0.36, at temperature zero. Today's
models: `[RANGE]`. Frame honestly: *the gap persists in direction and
appears narrower in size — measured differently, so I'd call it an
evolution, not a replication.* If recourse stability has genuinely
improved, that is good news worth reporting straight.

## 7. Kick the tyres (≈100 words)

Repo link (when public), one-command quickstart, the invitation: every
transcript behind every number in this piece is in the repo; run it
against your own configuration for about the price of a coffee. Reports
carry a provenance stamp so screenshots stay traceable.

---

### Slot-filling checklist (from `audits/<id>/metrics/<v>/metrics.json`)
- [ ] `[N_SUTS]`, `[N_CASES]`, `[N_REPEATS]`, `[$COST]` — audit header + `total_cost_usd`
- [ ] Per-SUT table — `conditions[].aggregates` (cluster means + IQRs) and
      decision stability per case; quote medians/IQR where means mislead
- [ ] `[FRACTION]` — reporter's `headline_statistic` for the chosen SUT
- [ ] Decision-flip counts — per-case `decision_stability.modal_agreement`
- [ ] Raw-vs-cluster ladder numbers for the uncertainty box
- [ ] Perturbation line (if run): decision flips under immaterial edits
- [ ] Provenance footer: audit id, goalpost/taxonomy/anchors versions
