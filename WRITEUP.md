# I ran an AI hiring tool five times on the same CV. It changed its mind.

*Draft v4 — from the WRITEUP_TEMPLATE skeleton; every number traces to a
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
this summer turning it into **Goalpost**: an open instrument for auditing
decision, reason and recourse stability in LLM-mediated screening
configurations — any configuration its operator controls. It measures one
property, repeat-consistency, and produces two things: a machine-readable
evidence file, and a one-page report a non-specialist can act on.

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

**Where the calls went, and why it matters.** Every measurement here went
to a single named provider endpoint, fixed in advance and recorded in the
audit config — never through a routing layer that picks a backend on your
behalf. That sounds like fussiness. It isn't. The same model served by
different backends can disagree substantially: one analysis found the
choice of backend alone shifting benchmark scores by [up to 16.6
percentage points](https://www.lesswrong.com/posts/KsyoSAyBRXtwzSugg/not-pinning-your-openrouter-provider-might-invalidate-your),
and a peer-reviewed study of five APIs configured for determinism still
measured [accuracy swings of up to 15% between
runs](https://aclanthology.org/2025.eval4nlp-1.12/). The mechanism is
mundane — reduction kernels split their work differently at different
batch sizes, so identical prompts drift with server load.

For a leaderboard, that's a footnote. For this audit it would be fatal,
because the quantity I am measuring *is* variation between identical runs
— precisely what a router silently manufactures. An auditor working
through one cannot say whether the instability belongs to the system or to
the serving layer, and the audited party has a complete rebuttal: *you
didn't measure us, you measured your router.* So: where a model's own lab
serves it, I used the lab; where it doesn't — open-weights models — I
pinned one named host and disclosed which. I'd suggest this is a
requirement, not a nicety, for any audit whose findings are meant to
attach to a named system.

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
the tool itself. An independent stability check on a deployed screening
pipeline costs less than a Freddo. (Cumulatively — every false
start, quota wall, the extractor rebuild and the control run described
below — the whole investigation ran to about five dollars of paid API
spend, plus free-tier usage on an open-weights host.)

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
with this instrument, including four frontier-lab configurations and a
bare-model control on the pipeline's own model. Because
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
against the candidate*, and it flips in **between a third and a half** of
paired comparisons (0.378–0.508, depending on which of two independently
certified extraction lenses does the reading). Your
experience can be the reason you're recommended on one run and the reason
you're not on the next. The explanation looks stable at the level of what
it mentions, and is unstable in what it asserts.

That is my dissertation's thesis in a sharper form than my dissertation
managed to state it — and, unlike the number beside it, it never needed a
control run to rescue it.

**About the gap.** Reasons measured 0.983 and advice 0.448 — a stability
gap of 0.535, wider than anything I have measured on a lab configuration.
An earlier draft of this piece reported that number and then spent three
paragraphs explaining why I couldn't fully stand behind it. What changed is
the control described in the next section: measured the same way, with the
same model and the same lens, a plain one-prompt screener's gap is
**0.106**. Whatever share of 0.535 is measurement artifact applies to both
sides equally — so the *difference*, roughly 0.43, is the part attributable
to the pipeline's design.

One caveat survives, and I'm keeping it in the open: the two sides aren't
measured at the same resolution. Reasons are counted at the level of four
fixed rubric headings, advice at the level of individual recommendations,
and coarse buckets match each other more easily than fine-grained items do.
That inflates the absolute gap on both sides. It does not explain the
distance between them.

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
certifies whatever its author is hunting for, with no gate that can tell it
no, is a demo. Mine said no twice: once to the finding I was chasing, and
once, later, to an extraction lens I had grown attached to.

## The control, and what it rules out

An audit of one system tells you about one system. To say anything about a
*design*, you have to know what the same model does without it. So I ran
the pipeline's own model — same twenty-five CVs, same settings, same
certified measurement lens — behind a plain one-prompt screener instead of
the four-agent chain. Three things then separate cleanly, and the
separation is the most useful thing in this piece.

**What belongs to the model, not the pipeline.** Verdict flipping. The bare
model changed its accept/reject answer on four of twenty-five candidates;
the full pipeline on three. The chain neither causes this nor cures it, and
it would be unfair to the developer to imply otherwise. Every configuration
I have measured — six now, across three model families — flips at least
some verdicts. If you are running an LLM as a screening gate, the odds are
this is your problem too, not this developer's.

**What belongs to the design.** The gap, and the valence flipping. The
chain's fixed rubric lifts topic-stability from 0.61 to 0.99 while leaving
advice no more stable than the bare model's (0.456 against 0.507 — if
anything slightly worse) — it
manufactures consistent-looking *explanations* without manufacturing
consistent *guidance*. And it makes the meaning-flipping worse, not better:
0.378 against the bare model's 0.249. The architecture that was presumably
added to make the system more rigorous made its explanations more
authoritative-looking and no more stable.

**What belongs to my instrument, and had to be caught.** The extraction
rule that reads reasons out of free text was written after I'd seen this
pipeline's four-heading structure — a selection effect that would flatter
exactly the number it produced. So I pointed it at the bare model's
unscaffolded prose, where that structure doesn't exist. Its self-consistency
fell below the pre-registered bar and the instrument withheld the numbers.
The worry was real, the gate caught it, and a second independently
certified lens then reproduced the target's gap almost exactly (0.537
against 0.535) — so the finding survives, but the rule doesn't get to
travel unexamined. Extraction rules get developed on held-out data from
here on.

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
> that target's output — a selection effect I tested rather than merely
> disclosed (see the control), and one I'll design out with held-out data
> next time. And
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

Set against the control above, the reading is that verdict instability is
a property of this generation of models, while the explanation/advice
pattern is a property of the chained design — which is why the piece is
about a pattern rather than a project.

## Why it matters

Contestability — the right to meaningfully challenge an automated
decision — presupposes that the decision and its explanation hold still
long enough to be challenged. A rejection that would have been an
acceptance on a different run is hard to contest not because the reasoning
is opaque, but because there is no stable reasoning to contest. And advice
that changes on every query isn't guidance; it's noise wearing guidance's
clothes. Regulation increasingly demands that automated screening give
reasons and a route to challenge. Almost none of it asks whether either
survives the same case being run twice.

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
