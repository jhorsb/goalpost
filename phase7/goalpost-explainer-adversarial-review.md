# Goalpost explainer: adversarial review and rebuild rationale

## Verdict

The supplied page fails its main communication job. It demonstrates the verdict flip well, then spends roughly two phone screens on definition, provenance and a horizontally scrolling process before it reaches the reason to trust Goalpost. A 40-second reader leaves with “AI hiring can be inconsistent,” but not the more important clause: “this instrument has refused its own result.”

Its visual language is generated “editorial SaaS”: warm cream, teal, serif body copy, monospace micro-labels, nested rounded cards, status chips, an analytics chart, a four-card scoreboard and a project timeline. The style supplies seriousness as a surface treatment. It does not encode the page’s real epistemic structure.

Line references below refer to the attached one-pass snapshot at commit `14f46f3`, before the concurrent provenance correction in `1d2f8aa`. The correction changes some evidence facts; it does not remove the design problems.

## Task 1: the AI tells

### Palette and type

1. **Lines 4–15: `#f6f5f1` paper, `#14606b` accent, green certification and rust withholding.**
   - Why it reads machine-made: cream + charcoal + muted teal is the default “serious editorial explainer” palette; green/rust adds a stock SaaS status layer. None of it comes from repeated trials, calibration or refusal.
   - Fix: use an audit-sheet palette—paper, ink and rules—with one distinct reporting colour and one refusal colour. The subject calls for test-bench clarity, not tasteful magazine ambience.

2. **Lines 11–14, 92–93, 140, 153–154 and 213–217: the same green/rust pair means ACCEPT/REJECT and PASS/WITHHELD.**
   - Why: default traffic-light semantics were applied without examining the categories. It implies acceptance is “good” and rejection “bad,” then reuses the same moral coding for measurement integrity.
   - Fix: render hiring outcomes neutrally with solid/pattern contrast. Reserve status colour for Goalpost’s publish/stop decision.

3. **Lines 17–35: the dark theme is a formulaic inversion of the light palette.**
   - Why: it preserves the decorative palette rather than the semantic hierarchy.
   - Fix: retain semantic roles across themes—neutral hiring verdicts, high-contrast refusal, clearly secondary evidence notes—and tune each token for contrast.

4. **Lines 41–50: Charter/Iowan serif body + Avenir/Segoe headings + monospace metadata.**
   - Why: this is the generated shorthand for “editorial authority plus technical credibility.”
   - Fix: use one workmanlike system sans for prose and headings. Use tabular monospace only for versions and exact measurements.

5. **Lines 49–50, 58–60, 82–83, 107–109, 131, 143, 145–146, 151–152, 161, 178–179 and 192: monospace is sprayed over labels, dates, chips, values and legends.**
   - Why: small uppercase mono is being used as a lab coat rather than a data format.
   - Fix: write ordinary labels in sentence case. Let structure and provenance carry rigour.

6. **Lines 44 and 52: `76ch` wrapper and `68ch` paragraphs.**
   - Why: these are stock long-form article defaults, not dimensions derived from a 40-second task.
   - Fix: use a short causal path at the top; widen only the comparisons that genuinely need two columns.

### Hero conventions and decorative structure

7. **Lines 56–77 and 202–220: eyebrow → giant wordmark → rhetorical thesis → rounded demo card.**
   - Why: this is the canonical generated landing-page hero. It spends the first viewport on brand convention rather than the instrument’s integrity mechanism.
   - Fix: make the observed contradiction the headline and put the refusal rule immediately after it.

8. **Line 203: “An audit instrument · evidence-first · target identities withheld pending disclosure.”**
   - Why: tiny uppercase mono, three clauses and middle dots are generic trust-signalling. “Evidence-first” asserts the virtue instead of proving it. “Withheld” also gets used for two unrelated concepts: anonymous targets and failed measurements.
   - Fix: say targets are anonymised during disclosure in a separate note. Reserve WITHHELD for the measurement status.

9. **Lines 205–206: the duplicated outlined GOALPOST ghost.**
   - Why: fashionable hero decoration. If it is meant to suggest repetition, it is too coy to teach anything.
   - Fix: remove it and make the five repeated outcomes the visual motif.

