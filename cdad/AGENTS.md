# CDAD Agent Instructions

This project follows **CDAD — Context-Driven AI Development**.

`cdad/AGENTS.md` is the official entry point for AI agents and Agentic Development Environments (ADEs).

Before making implementation decisions, AI agents and ADEs must read and respect the governed context.

## Core Principles

> Context is the Source of Truth.

> When context doesn't govern AI, AI governs the solution.

AI accelerates implementation.

Humans govern context and architecture.

## Required Context Reading Order

1. `cdad/project-context.md`
2. `cdad/ai-rules.md`
3. `cdad/governance.md`
4. `cdad/guardrails.md`
5. `cdad/context/vision.md`
6. `cdad/context/architecture.md`
7. `cdad/context/principles.md`
8. `cdad/context/constraints.md`
9. `cdad/adr/`

## Protected Files

The following files are classified as **L0 — Foundational Context**:

- `cdad/context/vision.md`
- `cdad/context/architecture.md`
- `cdad/context/principles.md`
- `cdad/context/constraints.md`

AI may:

- Read
- Analyze
- Reference
- Suggest improvements

AI must not:

- Modify L0 files directly
- Redefine the architectural direction
- Change the selected paradigm
- Change foundational principles
- Remove architectural constraints
- Treat generated code as the source of truth

unless explicitly approved by the Solution Designer.

## Architecture Change Policy

If an architectural change is required, do not apply the change directly.

Return:

```text
Proposed Architecture Change

Current Decision:
...

Suggested Change:
...

Reason:
...

Impact:
...

Risk:
...

Affected Files:
...

Status:
Requires Architect Approval
```

## Guardrails

AI must operate within the guardrails defined by CDAD.

Examples:

- Follow the current architecture.
- Preserve the selected paradigm.
- Respect constraints and principles.
- Prefer ADRs for architectural changes.
- Avoid introducing new frameworks without approval.
- Avoid introducing new architectural patterns without approval.
- Ask for approval before changing L0 context.
- Report conflicts between implementation and governed context.

## Expected Behavior

Implementation may evolve.

Architecture, principles, constraints, and vision are governed assets and require explicit approval before modification.
