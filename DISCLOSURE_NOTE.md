# Draft disclosure note to the upstream author (D-024 norm)

*Draft — not sent. Channel: GitHub issue on the audited repo (public) or
email if listed. Author review required before anything is sent.*

**Before sending, fill `<<SUBSTACK_URL>>`.** Publication target date in the
note is **12 August 2026**; if that slips, the note's stated date must move
with it — a missed self-imposed deadline is worse than a later one.

**Pre-decided answer if they reply asking to be named (D-030):** the prose
still describes the design category; the name and link go in a footnote and
the evidence appendix. The argument is about a pattern deployed everywhere,
and a named target in the body invites readers to make it about one
developer. Say yes to attribution, not to headlining them.

---

Subject: Heads-up before I publish: an independent stability audit of
your resume-screening project

Hi — I'm Jamie Horsburgh, an AI-governance researcher (this is personal
research, done in my own time and not for any employer). The write-up will
appear at <<SUBSTACK_URL>>. I built an open-source audit instrument that measures
whether LLM screening systems give the same answer twice, and I chose your
resume-screening project as its first real-world target — because it's one
of the few complete, runnable, published examples of the multi-agent
screening pattern. That's a compliment to the openness of your work, not a
criticism of it, and I want you to see the results before anyone else
does.

What I did: I ran your pipeline entirely on my own API keys, at a pinned
commit, exactly as your code wires it (25 fictional CVs × 5 identical
runs, at your default settings). No hosted service of yours was touched;
no real person's data was involved. Your prompts were fetched at runtime
from your repo and never redistributed.

What I found, in one paragraph: on identical inputs, the pipeline's
accept/reject verdict changed on 3 of 25 candidates; its improvement
advice repeats less than half the time (0.448 on a 0–1 similarity
measure); and while it discusses the same four rubric headings almost
perfectly consistently, whether a given heading counts *for or against*
a candidate flips in roughly a third to a half of repeat comparisons. A
control run (same model, plain single prompt) shows the verdict flipping
comes from the underlying model, not your design — but the
explanation/advice pattern is specific to the chained design. One more
thing you'd probably want to know: the model your code pins
(llama3-70b-8192) has been retired by every provider that served it, so
the project no longer runs as shipped; I substituted a current open-weights
model and disclosed that in the audit.

In the write-up I describe the project as "a published open-source
screening pipeline" without naming it or you. I'm happy to (a) name the
project with a link, (b) keep it anonymous, or (c) hold publication for a
reasonable window while you look at the full evidence. If you think I've
made an error, I want to know before I publish, and I'll print your
response alongside if you'd like.

The evidence is yours on request: reply and I'll send the complete bundle
within a day — every transcript, config, metric file and the audit
instrument itself, enough to re-run the whole thing yourself.

Timeline, so this isn't an open loop: I'm planning to publish on or around
12 August 2026. If I don't hear from you I'll go ahead with the anonymous
version (option b), and the offer to correct or respond stays open after
publication.

No action is needed from you; this is a courtesy note, not a demand.
Thanks for publishing your work openly — audits like this are only
possible against people willing to show their code.