10. **Line 208: “Does an AI hiring tool give the same answer twice? Usually. And that’s the problem with ‘usually.’”**
    - Why: rhetorical question, fragment, delayed aphorism and scare quotes are classic AI keynote cadence. “Usually” can reassure the reader.
    - Fix: “The same CV received opposite verdicts across five identical runs.”

11. **Lines 210–220: the strongest result is a pale rounded card containing five smaller cards.**
    - Why: nested cardification makes the evidence look interchangeable with KPI or pricing tiles.
    - Fix: use one joined specimen strip with a shared “same CV / same settings” label.

12. **Lines 211 and 219: the invariant is explained above and below the visual.**
    - Why: generated over-explanation does not trust the visual to carry its own load.
    - Fix: label the invariant once, then attach “3–2 split” and “3 / 25” directly to the strip.

13. **Lines 89–100: the five outcomes fade in from `.15s` through `1.55s`.**
    - Why: the stagger flatters the component and briefly hides the evidence. It explains nothing.
    - Fix: render all outcomes immediately. Do not animate page-load evidence.

14. **Lines 86–93: each run is an isolated mini-card.**
    - Why: the relation that matters is that all five outputs share one unchanged input; separated tiles weaken that relation.
    - Fix: join the outcomes on one baseline inside one test strip.

### Component-factory structure

15. **Lines 103–109 and every section from 223–377: identical `4rem` rhythm, kicker, H2, paragraph and component.**
    - Why: the page was assembled from one section template. The gate and timeline receive the same rhetorical weight.
    - Fix: make the gate spatially dominant; subordinate chronology and provenance.

16. **Lines 224, 232, 245, 302, 351 and 366: “What this is,” “How one audit works,” “The integrity mechanism,” and similar kickers.**
    - Why: decorative document-category eyebrows add no information.
    - Fix: use headings that state the operation or consequence.

17. **Lines 80–81, 86–87, 114–115, 125–126, 157 and 169–170: the same pale fill, one-pixel border and small radius for every object.**
    - Why: safe-card styling makes trials, stages, measurements, refusals and findings look epistemically interchangeable.
    - Fix: use spacing and rules for ordinary content. Reserve a containing shape for the stop/withhold decision.

18. **Lines 112–122 and 234–241: six equal pipeline cards joined by arrows.**
    - Why: stock “How it works” component. The difficult fifth stage is offscreen on a phone.
    - Fix: collapse the main method to fixed reply → repeated reader → publish/stop. Put hashes and normalisation in technical detail.

19. **Line 122: the gate gets only a teal border and inset shadow.**
    - Why: generic selected-card styling is carrying the project’s proudest feature.
    - Fix: make the gate visibly stop the flow and branch to “eligible to report” or “WITHHELD.”

20. **Lines 125–148 and 249–283: rounded analytics card, tracks, dots, threshold line, axis and four-item legend.**
    - Why: the chart component came before the comprehension problem. It requires position, colour, fill and legend decoding.
    - Fix: print each exact check beside “passes,” “fails” or “claim withheld.”

21. **Lines 253–272: exact values exist only in `title` attributes.**
    - Why: invisible precision is a one-pass chart hack. Touch users cannot access it; the dots are not keyboard-focusable.
    - Fix: make every value visible text.

22. **Lines 277–282: the legend comes after the chart and encodes filled/hollow plus green/rust.**
    - Why: the visual cannot stand alone.
    - Fix: directly label reasons and advice in each row; repeat the status in words.

23. **Lines 151–155, 247, 308, 319, 329 and 340: uppercase outlined status chips.**
    - Why: certification becomes a generic app state. The third “info” colour further muddies a mechanism that must be exact and field-specific.
    - Fix: use explicit bands: “reader check passed—eligible to report” and “reader check failed—WITHHELD.”

24. **Lines 285–298: three refusals become an equal-row ledger.**
    - Why: the page turns its main act of integrity into release-note chronology.
    - Fix: feature the first refusal as a worked example; keep the other two in a compact audit trail.

25. **Lines 306–347: audited pipeline, control, partial second audit and lab backdrop all use one card template.**
    - Why: four unequal evidence roles look equally comparable. This recreates the dense predecessor dashboard in a nicer skin.
    - Fix: pair Audit #1 with its same-model control, separate Audit #2’s field-level statuses, and label the lab evidence as context.

