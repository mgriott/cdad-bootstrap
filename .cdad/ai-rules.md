# CDAD AI Rules

These rules must be followed by AI agents, coding assistants, and Agentic Development Environments working in this project.

## General Rules

1. Always read governed context before implementation.
2. Do not change architectural direction without approval.
3. Do not introduce a new paradigm without proposing an ADR.
4. Do not modify L0 files automatically.
5. Prefer small, traceable changes.
6. Keep implementation aligned with `context/architecture.md`.
7. Keep decisions aligned with `context/principles.md`.
8. Respect constraints defined in `context/constraints.md`.

## L0 Protection Rule

L0 files are foundational.

AI must not directly edit:

- `context/vision.md`
- `context/architecture.md`
- `context/principles.md`
- `context/constraints.md`

If a change is needed, AI must produce a proposal.

## Required Proposal Format

```text
Proposed Context Change

File:
...

Current Statement:
...

Suggested Change:
...

Reason:
...

Impact:
...

Risk:
...

Status:
Requires Solution Designer Approval
```

## Architecture Change Format

```text
Proposed Architecture Change

Current Decision:
...

Suggested Change:
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

## Coding Behavior

When generating or changing code:

- Use the current architecture.
- Use the existing folder structure.
- Do not introduce unnecessary abstractions.
- Do not change the project style silently.
- Do not rewrite modules using a different paradigm unless approved.
- Explain architectural impact when relevant.
