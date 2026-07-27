# I ran an AI hiring tool five times on the same CV. It changed its mind.

*Draft v3 — from the WRITEUP_TEMPLATE skeleton; every number traces to a
committed audit transcript. Target identity withheld from the prose per
D-024; full identification (URL, pinned commit, content hashes) is in the
audit evidence.*

---

Somewhere on the internet is a free, working AI hiring tool. Anyone can
download it, point it at a folder of CVs and a job advert, and let it
decide who gets an interview. It reads each CV through a chain of four AI
agents, scores the candidate out of 100, and applies a hard rule: above
75, *"I recommend this candidate for the job"*; below, *"I do not."*

I ran it five times on the same CV, with identical settings, and it
rejected the candidate three times and accepted them twice.

Not a candidate I invented to break it — one of twenty-five fictional but
realistic CVs, spanning five different jobs, that I ran through the tool
five times each. On three of the twenty-five, the verdict changed across
identical runs. Same CV on Tuesday, different answer on Thursday.

Imagine a sat-nav that always tells you *why* you haven't arrived —
"you're 40 miles out" — but gives you contradictory directions every time
you ask how to get there. The explanation is consistent; the route is
noise. I built an instrument to measure whether automated screening
systems are that sat-nav. It turned out this one couldn't even agree on
whether you'd arrived.

## Where this comes from

In 2026 I finished an undergraduate dissertation with one central finding:
when a language model explains an automated hiring decision, the *reasons*
it gives are far more stable across repeated identical queries than its
*advice* — what the candidate should change to succeed. Reasons scored
0.89 on a 0-to-1 similarity measure; advice scored 0.36. The gap survived
turning the model's randomness setting to zero, which means you can't fix
it with a dial. It's structural.

That mattered to me because advice is the part that's supposed to be
*actionable*. The people on the receiving end of these systems — job
applicants, loan applicants, benefits claimants — can't meaningfully
contest a decision, or plan their way past it, if the guidance moves every
time they look.

A dissertation proves something once, under lab conditions. So I spent
this summer turning it into **Goalpost**: an open instrument that can
audit any screening configuration its operator controls, and produce two
things — a machine-readable evidence file, and a one-page report a
non-specialist can act on.

## What I did

I audited a published, openly downloadable screening pipeline of a common
design: multiple AI agents in a chain — one extracts the candidate's
details, one extracts the job requirements, one hunts for red flags, and a
final "recruiter" agent scores the match out of 100 and issues a verdict
under fixed thresholds. I ran it entirely on my own accounts and keys,
exactly as its code wires it together, quirks included. Nothing about the
audit touched anyone's hosted service.

The protocol was frozen before any measurement: twenty-five fictional CVs
against five job specs, five identical runs each, at the pipeline's own
default settings. Every API call recorded. Decision, reasons, and advice
pulled from the tool's free-text output by a separate extraction model,
whose own consistency is *measured, not assumed* — more on why that
matters below.

Two substitutions have to be disclosed up front, and one of them is a
finding in its own right:

- **The tool's pinned AI model no longer exists.** Its code specifies a
  model that has since been retired by every provider that served it.
  A published, deployable hiring tool has silently become impossible to
  run as its author shipped it — and nothing in the tool itself would tell
  a deployer that. The model didn't drift; it *ceased to exist*.
- I therefore ran its prompt-and-chain design on a current open-weights
  model of comparable scale. So the precise claim is: **this is an audit
  of the pipeline's design as served by a current open model** — not of
  the artifact as originally deployed, which nobody can run any more.

Cost of the final certified measurement: **$0.28** — about 22p, and
nearly all of it spent on the extraction and checking layers rather than
the tool itself. Independent behavioural validation of a deployed
screening pipeline costs less than a Freddo. (Cumulatively, including
every false start, quota wall and the extractor rebuild described below,
this whole investigation came in under a pound.)

## What I found

Three findings, in ascending order of how much I want a sceptic to
read the small print — and one of them the instrument refused to certify
until I rebuilt the thing doing the measuring.

**1. The verdict moved on identical inputs.** (Certified.) Across
125 runs, the pipeline's accept/reject verdict changed on three of
twenty-five candidates — including one 3–2 split across five identical
runs. The extraction layer's agreement on verdicts was perfect (1.000), so
this number carries no measurement caveat. Twenty-five cases is a small
sample, so I'll say it precisely: *verdict instability was observed at the
tool's own default settings.* I make no claim about the rate at which it
occurs — only that a candidate's outcome from this design can depend on
which run they happened to get.

**2. The advice repeats about half the time.** (Certified, as a lower
bound.) Recourse stability measured **0.448**: ask this pipeline twice
and, on average, fewer than half of its improvement recommendations
appear both times — the least stable advice of anything I have measured
with this instrument, including four frontier-lab configurations. Because
the tool's output is free text, this number passes through an extraction
model, and extraction noise can only make stability look *worse* — so
0.448 is a floor, not a point estimate. The extraction layer's measured
consistency on advice, at the level this claim is made, was 0.932 against
a pre-registered bar of 0.90.

**3. The explanations kept their topics and flipped their meaning.** This
is the finding I did not go looking for, and it is the one I now think is
the real result.

The pipeline's recruiter agent always evaluates under the same four
headings — skills, experience, education, extras. Those headings are
almost perfectly stable across runs: measure "did it discuss the same
topics?" and you get 0.983. But measure whether each topic *counted for or
against the candidate*, and it flips in **roughly half** the cases. Your
experience can be the reason you're recommended on one run and the reason
you're not on the next. The explanation looks stable at the level of what
it mentions, and is unstable in what it asserts.