26. **Lines 315, 325, 336 and 345: every scorecard ends in a miniature interpretation footer.**
    - Why: “metrics + insight” factory syntax compensates for a layout that does not reveal relationships.
    - Fix: use one caption for the paired comparison and one explicit status explanation for Audit #2.

27. **Lines 350–363: five identical left-rule finding blocks.**
    - Why: standard “five takeaways” listicle repeats the scorecard evidence rather than sharpening it.
    - Fix: keep each bounded claim beside the comparison that supports it; move secondary observations down-page.

28. **Lines 365–376: horizontal project timeline with highlighted NOW.**
    - Why: stock portfolio-journey theatre. It advertises progress and demands another phone swipe.
    - Fix: put current disclosure status and dates in a collapsible record.

29. **Lines 379–380: tiny muted credibility colophon.**
    - Why: important evidence-chain and anonymity facts become editorial ambience.
    - Fix: separate evidence trail, anonymity and cost into labelled method notes.

30. **Lines 113, 127 and 167: `min-width: 720px`, `560px` and `290px`.**
    - Why: the mobile strategy is “keep the desktop component and make it scroll.”
    - Fix: stack the teaching sequence. Permit horizontal overflow only for a comparison whose columns must remain aligned.

### Copy tells

31. **Line 225: “An instrument, not an opinion.”**
    - Why: canonical “isn’t X, it’s Y” positioning copy.
    - Fix: state the operation: “Goalpost runs each fictional CV five times through the same tool.”

32. **Line 226: “one property: repeat-stability” plus the bold decision/reasons/advice triad and another question.**
    - Why: coined noun + colon + bold triad + rhetorical question is over-authored explainer copy.
    - Fix: use three plain rows showing what is compared.

33. **Line 227: “Advice that reshuffles … isn’t guidance — and regulation …”**
    - Why: negation, em dash and broad policy claim aim for gravitas instead of comprehension.
    - Fix: use one concrete consequence: a candidate cannot know which changing reason to challenge.

34. **Line 228: dissertation origin, `0.89 vs 0.36`, scalability and “price of a coffee” in one paragraph.**
    - Why: startup-origin and coffee-price clichés interrupt the main argument.
    - Fix: move provenance and exact costs to the record; anchor the decimals on a defined scale.

35. **Lines 235–240: “Frozen corpus,” “Their system, our keys,” “quirks-and-all,” “Normaliser,” “taxonomy,” “Evidence file.”**
    - Why: slogan labels and insider nouns perform rigour instead of teaching the method.
    - Fix: “lock fictional cases,” “run the published setup,” “turn prose into lists,” “test the reader,” “report or withhold.”

36. **Line 246: “The gate: measurements that can refuse.”**
    - Why: portentous colon headline does not say what stops or why.
    - Fix: “If the reader cannot repeat itself, Goalpost withholds the result.”

37. **Line 247: “The obvious attack … maybe your reader is the unstable one … manufacturing ‘instability’ out of nothing.”**
    - Why: imagined-sceptic debate script dramatizes the objection in a dense paragraph because the mechanism has not been visualised.
    - Fix: show one fixed reply being read three times, then branch to pass or stop.

38. **Lines 251–269: “first lens,” “rebuilt lens,” versions, model, dates, scaffold and freeze status.**
    - Why: metadata accumulation is used as credibility texture before the reader understands the gate.
    - Fix: lead with “first reader: claim stopped,” “rebuilt reader: passed,” and move versions into the record.

39. **Lines 287, 291 and 295: “No #1—and a rescue,” “No #2—the selection effect, proven,” “No #3—and this time, no rescue.”**
    - Why: numbered triad, repeated em-dash cadence and escalating drama are unmistakably machine-shaped. “Proven” is stronger than necessary.
    - Fix: use procedural titles naming which rule fired and what was withheld.

40. **Line 304: “Cluster-level numbers (synonyms grouped; ungrouped always lower…).”**
    - Why: the generic “Scoreboard” is followed by parenthetical throat-clearing about vocabulary it should have translated.
    - Fix: say “equivalent wording counted together” and move raw-score detail to the glossary.

41. **Line 325: “verdict-flipping belongs to the model; the explanation pattern belongs to the design.”**
    - Why: neat mirrored antithesis overstates causal attribution.
    - Fix: bound the inference: removing the workflow did not remove flips; it did change the measured explanation pattern.

