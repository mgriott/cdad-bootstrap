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
3. `CHANGE-REQUEST.md` is always read-only for you, in every regime. Under the
   governed regime (see Regime below), `cdad/context/`, `cdad/adr/`, and
   `SOURCE-BRIEF.*` are also read-only. Do not edit any of them and do not work
   around a block that stops you. Write drafts to `cdad/proposals/` instead.
4. If the code contradicts the governed context, report the conflict. Never
   silently adapt the context to match the code.
5. Deliver incrementally, module by module. No opportunistic refactors, no new
   abstraction layers, no silent style changes.

Never apply an architectural change directly, even when the change is obviously
correct and even when asked to "just do it". Produce a proposal and stop.

## Regime

This project has two regimes, discriminated by the file `cdad/.frozen`.

**Pre-freeze** (`cdad/.frozen` absent). No ratified context exists yet. You may
write `cdad/context/` and `cdad/adr/` directly, as part of bootstrapping. Rule 3
above does not apply to those paths in this regime.

**Governed** (`cdad/.frozen` present). Rule 3 applies in full. Those paths are
read-only for you.

In both regimes, without exception: you never create, edit or delete
`cdad/.frozen`, and you never edit `AGENTS.md`, `.claude/rules/`,
`.claude/settings.json`, `.claude/hooks/`, `.kiro/settings/`, `.kiro/steering/`
or `CHANGE-REQUEST.md`. Freezing is a human act, run through
`cdad/scripts/cdad-freeze.sh`.

If `cdad/context/` already holds real content but `cdad/.frozen` is absent, stop
and say so. That project was probably governed under an older version of CDAD
and needs to be frozen, not bootstrapped again.

## Drift

Paths listed in the `cdad-drift-signals` block of `cdad/context/stack.md` carry
architectural weight even though they sit outside the governed paths. You may
write to them. When you do, check whether the change contradicts
`cdad/context/` or an accepted ADR. If it does, draft a proposal under
`cdad/proposals/` and hand the Solution Designer the commands to ratify it.
Never promote a proposal yourself.

## The change flow

The Solution Designer states intent in `CHANGE-REQUEST.md`, at the project
root. You turn it into a proposal in `cdad/proposals/`. They approve and apply.

```
CHANGE-REQUEST.md  ->  cdad/proposals/  ->  cdad/adr/ + cdad/context/
     they write            you write            they apply
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
- `cdad/docs/DOCS.md` — the CDAD model itself (human reference)

Start with `stack.md`. It is the densest view and usually the only one needed.

Hard constraints are always in context — see `cdad/context/constraints.md`.

## Keeping the map current

`cdad/context/stack.md` is the artifact that must never go stale. Any approved
architectural change updates it in the same change as its ADR, including a row
in the map change log. An ADR that does not state its effect on the map is
incomplete.
