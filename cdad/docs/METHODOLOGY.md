# CDAD — The methodology

> When context doesn't govern AI, AI governs the solution.

This document is for humans. It is deliberately outside the agent's context
window: an agent does not need to understand CDAD to comply with it, and every
token spent explaining the methodology is a token not spent on the problem.

## The premise

AI accelerates implementation. Humans govern context and architecture.

The failure mode CDAD addresses is not bad code — agents write reasonable code.
It is **architectural drift**: a sequence of individually defensible changes that
collectively move the solution somewhere nobody decided to go. Drift is invisible
at the commit level and only visible at the architecture level, which is exactly
the level nobody is reviewing.

## Context layers

| Layer | Contents | Policy | Who edits |
|---|---|---|---|
| L0 | `cdad/context/` — the map, vision, architecture, principles, constraints | propose only | Solution Designer |
| L1 | `cdad/adr/` — accepted decisions | propose with review | Solution Designer |
| L2 | `docs/` — diagrams, specifications | editable with review | anyone |
| L3 | `src/`, `tests/`, pipelines, infrastructure code | editable | agents and humans |

The layer determines two things: **who may edit** and **when it loads into
context**. Earlier versions of CDAD only defined the first, which is what made
the model expensive — every layer loaded on every session regardless of
relevance.

## The three enforcement planes

CDAD's guarantees do not come from asking the agent nicely. They come from
putting each concern in the plane that can actually enforce it.

| Plane | Mechanism | Guarantee | Cost per session |
|---|---|---|---|
| Control | `permissions.deny`, PreToolUse hook | Deterministic | Zero context |
| Build | `cdad/scripts/cdad-check-stack.sh` in CI | Deterministic, after the fact | Zero context |
| Instruction | `AGENTS.md`, `.claude/rules/` | Probabilistic | Tokens |
| Procedural | `.claude/skills/` | On demand | Zero until invoked |

The rule: **anything that can be enforced in the control plane must not be
written as an instruction.** An instruction is a request the model may decline
under pressure; a deny rule is not. Writing "AI must not modify L0 files" into
context is strictly worse than blocking the write — it costs tokens every
session and holds only probabilistically.

Instructions remain necessary for everything that requires judgment: whether a
change is architectural, whether code contradicts context, whether an
abstraction is warranted. No permission rule can decide those.

## What lives where

| Concern | Location | Loads |
|---|---|---|
| Non-negotiable behavioral rules | `AGENTS.md`, imported by `.claude/CLAUDE.md` | always |
| Hard project constraints | `cdad/context/constraints.md`, imported by `.claude/CLAUDE.md` | always |
| Rules for one area of the codebase | `.claude/rules/*.md` with `paths:` | when touching matching files |
| Proposal, ADR, audit procedures | `.claude/skills/*/SKILL.md` | when invoked |
| The stack and architecture map | `cdad/context/stack.md` | when the task needs it |
| Architecture prose, vision, principles | `cdad/context/` | when the task needs them |
| Accepted decisions | `cdad/adr/` | when the task needs them |
| Change requests | `cdad/CHANGE-REQUEST.md` | never |
| Agent drafts awaiting review | `cdad/proposals/` | never |
| This document | `cdad/docs/` | never |

## The change flow

Governance fails when the compliant path is harder than the workaround. CDAD
therefore has exactly one entry point for change, and it is a plain markdown
file that is always in the same place.

```
cdad/CHANGE-REQUEST.md  ->  cdad/proposals/  ->  cdad/adr/ + cdad/context/
     Designer states           agent drafts         Designer applies
     intent, 4 lines           a full proposal      after approval
```

The asymmetry is the mechanism: `cdad/proposals/` is the only directory under
`cdad/` an agent can write to. An agent that wants to change the architecture
has exactly one move available — write a reviewable draft. There is no path
where it edits the architecture and no path where it silently skips review,
because the alternative is blocked at the permission layer rather than
discouraged in prose.

This also removes the friction that kills governance models in practice. The
Designer does not need to remember which of six files to edit, or how to format
an ADR. They write four lines in one known location.

## Governance model

**Human approval required for:** architectural direction, paradigm, module
boundaries, integration strategy, deployment strategy, data model, frameworks,
runtimes, cloud platform and managed services, and any change to L0.

**Agents may:** read and analyze context, detect inconsistencies, propose
changes, and generate implementation aligned with the governed context.

**The golden rule:** an agent may suggest, analyze, and accelerate. It may not
redefine architecture without explicit approval from the Solution Designer.

## The map

`cdad/context/stack.md` is the one page that answers "what is this system" in a
single screen: the stack table, the component map, the deployment topology, the
observability view, the dependency rules, and the change log. It is written in Markdown and Mermaid, so it renders in
GitHub and any IDE without an image to regenerate and without a diagram tool to
keep licensed.

It is governed at L0 and updated in the same change as the ADR that approves the
architectural decision. Three mechanisms hold that line, in descending strength:

1. **CI gate** — `cdad/scripts/cdad-check-stack.sh` fails the build when an ADR
   changes and the map does not.
2. **ADR procedure** — the `cdad-adr` skill requires a stack map delta section
   with before/after rows; an ADR without one is incomplete.
3. **Audit** — the `cdad-audit` skill checks each map claim against dependency
   manifests, the real import graph, and deployment definitions.

A row in "Stack at a glance" with no ADR in its "Locked by" column is a finding
in its own right: a decision that entered the system without passing through
governance.

## Context freshness

A stale context file is worse than a missing one — it produces confident,
consistent, wrong behavior across every agent in the project.

Context freshness is therefore an operational responsibility, not a
documentation chore. Run the `cdad-audit` skill before releases and after large
merges. When implementation and context diverge, the Solution Designer decides
which one is wrong; the agent is not permitted to assume the code is right.

## Operational boundary

CDAD does not slow implementation down. It prevents accidental architectural
change. Everything under L3 stays fully editable, and the majority of day-to-day
work never touches the governance path at all.

If CDAD is producing friction on routine work, the constraints are written too
broadly — narrow them rather than working around them.