42. **Lines 352–362: “Five things we now know,” “verdict lottery,” “manufacture,” “flip,” “quietly stop existing.”**
    - Why: listicle number plus five headline-ready metaphors trades calibration for quotability.
    - Fix: integrate the model, workflow and explanation claims with their comparison; keep only genuinely additional observations in a later section.

43. **Line 362: “possibly a finding about the tool, not the reader.”**
    - Why: speculation is tucked after a decisive conclusion, allowing the copy to sound bold and cautious simultaneously.
    - Fix: label the attribution unresolved until a passing independent reader checks it.

44. **Line 380: “Every number … transcript … hash … config … pinned versions … disclosure … spend.”**
    - Why: one comma-heavy credibility bundle tries to satisfy technical peers after the narrative has ended.
    - Fix: use three labelled notes: evidence trail, anonymity and cost.

45. **Across lines 203–380: repeated em dashes, middle dots, triads and antitheses.**
    - Why: nearly every label becomes “claim — qualifying flourish” or a metadata triplet. The cadence is a house style rather than a comprehension aid.
    - Fix: prefer short subject–verb sentences and explicit field labels.

The largest structural tell is repetition: the demo, gate paragraph/chart/ledger, scoreboard and five findings explain the same material four times. This is generated completeness masquerading as communication.

## Task 2: where a non-expert falls off

### The measured 40-second path

At a `390 × 844` viewport, the supplied gate started at `1,946px`, after about 345 words and roughly 2.3 screens. The chart began at `2,370px`; the page was `6,983px` tall. A fast policy reader gets the hero and the general definition, then leaves before the page’s central trust claim.

The rebuild moves the gate to immediately after the first trial strip. The opening path is now: same CV → opposite verdicts → why prose needs a reader → why the reader must repeat itself → publish or stop.

### Early stalls and misreads

- **Lines 203–208:** “withheld” first means anonymous identities, then later means failed evidence. “Usually” can sound reassuring. Use “anonymised during disclosure” for targets and reserve WITHHELD for measurement status.
- **Lines 210–219:** “One real measurement” can imply a real applicant even though the CV is fictional. Say “one fictional candidate, submitted unchanged.”
- **Line 219:** “worst case” invites a cherry-picking objection unless the two audit-level frequencies sit beside it.
- **Lines 223–228:** 148 words of definition, regulation, origin story, unexplained decimals and coffee pricing delay the gate.
- **Lines 231–241:** the six-stage method makes the reader swipe past the normaliser before discovering the gate.

### Why the old gate does not land

The supplied explanation jumps from “the reader may wobble” to “the claim is certified.” A non-expert can hear “one AI agrees with another AI, therefore it is right.” The missing causal chain is:

1. Hold one hiring-tool reply fixed.
2. Ask the reader to extract that exact reply repeatedly.
3. If the extracted lists change, variation may come from the measuring reader.
4. Stop. Do not attribute that variation to the hiring tool.
5. Only a reader repeatability pass makes the measure eligible to report.

Passing establishes repeatability, not correctness. A consistently wrong reader can pass. “Certified” therefore needs a narrow definition: eligible to report after the reader-repeatability rule, not true, accurate or fair.

The concurrent provenance update makes the rule more exact. There are two thresholds:

- the reader must meet `≥ 0.90` at all;
- an instability claim must clear a stricter margin.

The first refusal is the strongest integrity example because the reasons check was `0.904`: above `0.90`, but `0.051` below the `0.955` margin required for that claim. The instrument did not withhold all numbers; it withheld the favourite instability claim.

### Why the dot chart fails

- It is about `605px` wide inside a `348px` content area.
- At the initial scroll position, row labels are visible but the dots and threshold are not.
- After scrolling right, dots appear but the row labels disappear.
- Filled/hollow means reasons/advice; colour means pass/fail. Neither mapping is intrinsic.
- Exact values live in hover-only `title` attributes, unavailable on touch and unreliable for keyboard or screen-reader users.
- One failed dot does not reveal whether a field, a claim or the whole audit is withheld.
- The original first reasons dot was materially wrong. It showed `0.899` at `69.8%` on a `0.50–1.00` axis, where that value would belong at `79.8%`. The primary record later corrected the value to `0.904` and the relevant rule to the `0.955` margin.

