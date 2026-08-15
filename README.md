# CDAD Bootstrap

> **When context doesn't govern AI, AI governs the solution.**

The official starter kit for **Context-Driven AI Development (CDAD)** — governed
context for AI-assisted software development.

**Context is the Source of Truth.**

<sub>Works with Claude Code, Kiro, and Codex · CC BY 4.0</sub>

---

## Usage flow

### 1. Bootstrap the governed context

**Step 1: leave your design document at the project root, if you have one.**
Any name, any common format — `.md`, `.txt`, Word, PDF. No convention to
follow, just drop the file there. It should be finished, not a draft: idea,
goal, vision, requirements, proposed architecture, tech stack, constraints,
and development rules — ideally already reviewed and discussed with an LLM to
catch inconsistencies. Don't have one yet? Skip this step; the agent will
define the context with you through conversation instead.

**Step 2: tell your IDE agent to pull down CDAD Bootstrap and set it up** (say
*"clone CDAD Bootstrap and bootstrap the project"* — the agent runs the
`cdad-bootstrap` skill). The agent (Kiro, Codex, Cursor, Claude Code, or
whichever ADE you use):

→ clones/downloads CDAD Bootstrap into the project
→ checks whether `cdad/context/` is still template placeholders
→ checks the root for the document you left in step 1; if there's none, or
more than one, asks instead of guessing
→ if a document exists, asks you to confirm it's finished — not a draft —
before touching it; if you say it isn't, it stops and waits for you to finish
it instead of asking around the gaps
→ once confirmed (or if there was never a document to confirm), reads it and
maps it onto the six context files
→ asks you directly for whatever it still doesn't answer — the less there was
to start with, the more it asks, and that's expected
→ summarizes the result and waits for your explicit confirmation — a second,
separate confirmation from the one above: that one was about your design being
settled, this one is about whether the six files actually capture it
→ only then drafts the completed context files — plus your source document,
renamed `SOURCE-BRIEF.*`, if you had one — to `cdad/proposals/bootstrap/`, and
hands you the commands to apply them, so it ends up permanently at the
project root, not tucked away

The agent never writes `cdad/context/` itself, not even on the very first run —
`cdad-bootstrap` goes through the same propose-then-you-apply flow as every
other change to governed context. See `.claude/skills/cdad-bootstrap/SKILL.md`
for the full procedure.

From that point on, the agent reads that governed context first, before
making any implementation decision.

The idea is simple: you and the agent work out what you want to build and how
it should be, confirmed by you; then CDAD's governed context is populated from
that; finally the AI develops under that context.

---

## The problem

AI accelerates implementation. Humans govern context and architecture.

The failure mode is not bad code — agents write reasonable code. It is
**architectural drift**: a sequence of individually defensible changes that
collectively move the solution somewhere nobody decided to go.

Drift is invisible at the commit level and only visible at the architecture
level, which is exactly the level nobody reviews.

CDAD makes the architecture an explicit, protected, machine-readable asset, and
makes changing it a deliberate act instead of a side effect.

---

## Two files you will always touch

Everything else in this kit is machinery. These two live at the project root,
not inside `cdad/` — you should never have to go looking for them.

| File | What it is | When you touch it |
|---|---|---|
| **`SOURCE-BRIEF.*`** | Your original design — vision, architecture, stack, constraints, in your own words | Once, before or during setup |
| **`CHANGE-REQUEST.md`** | The front door. Where you ask for anything to change | Whenever a decision needs to change |

`cdad/context/stack.md` is the file you'll *read* the most — the one-screen
map of what this system is — but it's an output, not something you write by
hand. Approved changes reach it through `CHANGE-REQUEST.md`, never directly.

---

## The map

`cdad/context/stack.md` answers "what is this system" without opening the code.
Six views:

| # | View | Answers |
|---|---|---|
| 1 | Stack at a glance | what are we built on, and which ADR locked it |
| 2 | Component map | what talks to what, over which protocol |
| 3 | Deployment topology | where does each piece run |
| 4 | Observability | if it breaks at 3am, what do I look at |
| 5 | Dependency rules | which module may call which |
| 6 | Map change log | one row per accepted ADR |

