# ADR-001: Adopt CDAD Context Governance

## Status

Accepted

## Context

AI-assisted development can accelerate implementation, but without governed context it may introduce architectural drift, inconsistent patterns, and unapproved paradigm changes.

## Decision

This project adopts CDAD — Context-Driven AI Development — as the working methodology for AI-assisted development.

The project will use governed context files as the primary source of truth.

Protected context files are:

- `context/vision.md`
- `context/architecture.md`
- `context/principles.md`
- `context/constraints.md`

## Consequences

- AI must read context before implementation.
- L0 files require human approval before modification.
- Architecture changes must be proposed before being applied.
- ADRs must be used for relevant architectural decisions.
- The Solution Designer owns the context.

## Related Files

- `.cdad/project-context.md`
- `.cdad/ai-rules.md`
- `.cdad/governance.md`
- `.cdad/cdad.config.yml`