The replacement uses a text-labelled table: exact value, inequality, rule outcome and what may be reported. No legend is needed.

### Certified versus withheld

In the supplied snapshot, `0.719` and `0.567` were printed in ordinary metric rows, grey and struck through. That reads as deleted, disabled, coyly hidden or broken. It also contradicts “WITHHELD instead of a number.”

The replacement quarantines failed-reader calculations in a high-contrast double-border block. It says why the value is retained, which reader failed, what later passed, and that the failed-reader values are not findings and must not be cited. Colour is redundant to the words and border treatment.

The concurrent backup-reader result also changes the correct story. Audit #2 is no longer “decisions certified; explanations withheld indefinitely.” The primary reader and sole backup were locked before any target reply; the backup passed and no further retry was allowed. Both reader results are shown: the primary reader is visibly withheld, while the backup licenses the published `0.729` and `0.556`. The two readers disagree about their own repeatability but return nearby target measurements.

### Number literacy

| Display | Likely novice reading | Concrete treatment |
|---|---|---|
| `3 / 25`, `4 / 25`, `6 / 25`, `7 / 25` | Immediately meaningful | Lead with these natural frequencies. |
| `0.968`, `0.936` | “Almost perfect, so no problem” | Keep secondary to flip counts and define as an average across repeat comparisons. |
| `0.983`, `0.448` | Uninterpretable grades | Put topic overlap beside meaning reversal; label `1.00` as matching lists and state that the score is not a percentage of runs. |
| `0.904`, `0.902`, `0.895`, `0.817`, `0.876`, `0.814`, `0.989`, `0.975` | Decimal noise | Print each beside the relevant `0.90` or `0.955` rule and a word outcome. |
| `0.535 / 0.537` | Two unexplained measures | Label as the reason–advice gap from two reader setups. |
| `+0.106` vs `+0.537` | Improvement or change score | Show pipeline and same-model control in aligned columns; label it a gap, not a benefit. |
| `⅓ – ½` | Understandable | Put directly beside “same topic, opposite sign.” |
| `0.719`, `0.567` | Still appears citable | Keep only in a WITHHELD primary-reader block; show the passing fallback values separately. |
| `+0.12 … +0.29`, `0.50 – 0.68` | Scale-free decoration | Keep in explicitly secondary lab context. |
| `$0.28`, `$4.00`, `under $12` | Distracts from validity | Retain in method/provenance, not the headline hierarchy. |

Do not translate overlap scores into percentages unless the metric itself is a frequency. `0.448` is not safely paraphrased as “44.8% of advice repeated.”

### Vocabulary that causes stalls

| Supplied term | Plain-language replacement |
|---|---|
| audit instrument / integrity mechanism | a test; the reader repeat-check |
| LLM-based / repeat-stability | AI text model; same-input repeatability |
| pipeline / prompts and wiring / scaffold | multi-step screening workflow |
| corpus | locked fictional CV/job cases |
| reader | a separate AI that turns prose into lists |
| self-agreement | repeat-check on the exact same reply |
| normaliser / taxonomy | groups equivalent wording such as “work history” and “experience” |
| lens | reader setup |
| cluster-level | equivalent wording counted together |
| temperature | a randomness-related setting; use the tool’s own value |
| pre-registration / pre-declared | rules locked before target replies existed |
| certified | eligible to report after the reader-repeatability rule |

Technical terms remain in a glossary for peers; they no longer block the novice path.

### Why the four scoreboard cards fail

The four cards have different epistemic jobs:

1. Audit #1 is a published tool.
2. The control exists only to interpret Audit #1.
3. Audit #2 is a second published tool with reader-specific provenance.
4. The lab backdrop is context from researcher-built systems with no reader in the path.

Equal cards imply equal purpose. On a phone, the pipeline and control cannot be compared without memorising earlier decimals, and the lab looks like a fourth target audit.

The replacement makes the control logic visible:

- **Held constant:** the same serving model, cases and settings.
- **Changed:** remove the multi-step workflow.
- **Observed:** verdict flips persist (`3 / 25` versus `4 / 25`); the explanation gap changes (`+0.537` versus `+0.106`).
- **Bounded inference:** removing the workflow does not remove flips; workflow design changes the measured explanation pattern.

Audit #2 is structurally separate. The lab backdrop is explicitly labelled “not a fourth target audit.”

