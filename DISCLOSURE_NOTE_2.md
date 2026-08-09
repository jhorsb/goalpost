# Draft disclosure note — target #2's author (D-024 norm; D-058 calibration)

*Draft — NOT SENT.*

**Channel problem, and the two-step plan.** Unlike author #1, this author
publishes no email anywhere (profile email null; no README contact;
commits via GitHub noreply). A public GitHub issue containing the
findings would de-anonymise the audit before he can respond — inverting
the norm. Plan: **step 1**, the author posts the content-free contact
request below as a GitHub issue on the repo (reveals only that someone
wants to share research privately — nothing about findings); **step 2**,
when he replies with a channel, the full note below goes to it verbatim.
If no response by ~19 August, the anonymous-by-default path applies
unchanged — the attempt and its date are the record.

**Recipient:** Pakawat Kraisintu (GitHub: Pakawat-Dev), author of the
MIT-licensed Candidate_Screening_Agent. Bio: "enjoys coding as a hobby" —
tone calibrated accordingly.

---

## Step 1 — content-free contact request (public GitHub issue)

> **Title:** Independent research involving this repo — may I share it
> with you privately before publishing?
>
> Hi Pakawat — I'm an AI-governance researcher and I've done some
> independent research that involves this repository. I'd like to share
> the full details with you privately before anything is published, as a
> courtesy — you'd get the first read and a chance to respond. Could you
> post or email me a way to reach you? I'm at
> jamie.horsburgh777@outlook.com and the eventual write-up venue is
> https://jamiehorsburgh.substack.com. Thanks for publishing your work
> openly.

## Step 2 — the full note (private channel, once he provides one)

Subject: Heads-up before I publish: an independent stability audit of
your candidate-screening project

Hi Pakawat,

I'm Jamie Horsburgh, an AI-governance researcher (this is personal
research, done in my own time and not for any employer). The write-up
will appear at https://jamiehorsburgh.substack.com. I build an
open-source audit instrument that measures whether LLM screening systems
give the same answer twice, and your Candidate_Screening_Agent was its
second real-world target — because it's one of the few complete,
runnable, published examples of the LangGraph screening pattern. That's a
compliment to the openness of your work, and I want you to see the
results before anyone else does.

What I did: I ran your pipeline's three LLM stages entirely on my own
API keys, at the pinned commit 707e6ab, mirroring your prompts and data
flow exactly (your prompts are vendored in my repo under your MIT licence,
with attribution). 25 fictional CVs, 5 identical runs each, at your
code's own per-stage settings. Three divergences, disclosed in the audit:
plain-text CVs in place of the OCR stage, direct API calls in place of
the LangGraph harness, and — you'd want to know this — the model your
code pins (claude-3-5-sonnet-20241022) has been retired by Anthropic, so
nobody can run your project as shipped any more; I substituted the
current same-class model (claude-sonnet-4-5) and disclosed it. Both
tools I've audited so far pin now-retired models — this is an industry
pattern, not a criticism of you.

What I found, in one paragraph: on identical inputs, the verdict changed
for 6 of 25 candidates; the improvement advice repeats a bit more than
half the time (0.556 on a 0–1 overlap measure); and 7 of 25 candidates
consistently received no clear verdict ("Maybe") — with every verdict
flip occurring in that group. I want to flag something genuinely
positive alongside: yours is the only system I've measured with an
explicit "Maybe" tier, and it uses it consistently — on genuinely
borderline candidates, declining to decide is arguably the most honest
behaviour I've observed from any screening tool, and my write-up says
so. I'd also note that every configuration I've measured, on six model
families, flips some verdicts on identical inputs — this is not unique
to your design.

In the write-up I describe the project as "a published 3-stage screening
pipeline" without naming it or you. I'm happy to (a) name the project
with a link, (b) keep it anonymous, or (c) hold publication for a
reasonable window while you look at the full evidence. If you think I've
made an error, I want to know before I publish, and I'll print your
response alongside if you'd like.

The evidence is yours on request: reply and I'll send the complete
bundle within a day — every transcript, config, metric file and the
audit instrument itself, enough to re-run everything yourself.

Timeline, so this isn't an open loop: I'm planning to publish on or
around 22 August 2026. If I don't hear from you I'll go ahead with the
anonymous version (option b), and the offer to correct or respond stays
open after publication.

No action is needed from you; this is a courtesy note, not a demand.
Thanks for building in the open — audits like this are only possible
against people willing to show their code.

Best,
Jamie Horsburgh
https://jamiehorsburgh.substack.com

---

**Pre-decided (asked-to-be-named case, per D-030):** attribution yes,
headlining no — name and link in a footnote plus the evidence appendix;
prose keeps the category description.