Markdown plus Mermaid, so it renders in GitHub and any IDE — no image to
regenerate, no diagram tool to keep licensed, and **it diffs like code**. In a
pull request you see exactly what changed in the architecture.

A row in the stack table with no ADR in its "Locked by" column is itself a
finding: a decision that entered the system without passing through governance.

---

## Changing something

One entry point. You never hunt for the right file.

```
CHANGE-REQUEST.md  ->  cdad/proposals/  ->  cdad/adr/ + cdad/context/stack.md
     you state intent      agent drafts           you approve and apply
     always writable       agent writable         blocked for agents
```

Fill in the request block in `CHANGE-REQUEST.md`, at the project root — what
needs to change, why, what triggered it, scope, impact, risk, priority. Say
*"process the change request"*. The agent
returns a complete proposal: current decision, suggested change, impact, risk,
alternatives, and the exact stack map rows that change. You approve; it drafts
the ADR; you apply.

**`cdad/proposals/` is the only directory under `cdad/` an agent may write to.**
That single asymmetry is what makes the governance real rather than
aspirational: an agent that wants to change the architecture has exactly one
move available — hand you a reviewable draft.

Routine implementation work never touches this flow. If you find yourself
filing change requests for ordinary tasks, your constraints are written too
broadly. Narrow them.

---

## Keeping the map honest

Four mechanisms, weakest to strongest:

| Mechanism | What it does |
|---|---|
| `AGENTS.md` | States the rule: an ADR that doesn't declare its effect on the map is incomplete |
| Skill `cdad-adr` | Requires a before/after stack delta plus a change log row |
| Skill `cdad-audit` | Verifies each view against manifests, the real import graph, and alert rules |
| `cdad/scripts/cdad-check-stack.sh` | **Fails the build** when an ADR changes and the map does not |

The first three are instructions — a model can fall short. The fourth is
deterministic.

---

## Design principle

Put each concern in the plane that can enforce it.

| Plane | Mechanism | Guarantee | Context cost |
|---|---|---|---|
| Control | `permissions.deny` + PreToolUse hook | Deterministic | Zero |
| Build | CI gate in `cdad/scripts/` | Deterministic, at merge | Zero |
| Instruction | `AGENTS.md`, `.claude/rules/` | Probabilistic | Tokens |
| Procedural | `.claude/skills/` | On demand | Zero until invoked |

**Anything enforceable in the control plane is never written as an
instruction.** Putting "AI must not modify architecture files" into the context
window costs tokens every session and holds only probabilistically. Blocking the
write holds absolutely and costs nothing.

Instructions remain necessary for everything requiring judgment: whether a
change is architectural, whether code contradicts context, whether an
abstraction is warranted. No permission rule decides those.

The second principle follows: **the layer determines both who may edit and when
it loads.** Nothing is read at session start except the rules and the hard
constraints — roughly 85 lines, not the whole knowledge base.

---

## Structure

```
INDEX.md                        # map of every file — start here
AGENTS.md                       # portable core rules — Kiro & Codex read this natively
CHANGE-REQUEST.md               # ← the front door: you write intent here
SOURCE-BRIEF.*                  # ← your original design, created by cdad-bootstrap, never touched again
.gitignore                      # ignores __pycache__/ from the hook — merge into yours, don't overwrite it
│
cdad/
├── proposals/                  # agent drafts land here, awaiting your review
├── context/                    # L0 — governed, read-only for agents
│   ├── stack.md                #   ← the map: 6 views, incl. observability
│   ├── architecture.md
│   ├── solution-vision.md
│   ├── principles.md
│   ├── constraints.md          #   always in context, imported by .claude/CLAUDE.md
│   └── glossary.md
├── adr/                        # L1 — accepted decisions
├── scripts/cdad-check-stack.sh # CI gate
└── docs/                       # human reference, never loaded by agents
    └── DOCS.md                 # methodology, portability, migration
│
.claude/
├── CLAUDE.md                   # imports AGENTS.md + Claude Code specifics
├── settings.json               # write protection for governed paths
├── hooks/protect-l0.py         # same block via shell too — exit 2
├── rules/                      # path-scoped: load only for matching files
└── skills/                     # cdad-bootstrap, cdad-propose-change, cdad-adr, cdad-audit
│
.kiro/steering/                 # Kiro mirrors of the path-scoped rules
```

