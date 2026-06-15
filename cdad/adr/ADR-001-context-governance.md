# ADR-001: Adopt CDAD Context Governance

## Status

Accepted

## Context

AI-assisted development can accelerate implementation, but without governed context it may introduce architectural drift, inconsistent patterns, unapproved paradigm changes, and loss of design intent.

## Decision

This project adopts **CDAD — Context-Driven AI Development** as the working methodology for AI-assisted development.

The project will use governed context files as the primary source of truth.

Protected L0 context files are:

- `cdad/context/solution-vision.md`
- `cdad/context/architecture.md`
- `cdad/context/principles.md`
- `cdad/context/constraints.md`

## Consequences

- AI must read context before implementation.
- L0 files require human approval before modification.
- Architecture changes must be proposed before being applied.
- ADRs must be used for relevant architectural decisions.
- The Solution Designer owns the context.
- AI agents, ADEs, and platform engines operate under governed context.

## Alternatives Considered

- Relying only on prompts.
- Relying only on generated code.
- Relying only on informal documentation.
- Using AI without context governance.

## Related Files

- `cdad/project-context.md`
- `cdad/ai-rules.md`
- `cdad/governance.md`
- `cdad/guardrails.md`
