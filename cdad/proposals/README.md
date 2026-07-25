# Proposals — staging area

Agent-writable. This is the only place under `cdad/` an agent may create files.

A proposal here is a **draft, not a decision**. Nothing in this directory
governs anything. It exists so the agent can hand you a complete, reviewable
artifact without ever touching `cdad/context/` or `cdad/adr/`.

## Flow

```
cdad/CHANGE-REQUEST.md   →   cdad/proposals/   →   cdad/adr/ + cdad/context/
   you write intent          agent drafts          you apply, after approval
   (always writable)         (agent writable)      (blocked for agents)
```

## Lifecycle

| State | Meaning |
|---|---|
| `PROPOSAL-<slug>.md` | awaiting your review |
| deleted | rejected, or promoted to an ADR |

Delete proposals once resolved. A directory full of stale drafts is the same
failure as stale context: it makes the current state ambiguous.

## Naming

`PROPOSAL-<short-kebab-summary>.md` — no numbers. Numbering belongs to ADRs,
which are the permanent record. A proposal that never gets accepted should not
consume a number.