### Why some files stay at the root

Everything that is not a tool's fixed entry point, and not one of the two
files you touch yourself, lives under `cdad/`. `.claude/`, `.kiro/`,
`CHANGE-REQUEST.md`, and `SOURCE-BRIEF.*` are the exceptions, for two
different reasons.

`.claude/` and `.kiro/` staying at the root is not a style choice — it is how
these tools discover their configuration.

Claude Code loads `./CLAUDE.md` or `./.claude/CLAUDE.md` (plus ancestor
directories above the cwd) at session start. It does not walk into arbitrary
subdirectories looking for one. Nest `.claude/` a level deeper — say, inside
`cdad/.claude/` — and Claude Code simply never loads it. There is no error, no
warning: the rules and skills are silently absent from every session.

Kiro works the same way with `.kiro/steering/`: it is discovered at a fixed
location relative to the project root, not searched for. Move it under `cdad/`
and Kiro stops finding it, again without telling you.

`AGENTS.md` stays at the root for the identical reason — it is the file Kiro
and Codex read natively by convention. Only content that no tool discovers by
fixed path — docs, the CI script, `CLAUDE.md` itself once redirected through
`.claude/CLAUDE.md` — is free to move into `cdad/`.

`CHANGE-REQUEST.md` and `SOURCE-BRIEF.*` stay at the root for a different
reason: not tool discovery, yours. No tool reads either one automatically, so
nothing would break if they lived under `cdad/`. But they are the only two
files the Solution Designer ever needs to find — one on day one, one whenever
a decision needs to change — and burying them next to two dozen machinery
files defeats the point of having a single, obvious front door. Both stay
exactly as protected as any file in `cdad/context/` or `cdad/adr/` — the
permission rules and the hook target them by name, not by location.

---

## Context layers

| Layer | Contents | Policy | Loads |
|---|---|---|---|
| L0 | `cdad/context/` | propose only | on demand (except `constraints.md`) |
| L1 | `cdad/adr/` | propose with review | on demand |
| L2 | `docs/` | editable with review | never |
| L3 | `src/`, `tests/`, pipelines, IaC | editable | n/a |

---

## Getting started

1. Copy `INDEX.md`, `AGENTS.md`, `CHANGE-REQUEST.md`, `.claude/` (includes
   `.claude/CLAUDE.md`), `cdad/` (includes `cdad/docs/` and `cdad/scripts/`),
   and `.kiro/` if you use Kiro into your project root. `CHANGE-REQUEST.md`
   belongs at the root exactly as shipped — do not move it under `cdad/`, and
   do not recreate `CLAUDE.md`, `docs/`, or `scripts/` as separate top-level
   folders either; those live inside `.claude/` and `cdad/` now. Merge the
   kit's `.gitignore` into your own if you already have one — it just ignores
   the `__pycache__/` the protection hook generates the first time it runs.
2. Run the `cdad-bootstrap` skill (say *"bootstrap CDAD"* or *"set up CDAD"*)
   instead of filling `cdad/context/` by hand. It checks whether you already
   have a solution document, asks you directly for whatever it doesn't answer,
   confirms the result with you, and only then drafts the six files for you to
   apply. Keep `constraints.md` short either way: it is the only one loaded on
   every session.
3. If you'd rather fill it in yourself: start with `cdad/context/stack.md`, it
   forces the decisions the other files describe in prose. Leave a cell empty
   rather than guessing — an empty cell is a decision not yet made, and saying
   so is the point.
4. Adjust the `paths:` globs in `.claude/rules/` to your folder layout. They
   ship with `src/`, `tests/`, `infra/`, `deploy/`.
5. Wire `cdad/scripts/cdad-check-stack.sh` into CI against your default branch.
6. Run a session, then `/context`. Only `.claude/CLAUDE.md`, `AGENTS.md`, and
   `constraints.md` should be loaded.
