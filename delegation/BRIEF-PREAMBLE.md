# Brief preamble — constraints every Codex brief inherits

Referenced by briefs in `delegation/codex/`. The four existing briefs
(01–04) predate this file and repeat these constraints inline; they are
left as-is. New briefs should cite this file instead of copying it.

## Environment

- Venv: `export UV_PROJECT_ENVIRONMENT="$HOME/.venvs/goalpost"`
- Targeted tests: `uv run pytest -m codex tests/codex/<file>`
- Full suite, must stay green: `uv run pytest`
- Python 3.12. No network calls anywhere, including in tests.
- Never run a live audit command; they cost money and hit real APIs.

## No git commands

The Codex sandbox has working-tree write access but **cannot write to
`.git`** (`fatal: cannot lock ref`). Run no git commands at all — no
checkout, branch, commit, stash, or diff-with-write.

The delegator creates and checks out the working branch *before*
dispatch; the worker only edits files; the delegator reviews and commits
afterwards. A brief that instructs the worker to create its own branch
will fail at the first command (this is how task-03 failed once).

## File-touch allowlist

Every brief must state an explicit allowlist, and it is enforced on
review — a diff touching anything outside it is rejected rather than
fixed up. State what is out of scope as well as in, especially any
neighbouring function the worker might reasonably think it should tidy.

## Protocol is not delegable

Gate rules, threshold constants, metric definitions and the anchors
artifact are protocol. Briefs must instruct workers to **reuse** them
(`reporter._reportable`, `reporter.ANCHORS`, `reporter.GATE_AGREEMENT`)
and never to re-derive or restate them. A re-implementation that passes
tests is still a correctness bug: it silently forks the definition of
what the instrument certifies.

## Return format

Short summary of approach, the output tails of both test commands, and
anything the worker could not satisfy and why.
