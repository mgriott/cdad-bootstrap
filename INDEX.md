# CDAD Index

Every file in this kit: what it is, who owns it, and when it enters an agent's
context. If you read one file to orient yourself, read this one.

---

## Start here

| I want to... | Go to |
|---|---|
| Change the stack, architecture, or any directive | `cdad/CHANGE-REQUEST.md` |
| See what this system is, in one screen | `cdad/context/stack.md` |
| Understand why CDAD works this way | `cdad/docs/METHODOLOGY.md` |
| Set this up in my project | `README.md` |
| Run it on Kiro or Codex | `cdad/docs/PORTABILITY.md` |
| Delete the adapters I don't use | `README.md` → *Delete what you don't use* |

---

## Governed context — you own it, agents cannot write it

| File | Layer | Contains | Loads |
|---|---|---|---|
| `cdad/CHANGE-REQUEST.md` | — | Your standing request desk. The only input door | never |
| `cdad/context/stack.md` | L0 | **The map**: stack table, components, topology, observability, dependency rules, change log | on demand |
| `cdad/context/architecture.md` | L0 | Architecture in prose, module responsibilities | on demand |
| `cdad/context/constraints.md` | L0 | Hard limits. Kept short because it is always loaded | **always** |
| `cdad/context/principles.md` | L0 | Design principles in force | on demand |
| `cdad/context/solution-vision.md` | L0 | Purpose and non-goals | on demand |
| `cdad/context/glossary.md` | L0 | Terms whose meaning here differs from the usual | on demand |
| `cdad/adr/ADR-*.md` | L1 | Accepted decisions and their rationale | on demand |
| `cdad/adr/ADR-TEMPLATE.md` | L1 | Blank ADR | never |

## Staging — agents write here

| File | Contains | Loads |
|---|---|---|
| `cdad/proposals/` | Agent drafts awaiting your review. Delete when resolved | never |

## Instructions — how agents behave

| File | Contains | Loads |
|---|---|---|
| `AGENTS.md` | Portable core rules. Read natively by Kiro and Codex | **always** |
| `.claude/CLAUDE.md` | Imports `AGENTS.md`, adds skill routing | **always** |
| `.claude/rules/implementation.md` | Rules for `src/`, `tests/`, `lib/` | on matching files |
| `.claude/rules/infrastructure.md` | Rules for `infra/`, `deploy/`, CI | on matching files |
| `.kiro/steering/cdad-implementation.md` | Kiro mirror of the above | on matching files |
| `.kiro/steering/cdad-infrastructure.md` | Kiro mirror of the above | on matching files |

## Procedures — load only when invoked

| File | Invoked when |
|---|---|
| `.claude/skills/cdad-propose-change/SKILL.md` | processing a change request, or a change is needed |
| `.claude/skills/cdad-adr/SKILL.md` | a change was approved and needs recording |
| `.claude/skills/cdad-audit/SKILL.md` | checking whether context still matches the code |

## Enforcement — costs zero context

| File | Does |
|---|---|
| `.claude/settings.json` | Denies writes to governed paths |
| `.claude/hooks/protect-l0.py` | Blocks the same paths via shell too. Exit 2 |
| `cdad/scripts/cdad-check-stack.sh` | CI gate: an ADR without a map update fails the build |

## Human documentation — never loaded by any agent

| File | Contains |
|---|---|
| `INDEX.md` | This file |
| `README.md` | What CDAD is, setup, tool support |
| `cdad/docs/METHODOLOGY.md` | Governance model, layers, enforcement planes |
| `cdad/docs/PORTABILITY.md` | Claude Code vs Kiro vs Codex |
| `cdad/docs/MIGRATION.md` | Upgrading from CDAD v1 |

---

## The one flow that matters

```
cdad/CHANGE-REQUEST.md  ->  cdad/proposals/  ->  cdad/adr/ + cdad/context/stack.md
     you state intent         agent drafts           you approve and apply
     always writable          agent writable         blocked for agents
```

Everything else in this kit exists to make that flow cheap to run and hard to
skip.

---

## What loads on every single session

Only these. Everything else is on demand or never.

- `.claude/CLAUDE.md` (or `AGENTS.md` on Kiro and Codex)
- `AGENTS.md`
- `cdad/context/constraints.md`

If `/context` shows anything else from `cdad/`, something is importing more than
it should.