7. **Verify the guardrail is real:** ask the agent to edit
   `cdad/context/stack.md`. It must be *blocked*, not merely reluctant. If it
   only hesitates, the enforcement layer is not loading.

Full file map: [`INDEX.md`](INDEX.md) · Upgrading from v1:
[`cdad/docs/DOCS.md`](cdad/docs/DOCS.md#migrating-from-cdad-v1)

---

## Tool support

| | Claude Code | Kiro | Codex |
|---|---|---|---|
| Portable core rules | via import | native | native |
| Conditional loading | `paths:` | `inclusion: fileMatch` | nested `AGENTS.md` |
| On-demand procedures | Skills | `inclusion: manual` | prompt |
| Deterministic write block | yes | filesystem or CI | config globs |
| Governed context + CI gate | yes | yes | yes |

Claude Code runs everything. Kiro runs everything except the declarative write
block — fall back to `chmod -R a-w cdad/context` or the CI gate. Codex keeps the
write block but loses fine-grained conditional loading.

Details and workarounds: [`cdad/docs/DOCS.md`](cdad/docs/DOCS.md#portability-claude-code-kiro-codex)

### Delete what you don't use

The kit ships with adapters for all three tools. Keeping adapters nobody reads
is the same duplication defect CDAD v2 was built to remove — the mirrors drift
apart and you stop trusting either one. **Prune on day one.**

| You use | Keep | Delete |
|---|---|---|
| Claude Code only | `AGENTS.md`, `.claude/` (incl. `.claude/CLAUDE.md`) | `.kiro/` |
| Kiro only | `AGENTS.md`, `.kiro/` | `.claude/` |
| Codex only | `AGENTS.md` | `.claude/`, `.kiro/` |
| More than one | everything | nothing |

```bash
# Claude Code only
rm -rf .kiro

# Kiro only
rm -rf .claude

# Codex only
rm -rf .claude .kiro
```

**Never delete `AGENTS.md`.** It holds the core rules. Claude Code imports it
from `.claude/CLAUDE.md`; Kiro and Codex read it natively.

Two consequences worth knowing before you prune:

**Deleting `.claude/` removes the enforcement layer.** `settings.json` and
`hooks/protect-l0.py` are what make L0 protection deterministic rather than
advisory. On Kiro or Codex you are falling back to `chmod -R a-w cdad/context`
plus the CI gate — weaker, but still real. Do not skip both.

**On Codex, add nested instruction files.** Codex has no path-scoped rules, so
recreate the effect by placing scoped `AGENTS.md` files near the code they
govern, porting the content from `.claude/rules/` before you delete it:

```
AGENTS.md          # core
src/AGENTS.md      # implementation rules
infra/AGENTS.md    # infrastructure rules
```

Also note that Kiro loads `AGENTS.md` in full on every session — it has no
inclusion modes. Your core stays small either way, but the startup saving is
smaller there than on Claude Code.

---

## What you maintain

`cdad/context/` and `cdad/adr/` — applied by you, never written by an agent.
`CHANGE-REQUEST.md` is yours to fill in whenever something needs to change.
`SOURCE-BRIEF.*` is written once, by `cdad-bootstrap`, then left alone.
Everything under `.claude/`, `.kiro/`, and `cdad/scripts/` is CDAD runtime and
rarely needs changes beyond the path globs.

---

## Requirements

Claude Code, Kiro, or Codex. The protection hook needs `python3`, present by
default on Linux and macOS. The CI gate needs `git` and `bash`.

---

## Evolution

CDAD is an evolving methodology focused on the governance of context in
AI-assisted development. Future work may extend it across software solutions,
cloud and infrastructure, agentic systems, documentation, and knowledge
governance — while preserving the core principle:

> **Context is the Source of Truth.**

Related: [CDAD Framework](https://github.com/mgriott/context-driven-ai-development)
— methodology, whitepapers, principles, and governance model.

---

## License

Creative Commons Attribution 4.0 International (CC BY 4.0).

You are free to share, adapt, and build upon this work, including commercially,
provided appropriate attribution is given.

<https://creativecommons.org/licenses/by/4.0/>

Copyright © 2026 Moisés Griott
