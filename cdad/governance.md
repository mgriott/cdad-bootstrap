# CDAD Governance

## Definition

Governance of Context is the set of practices, rules, and mechanisms used to control, protect, and evolve the knowledge that guides AI during the lifecycle of a solution.

## Single Source of Truth

The official source of truth for this project is the governed context stored in:

- `cdad/project-context.md`
- `cdad/context/`
- `cdad/adr/`
- `cdad/governance.md`
- `cdad/guardrails.md`

## Protection Levels

| Level | Scope | Policy |
|---|---|---|
| L0 | Foundational context | Propose only |
| L1 | Architecture decisions | Propose with review |
| L2 | Technical documentation | Editable with review |
| L3 | Implementation | Editable |

## Human Approval Required For

- Architecture changes.
- Paradigm changes.
- Changes to principles.
- Changes to constraints.
- Major framework changes.
- Major infrastructure changes.
- Major cloud platform changes.
- Major changes in integration strategy.
- Major changes in data model.
- Any change affecting L0 files.

## Context Freshness

Governed context must remain current.

If the implementation changes in a way that invalidates the context, the AI must report it as a context conflict.

The Solution Designer decides whether to update context, revert implementation, or create a new ADR.

## CDAD Golden Rule

AI may suggest.  
AI may analyze.  
AI may accelerate.  

But AI must not redefine architecture without explicit approval from the Solution Designer.

## Operational Boundary

CDAD does not prevent implementation.

CDAD prevents accidental architectural drift.
