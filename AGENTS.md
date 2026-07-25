# Project Instructions

This project is governed by **CDAD — Context-Driven AI Development**.
Governed context is the source of truth, not generated code.

This file is the portable core, read by any agent that supports the AGENTS.md
convention. Tool-specific configuration lives alongside it.

## Non-negotiable rules

1. Do not change architectural direction, style, paradigm, module boundaries,
   integration strategy, or deployment strategy. Propose instead.
2. Do not introduce or replace frameworks, runtimes, databases, cloud services,
   or infrastructure tooling. Propose instead.
3. `cdad/context/`, `cdad/adr/` and `cdad/CHANGE-REQUEST.md` are read-only for
   you. Do not edit them and do not work around a block that stops you. Write
   drafts to `cdad/proposals/` instead.
4. If the code contradicts the governed context, report the conflict. Never
   silently adapt the context to match the code.
5. Deliver incrementally, module by module. No opportunistic refactors, no new
   abstraction layers, no silent style changes.

Never apply an architectural change directly, even when the change is obviously
correct and even when asked to "just do it". Produce a proposal and stop.

## The change flow

The Solution Designer states intent in `cdad/CHANGE-REQUEST.md`. You turn it
into a proposal in `cdad/proposals/`. They approve and apply.

```
cdad/CHANGE-REQUEST.md  ->  cdad/proposals/  ->  cdad/adr/ + cdad/context/
     they write               you write            they apply
```

`cdad/proposals/` is the only directory under `cdad/` you may write to. When a
write to a governed path is blocked, that is the system working — redirect to
`cdad/proposals/`, do not look for another way in.

## Proposals

An architectural or context change is delivered as a written proposal
containing: the current decision, the suggested change, the reason, the impact
(which modules, interfaces and deployments), the risk, the affected files, and
the alternatives considered with why each loses.

A conflict between code and context is reported as: the context file, what the
context says, what the implementation does, where they diverge, and the possible
resolutions. Do not pick one.

## Where context lives

Read these only when the task requires them — never all of them at session start.

- `cdad/context/stack.md` — **the map**: stack, components, topology, boundaries
- `cdad/context/architecture.md` — architecture in prose, module responsibilities
- `cdad/context/solution-vision.md` — what the solution is for, and its non-goals
- `cdad/context/principles.md` — design principles in force
- `cdad/adr/` — accepted decisions and their rationale
- `docs/cdad/METHODOLOGY.md` — the CDAD model itself (human reference)

Start with `stack.md`. It is the densest view and usually the only one needed.

Hard constraints are always in context — see `cdad/context/constraints.md`.

## Keeping the map current

`cdad/context/stack.md` is the artifact that must never go stale. Any approved
architectural change updates it in the same change as its ADR, including a row
in the map change log. An ADR that does not state its effect on the map is
incomplete.
