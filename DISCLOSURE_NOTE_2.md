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
Publication proceeded 9 August (author decision, D-063) with anonymity
preserved; the posted request and its date are the record of contact
effort, and the full note goes to any channel he ever provides.

**Recipient:** Pakawat Kraisintu (GitHub: Pakawat-Dev), author of the
MIT-licensed Candidate_Screening_Agent. Bio: "enjoys coding as a hobby" —
tone calibrated accordingly.

---

## Step 1 — content-free contact request (public GitHub issue)

> **Title:** Independent research involving this repo — full details
> available to you privately
>
> Hi Pakawat — I'm an AI-governance researcher. I've published an
> independent, anonymised behavioural analysis that involves this
> repository (it is not named or linked anywhere in the publication).
> I'd like to share the complete details and evidence with you privately
> — you have a standing offer to correct anything you believe is in
> error, and any response you'd like made will be printed alongside.
> Could you post or email me a way to reach you? I'm at
> jamie.horsburgh777@outlook.com; the write-up venue is
> https://jamiehorsburgh.substack.com. Thanks for publishing your work
> openly.

## Step 2 — the full note (private channel, once he provides one)

Subject: An independent stability audit of your candidate-screening
project — full details and evidence for you

Hi Pakawat,

I'm Jamie Horsburgh, an AI-governance researcher (this is personal
research, done in my own time and not for any employer). The write-up
will appear at https://jamiehorsburgh.substack.com. I build an
open-source audit instrument that measures whether LLM screening systems
give the same answer twice, and your Candidate_Screening_Agent was its
second real-world target — because it's one of the few complete,
runnable, published examples of the LangGraph screening pattern. That's a
compliment to the openness of your work. An anonymised analysis is now
published; this note gives you the full detail directly.

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
half the time (0.556 on a 0–1 overlap measure); and for 6 of 25 candidates the
most common outcome was no clear verdict ("Maybe"), one unanimously so —
with five of the six verdict flips occurring among them. I want to flag something genuinely
positive alongside: yours is the only system I've measured with an
explicit "Maybe" tier, and it uses it consistently — on genuinely
borderline candidates, declining to decide is arguably the most honest
behaviour I've observed from any screening tool, and my write-up says
so. I'd also note that every configuration I've measured, on six model
families, flips some verdicts on identical inputs — this is not unique
to your design.

The write-up describes the project as "a published 3-stage screening
pipeline" without naming it or you, and that anonymity stands unless you
prefer attribution (in which case: name and link, gladly). If you think
I've made an error anywhere, I want to know — corrections will be made
prominently, and I'll print any response of yours alongside if you'd
like.

The evidence is yours on request: reply and I'll send the complete
bundle within a day — every transcript, config, metric file and the
audit instrument itself, enough to re-run everything yourself.

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