That is my dissertation's thesis in a sharper form than my dissertation
managed to state it. And it is robust to the measurement worry I have to
raise about the number next to it.

**About the gap — and why I'm not leading with it.** Reasons measured
0.983 and advice 0.448, which is a stability gap of 0.535, wider than
anything I measured on lab configurations. I am reporting it as an
observation rather than a headline, because three things inflate it and I
can't yet say by how much:

- **The two sides aren't measured at the same resolution.** Reasons are
  counted at the level of four fixed categories; advice at the level of
  individual recommendations. Coarse buckets match each other more easily
  than fine-grained items do, so some unknown share of the gap is an
  artifact of measuring the two properties at different grain.
- **My extraction rule was designed after looking at this target.** The
  rule that lifted reason-agreement — "produce one entry per category the
  response uses" — was written once I had seen that this pipeline always
  emits the same four categories. An extraction rule shaped to a target's
  structure will mechanically flatter that target's topic-stability. The
  gate that governs certification was fixed in advance and I did not touch
  it; the extraction *rule* was not, and I should have held out data to
  develop it on. Next audit will.
- **My earlier comparisons weren't like-for-like.** The four lab
  configurations I benchmark against were measured in a different mode
  entirely — the model emitted machine-readable output directly, with no
  extraction layer in the path at all. Comparing that to a
  free-text-plus-extractor measurement is comparing two measurement
  architectures, not two systems.

The valence-flip result survives all three, which is why it now leads:
it's measured on whatever units the extractor produces and asks a
different question of them — given the same topic came up, did its sign
change? Coarse categories make that *more* meaningful, not less.

**What the gate did, and why it still matters.** Before any audit ran, I
pre-registered a rule: no stability claim earns certification unless the
extraction layer demonstrates sufficient self-consistency — a hard bar,
plus an extra margin for claims of instability. On the first pass, the
reason-extractor missed that margin by 0.051, and the instrument refused
to certify a gap that was sitting in the evidence file, visible to anyone
who could subtract. I rebuilt the extraction layer, re-validated it
against a second model, and re-ran. That refusal is why I trust the
decision and valence findings above — and why I'm being this careful about
the one number the rebuild also happened to inflate.

I want this instrument's failure mode to be a number I decline to stand
behind — not a confident claim I can't support. An audit tool that
certifies what its author is hunting for, without a gate that can tell it
no, is a demo. Mine said no. It also, on the gap, isn't yet saying an
unqualified yes.

## What this doesn't tell you

> **The boring box, kept deliberately intact.** Stability is not accuracy:
> a system can be perfectly consistent and perfectly wrong, and I measured
> consistency only. This is not a fairness or bias audit — that is a
> different measurement, deliberately out of scope here. The CVs are
> fictional by design; no real person's data was involved. The similarity
> numbers depend on a published synonym-grouping step, and I report the
> ungrouped numbers alongside (they are lower for every system measured).
> The 25-case sample supports the existence claims made above and no rate
> claims. The reason-side numbers are measured at the target's own
> category granularity, using an extraction rule I developed after seeing
> that target's output — a selection effect I disclose rather than
> discount, and one I'll design out with held-out data next time. And
> everything here describes one configuration of one published
> design, run by me, on stated dates, with full transcripts retained — it
> is not a claim about any commercial product, or about the tool's author,
> whose project simply happens to be a publicly runnable example of a
> category that is being deployed everywhere.

## The wider pattern

Before the real target, I pointed the same instrument at four
configurations I built myself on current frontier-lab models (three
OpenAI, one Anthropic; temperature zero; same frozen corpus). The
dissertation's asymmetry appeared on every one: reasons more stable than
advice, gaps of +0.12 to +0.29, with advice stability between 0.50 and
0.68. Directionally consistent with my 2026 result, and consistent with
the gap having *narrowed* on current models — measured differently enough
that I'd call it an evolution, not a replication. Notably, even the
*decisions* flipped occasionally at temperature zero (agreement
0.96–0.98), something my dissertation's design couldn't observe.

Two honest caveats on that comparison. Those lab configurations were
measured in a different mode — emitting machine-readable output directly,
with no extraction layer in the path — so cross-reading them against the
target's free-text measurement compares architectures as much as systems.
And on decisions, the target was less stable than three of the four but
not all: one lab configuration flipped verdicts at a comparable rate.
Verdict instability is not unique to this pipeline, which is rather the
point — it looks like a property of the design pattern, not of one
developer's project.

## Why it matters

Contestability — the right to meaningfully challenge an automated
decision — presupposes that the decision and its explanation hold still
long enough to be challenged. A rejection that would have been an
acceptance on a different run is hard to contest not because the reasoning
is opaque, but because there is no stable reasoning to contest. And advice
that changes on every query isn't guidance; it's noise wearing guidance's
clothes. Regulation increasingly demands that screening systems be
explainable. Almost none of it asks whether the explanations *stay put*.

## Kick the tyres

Every number in this piece traces to a committed transcript with a full
provenance chain — corpus hash, configuration identity, the version of
every pipeline stage, and the pinned commit of the audited code. The
instrument is a small open Python tool: one config file, one command, a
hard spending cap, and a dry-run that prices the audit before a single
call is made. Run it against your own configuration for about the price
of a coffee.

*On the target's identity: this piece deliberately describes a design
category rather than naming a small open-source project. The full
identification is pinned in the audit evidence, and the professional norm
I intend to follow is disclosure to the audited party before publication —
if you're going to measure people's work, you owe them the first read.*

**Next:** more targets. The marginal cost of asking "does your screening
tool give the same answer twice?" is now small change, the instrument has
been through one full cycle of being told no by its own gate, and so far
— across four lab configurations and one published pipeline — the answer
has never been an unqualified yes.
