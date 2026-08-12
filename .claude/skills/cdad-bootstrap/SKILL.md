---
name: cdad-bootstrap
description: Populate cdad/context/ for the first time in a new project. Use when the user says to set up CDAD, bootstrap CDAD, initialize CDAD, or has just cloned CDAD Bootstrap into a project and cdad/context/ still holds template placeholders. Checks the project root for an existing solution document, confirms with the Solution Designer that it is finished rather than a draft, asks for whatever it does not answer, and drafts the six context files plus a permanent SOURCE-BRIEF at the project root for review before anything is written.
---

# Bootstrap the governed context

`cdad/context/` ships as a template — angle-bracket placeholders and empty
table rows, not real answers. This skill turns those placeholders into the
project's actual context, confirmed by the Solution Designer before anything
is written.

## 0. Check the context is actually unpopulated

Read the six files in `cdad/context/`. If they already contain real content —
not placeholders like `<layered / hexagonal / ...>` or empty table rows — stop
and say so. Offer the `cdad-audit` skill instead. Do not overwrite an already
populated context.

## 1. Look for an existing solution document

Look at the project root only — not subdirectories, not the rest of the repo.
Anything there that isn't part of the kit itself (`INDEX.md`, `AGENTS.md`,
`CHANGE-REQUEST.md`, `SOURCE-BRIEF.*`, `.claude/`, `.kiro/`, `cdad/`) and isn't
ordinary project scaffolding (`package.json`, `.gitignore`, a pre-existing
`README.md`, `LICENSE`, and the like) is a candidate solution document. The
Solution Designer does not have to name it anything in particular or tell the
agent it exists — a `.md`, `.txt`, Word, or PDF file sitting there is enough.

- **Exactly one candidate:** confirm it in one line — "Using `<name>` as the
  source document?" — rather than assuming silently, then use it.
- **No candidate at the root:** ask directly whether a document exists
  elsewhere — another path, an external doc, or paste it into chat.
- **More than one candidate:** ask which one. Do not guess between them.
- **A `SOURCE-BRIEF.*` already at the root:** this project was already
  bootstrapped. Stop and offer the `cdad-audit` skill instead (same as step 0).

Do not scan subdirectories or the rest of the repository speculatively looking
for "the" document — the root check above is the only place this skill looks
without being told, same as Claude Code checking a fixed location for
`AGENTS.md` instead of searching for it. Beyond that, ask.

Wherever it comes from, once it is processed a copy becomes `SOURCE-BRIEF.*` at
the project root (step 5) — permanent, not archived away into `cdad/docs/` —
so the reasoning behind the context stays visible and traceable right where
`CHANGE-REQUEST.md` already lives, not tucked inside `cdad/`.

## 2. Confirm the document is finished — or stop

If a document exists, do not start mapping it yet. Ask the Solution Designer
directly: is this finished — the real decisions, not a draft you're still
thinking through?

- **Confirmed finished:** move to step 3.
- **Still a draft, unsure, or "sort of":** stop here. Say plainly that
  `cdad-bootstrap` needs a finished document to work from, and that patching a
  draft with interview questions is not the same thing as the Solution
  Designer actually deciding it. Suggest reviewing it with an LLM for
  inconsistencies first if they haven't already. Do not proceed to step 3.
  They come back and run this skill again once it's ready.
- **No document exists at all:** this gate doesn't apply — skip straight to
  step 3. The interview itself is how the design gets defined this time.

This is a different confirmation from step 4. This one is about whether the
Solution Designer's *own* thinking is settled. Step 4 is about whether the
*derived* context files accurately capture it. Conflating them lets an
unfinished design slip through disguised as a completed bootstrap.

## 3. Ask what is still missing

Read the confirmed document and map its content onto the six files below. For
anything it does not answer, add it to the question list — do not infer or
invent an answer from adjacent context.

Group questions by file, not by field — six short rounds, not forty
one-line questions. Only ask about what the document actually left open.

| File | Ask for |
|---|---|
| `solution-vision.md` | The problem, who it's for, what success looks like, what it deliberately will not become |
| `architecture.md` | Architectural style, modules and boundaries, integration strategy, data ownership, deployment topology, known deviations |
| `stack.md` | Language, runtime, framework, compute model, datastores, messaging, identity, secrets, IaC, CI/CD, observability, testing |
| `constraints.md` | Cloud provider, compute model, IaC, runtime/language version, datastore, comms style, data residency, compliance, budget ceilings, explicit out-of-scope |
| `principles.md` | Design principles that would actually cause a PR to be rejected, and the trade-off each one accepts |
| `glossary.md` | Domain terms whose meaning here differs from the everyday meaning |

The fewer answers exist going in, the more of this step runs. That is
expected, not a failure state — a project with a thin source document just
needs more of the conversation to happen here instead.

If an answer is genuinely not decided yet, leave it empty rather than filling
it with a plausible guess — say so explicitly. An empty cell is a decision not
yet made; a guessed one is architecture invented by the agent, which is the
exact failure CDAD exists to prevent.

## 4. Confirm before drafting

Summarize what will go into each of the six files — not the full file text,
enough to review in one pass — and get explicit confirmation from the
Solution Designer before writing anything. Silence is not confirmation.

## 5. Draft, do not write

`cdad/context/` is write-protected for you, same as for any other change.
Write the six completed files to `cdad/proposals/bootstrap/`, using the exact
target filenames (`stack.md`, `architecture.md`, `constraints.md`,
`principles.md`, `solution-vision.md`, `glossary.md`). Do not attempt to write
into `cdad/context/` yourself.

If a source document existed (step 1), also copy it — unmodified, not
paraphrased — to `cdad/proposals/bootstrap/SOURCE-BRIEF.<original-extension>`.
It gets this canonical name regardless of what the original was called — that
naming is the kit's own convention, not something the Solution Designer had to
think about upfront. If it was pasted as chat text rather than a file, save
exactly what was pasted as `cdad/proposals/bootstrap/SOURCE-BRIEF.md`. If there
was no source document at all, skip this — the bootstrap conversation itself
is the record in that case, and there is nothing to preserve. Once applied,
`SOURCE-BRIEF.*` is write-protected the same as `CHANGE-REQUEST.md` — you
create it exactly once, here, and never touch it again.

Tell the Solution Designer the commands to apply everything. Fill in the real
root filename from step 1 on the last line, if there was one — it varies, you
know it by now:

```bash
cp cdad/proposals/bootstrap/{stack,architecture,constraints,principles,solution-vision,glossary}.md cdad/context/
cp cdad/proposals/bootstrap/SOURCE-BRIEF.* .   # to the project root — skip if no source document existed
rm -r cdad/proposals/bootstrap
rm <the original root filename>   # only if it differs from SOURCE-BRIEF.* — no duplicate copies at the root
```

They run it, not you.

## After bootstrap

Point out three things:

- `stack.md`'s "Locked by" column should reference `ADR-001` for now; later
  decisions get their own ADR through the normal change flow.
- If a `SOURCE-BRIEF.*` was created, it now sits permanently at the project
  root next to `CHANGE-REQUEST.md` — the original design intent, kept for
  anyone who later asks why the context says what it says.
- Run `/context` to confirm only `.claude/CLAUDE.md`, `AGENTS.md`, and
  `constraints.md` load — the same check the README asks for after any setup.
