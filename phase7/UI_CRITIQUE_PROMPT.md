# Prompt — adversarial UI critique + rebuild (for GPT 5.6 Sol Ultra)

Copy everything below the line. Attach or paste the HTML file
(`goalpost-explainer.html`) alongside it.

---

You are a senior product designer with a second specialism in science
communication. You are being hired to tear apart a page an AI wrote, and
then rebuild it properly. Be genuinely adversarial: I am not looking for
validation, and "this is quite good already" is a failed response.

## The artifact

A single-page explainer for **Goalpost**, an audit instrument that measures
whether AI hiring tools give the same answer twice. The HTML is attached.
It was written by Claude, in one pass, without user testing.

## Context you need

**What the tool does.** It runs the same fictional CV through a real,
published AI screening tool 25 times over (5 CVs × 5 identical runs, at the
tool's own settings), then measures whether three things stay the same
across identical runs: the **decision** (hire / don't), the **reasons**
given, and the **advice** on what the candidate should change. Findings so
far: verdicts flip on 3–5 of every 25 candidates; advice repeats less than
half the time; explanations keep the same topics while flipping whether
each topic counts *for* or *against* the candidate.

**The one hard concept.** Because the audited tools answer in prose, a
second AI model ("the reader") converts each reply into comparable lists.
That raises the obvious objection: *what if the reader is the unstable
one?* So there is a **gate**: the reader must re-read the same replies and
agree with itself at ≥ 0.90, or the instrument refuses to publish the
numbers ("withheld"). The gate has refused three times, including on the
project's own headline finding. **That refusal is the project's proudest
feature and the hardest thing to convey.** If a reader finishes the page
without understanding why an audit tool that says "no" to its own author is
more trustworthy than one that always produces a number, the page has
failed at its main job.

**Audience, in priority order.**
1. A curious non-technical reader — journalist, policy person, HR lead.
   No statistics background. Will not know what a Jaccard index is and must
   never need to.
2. A sceptical technical peer looking for methodological holes.
3. The author, using it to explain the project out loud to others.

**Constraint that shapes everything:** most readers get ~40 seconds. The
page must work if they read only the top third, and reward them if they
don't stop.

**Prior failure worth knowing.** An earlier dashboard on the predecessor
project ("Drift Arcade") failed for being *not intuitive enough* — it
exposed configuration controls, run selectors and dense metric panels, and
assumed the viewer already understood the measurement. Do not repeat that.
Any interactivity must *teach*, never *configure*.

## Task 1 — Name the AI tells

AI-generated frontends converge on a recognisable house style. Go through
this page and list, concretely and with line references, every place it
exhibits one. Consider at least: default palette and font choices that
signal "an AI made this"; decorative structure that encodes nothing (
numbered eyebrows, icon bullets, gratuitous cards); uniform section rhythm
where every block is the same size and shape; hero conventions; animation
that flatters rather than explains; copy patterns (triads, em-dash
cadence, "isn't X — it's Y" constructions, portentous one-line paragraphs);
and over-explanation where a visual would carry the load alone.

For each: quote it, say why it reads as machine-made, and give the specific
fix. Be concrete — "the colour palette feels generic" is useless; "the
teal-on-cream with a serif body is the default editorial-explainer look;
here is what the subject argues for instead, and why" is useful.

## Task 2 — Find where a non-expert falls off

Walk the page as **persona 1** — a policy researcher with no ML background,
40 seconds, on a phone. Identify every point where they would stall,
misread, or bounce. Pay particular attention to:

- **The gate.** Is the dot chart legible without the legend? Does "the
  reader must agree with itself" land, or does it require re-reading? Would
  a non-expert grasp *why* self-agreement licenses a claim about a
  different system? This is the make-or-break concept.
- **Certified vs withheld.** Withheld numbers are shown struck-through and
  grey. Does that read as "we're hiding something", "this is broken", or
  the intended "we measured it and won't stand behind it"?
- **Number literacy.** 0.448, 0.983, +0.106 — which of these actually mean
  anything to persona 1, and which are decoration they'll skim? Propose
  concrete reframings (natural frequencies, comparisons, small multiples)
  for the ones that don't earn their place.
- **Vocabulary.** Flag every term assuming knowledge the audience lacks
  ("cluster-level", "self-agreement", "lens", "temperature", "corpus").
- **The scoreboard's four cards.** Can a reader tell *why* there are four,
  and what each is for, without reading every line? What is the control
  for, and does the page make its logic (same model, no pipeline →
  therefore the difference is the design) visible at a glance?

## Task 3 — Rebuild it

Produce a complete replacement HTML file implementing your critique. Before
the code, give a short design plan: palette (4–6 named hex values), type
pairing and scale, layout concept, and the single idea the page is built
around. Then state explicitly what you changed and why — I want the
reasoning, not just the artefact.

**Requirements:**

- **Self-contained.** Strict CSP: no external stylesheets, scripts, fonts,
  or images. Inline all CSS/JS; embed any asset as a data URI. A linked
  webfont will silently fall back — use system/local stacks or an inlined
  @font-face.
- **No document wrapper.** The file is injected into an existing
  `<!doctype html><head>…</head><body>` skeleton. Emit page content only —
  no `<!DOCTYPE>`, `<html>`, `<head>` or `<body>` tags. A `<title>` and a
  `<style>` block are fine.
- **Both themes, token-level.** Define the palette as custom properties on
  `:root`; redefine the tokens under `@media (prefers-color-scheme: dark)`
  **and** under `:root[data-theme="dark"]` / `:root[data-theme="light"]`,
  since the viewer's toggle stamps `data-theme` and must win in both
  directions. Style components through tokens only.
- **Mobile-first.** Wide content (tables, charts) scrolls inside its own
  `overflow-x: auto` container; the body never scrolls sideways. Respect
  `prefers-reduced-motion`. Visible keyboard focus states.
- **Every number must survive unchanged.** You may reframe presentation
  (natural frequencies, comparisons, visual encodings) but may not alter,
  round differently, or invent a figure. If you think a number is
  misleading as presented, say so in the critique rather than editing it.
- **Withheld stays visibly withheld.** Improve how it reads; never let a
  withheld number appear as though it were certified. This is an integrity
  constraint, not a stylistic one.
- **Both audited tools stay anonymous.** They are described by category
  only, deliberately — one author has been sent a courtesy disclosure and
  the response window is still open. Do not add identifying detail even if
  you can infer it.

## What good looks like

A page where a policy researcher, in 40 seconds, comes away able to say:
*"An AI hiring tool changed its verdict on the same CV. Someone built an
instrument to measure that, and the instrument is honest enough to refuse
to publish numbers it can't stand behind — including its author's favourite
finding."*

If your rebuild does not make that second clause land, it has not
succeeded, however handsome it looks.