### Accessibility and mobile failures

- Gate values are hover-only.
- Pass/fail relies on colour and a legend.
- The dim withheld token is about `2.55:1` on light and `2.72:1` on dark, below normal-text contrast.
- Labels at `0.66–0.78rem` fall around 11–13px.
- At a 320px viewport, the `290px` scorecard minimum can exceed the padded content width.
- Pipeline, gate chart and timeline scrollers have no accessible name, focus stop or overflow cue.
- The gate itself requires horizontal exploration.
- The load animation delays the fifth result by roughly two seconds.
- `<s>` alone does not communicate “uncertified calculation” to assistive technology.

The replacement has no load animation, no body-level horizontal overflow, visible focus, directly labelled statuses, high-contrast withheld treatment, and labelled/focusable overflow regions only where aligned columns are useful.

## Task 3: design plan

### Palette

Six light-theme source colours, with token-equivalent dark values:

- **Calibration paper** `#F4F1E8`: page field.
- **Evidence white** `#FFFEFA`: fixed replies and report surfaces.
- **Graphite** `#171A20`: text, rules and neutral target verdicts.
- **Slate** `#5B6570`: secondary explanation.
- **Report cobalt** `#155EEF`: reader check passed; eligible to report.
- **Stop vermilion** `#B42318`: reader check failed; claim or measure withheld.

Hiring ACCEPT/REJECT outcomes use graphite, white and pattern rather than cobalt/vermilion. Status colours are reserved for the instrument’s decision.

### Type pairing and scale

- System sans: `-apple-system`, BlinkMacSystemFont, Segoe UI, Helvetica, Arial.
- System monospace only for exact measurements, versions and reader records.
- Scale: 13px labels, 17px body, 18–23px supporting leads, 32–62px section heads, 42–94px hero depending on viewport.

There is no serif “editorial authority” voice and no decorative webfont dependency.

### Layout concept

An evidence strip followed by a stop gate:

`unchanged fictional CV → five visible verdicts → fixed prose reply → three reader passes → eligible to report / WITHHELD`

The novice story stacks in one phone column. The only horizontal regions are the Audit #1/control comparison and the exact technical gate table; both have accessible names, focus states and a swipe cue.

### Single organising idea

**Test the ruler before trusting the measurement.**

The gate is not a caveat after the result. It is the page’s central event. A refused claim is evidence that the instrument’s author cannot force the answer they want.

## What changed and why

- Replaced the brand-first hero with the concrete same-CV contradiction.
- Put the three refusals and the gate directly after the trial strip.
- Made all five target verdicts static and immediately visible.
- Separated neutral hiring outcomes from Goalpost’s reporting statuses.
- Replaced the dot chart with visible inequalities and text outcomes.
- Explained field-specific gating and the difference between repeatability and correctness.
- Integrated the new two-threshold provenance: `0.904` passed the basic bar but missed the `0.955` instability margin by `0.051`.
- Integrated Audit #2’s locked backup reader: the failed primary audit trail and passing backup remain side by side.
- Preserved the supplied snapshot’s superseded `0.899`, `5 / 25`, `0.944`, `0.719` and `0.567` in a closed reconciliation record rather than silently erasing them.
- Resolved the sample description with the canonical statement: 25 fictional CVs, five for each of five roles, one job spec per role, each run five times = 125 pipeline runs per audit.
- Paired Audit #1 with its same-model control and wrote the bounded inference beside it.
- Used one certified reader setup on both sides of that comparison, with its gate records visible; kept the other certified Audit #1 reader as separate provenance rather than mixing lenses.
- Removed the duplicate five-item recap. The model, workflow and explanation claims now live with their evidence; only additional governance findings remain below.
- Split the second target audit from lab context.
- Replaced grey strikethrough with an explicit, high-contrast failed-reader quarantine.
- Kept exact costs, dates, versions, ranges and provenance below the novice path.
- Defined technical vocabulary in a progressive disclosure.
- Added both token-level themes, explicit viewer-toggle overrides, mobile-first layout, reduced-motion handling, visible focus and labelled overflow regions.
- Used no external styles, scripts, fonts, images or identifying target details.

The replacement is `phase7/goalpost-explainer-rebuilt.html`. It is an injectable fragment: metadata, title, inline style and page content only; no document wrapper.
