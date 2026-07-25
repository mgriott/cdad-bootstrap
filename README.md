# CDAD Bootstrap

> **When context doesn't govern AI, AI governs the solution.**

The official starter kit for **Context-Driven AI Development (CDAD)** — governed
context for AI-assisted software development.

**Context is the Source of Truth.**

<sub>Works with Claude Code, Kiro, and Codex · CC BY 4.0</sub>

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

## Two files you will actually use

Everything else in this kit is machinery.

| File | What it is |
|---|---|
| **`cdad/context/stack.md`** | The map. What this system *is*, in one screen |
| **`cdad/CHANGE-REQUEST.md`** | The front door. Where you ask for anything to change |

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
cdad/CHANGE-REQUEST.md  ->  cdad/proposals/  ->  cdad/adr/ + cdad/context/stack.md
     you state intent         agent drafts           you approve and apply
     always writable          agent writable         blocked for agents
```

Write four lines in `cdad/CHANGE-REQUEST.md` — what, why, what triggered it, how
urgent. Say *"process the change request"*. The agent returns a complete
proposal: current decision, suggested change, impact, risk, alternatives, and
the exact stack map rows that change. You approve; it drafts the ADR; you apply.

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
| `scripts/cdad-check-stack.sh` | **Fails the build** when an ADR changes and the map does not |

The first three are instructions — a model can fall short. The fourth is
deterministic.

---

## Design principle

Put each concern in the plane that can enforce it.

| Plane | Mechanism | Guarantee | Context cost |
|---|---|---|---|
| Control | `permissions.deny` + PreToolUse hook | Deterministic | Zero |
| Build | CI gate in `scripts/` | Deterministic, at merge | Zero |
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
CLAUDE.md                       # imports AGENTS.md + Claude Code specifics
│
cdad/
├── CHANGE-REQUEST.md           # ← the front door: you write intent here
├── proposals/                  # agent drafts land here, awaiting your review
├── context/                    # L0 — governed, read-only for agents
│   ├── stack.md                #   ← the map: 6 views, incl. observability
│   ├── architecture.md
│   ├── solution-vision.md
│   ├── principles.md
│   ├── constraints.md          #   always in context, imported by CLAUDE.md
│   └── glossary.md
└── adr/                        # L1 — accepted decisions
│
.claude/
├── settings.json               # write protection for governed paths
├── hooks/protect-l0.py         # same block via shell too — exit 2
├── rules/                      # path-scoped: load only for matching files
└── skills/                     # cdad-propose-change, cdad-adr, cdad-audit
│
.kiro/steering/                 # Kiro mirrors of the path-scoped rules
scripts/cdad-check-stack.sh     # CI gate
docs/cdad/                      # human reference, never loaded by agents
├── METHODOLOGY.md
├── PORTABILITY.md
└── MIGRATION.md
```

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

1. Copy `INDEX.md`, `AGENTS.md`, `CLAUDE.md`, `.claude/`, `cdad/`, `scripts/`,
   and `docs/` into your project root.
2. Fill in `cdad/context/stack.md` first. It forces the decisions the other
   files describe in prose. Leave a cell empty rather than guessing — an empty
   cell is a decision not yet made, and saying so is the point.
3. Fill in the rest of `cdad/context/`. Keep `constraints.md` short: it is the
   only one loaded on every session.
4. Adjust the `paths:` globs in `.claude/rules/` to your folder layout. They
   ship with `src/`, `tests/`, `infra/`, `deploy/`.
5. Wire `scripts/cdad-check-stack.sh` into CI against your default branch.
6. Run a session, then `/context`. Only `CLAUDE.md`, `AGENTS.md`, and
   `constraints.md` should be loaded.
7. **Verify the guardrail is real:** ask the agent to edit
   `cdad/context/stack.md`. It must be *blocked*, not merely reluctant. If it
   only hesitates, the enforcement layer is not loading.

Full file map: [`INDEX.md`](INDEX.md) · Upgrading from v1:
[`docs/cdad/MIGRATION.md`](docs/cdad/MIGRATION.md)

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

Details and workarounds: [`docs/cdad/PORTABILITY.md`](docs/cdad/PORTABILITY.md)

---

## What you maintain

Only `cdad/context/` and `cdad/adr/`. Everything under `.claude/`, `.kiro/`, and
`scripts/` is CDAD runtime and rarely needs changes beyond the path globs.

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
