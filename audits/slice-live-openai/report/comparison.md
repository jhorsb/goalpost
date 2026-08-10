# Goalpost comparison — slice-live-openai

> **Cross-mode comparison.** These systems were measured under different elicitation modes (structured vs freeform); their numbers are not strictly like-for-like. Rows are labelled.

Ranked by recourse stability (cluster level). Rows sharing a tie-band have overlapping spreads: treat them as not meaningfully ordered by this display (no statistical test is performed).

| band | SUT | mode | recourse stability | IQR | cases |
|---|---|---|---|---|---|
| 1 | gpt4omini-screener-structured | structured | 0.58 | [0.58, 0.58] | 1 |

## Unranked

These systems did not clear the eligibility floors and are listed without a rank:

- **gpt4omini-screener-freeform** (freeform): extractor self-agreement fails the pre-registered gate at the reported level (recourse 0.87)

*audit schema 0.1.0 · metrics 0.2.0 · anchors-1.1.0 · taxonomy 1.0.0+1dfd20707ff9 · report 0.2.0*