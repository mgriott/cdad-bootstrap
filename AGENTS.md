# CDAD Agent Instructions

This project follows **CDAD — Context-Driven AI Development**.

Before making implementation decisions, AI agents and ADEs must read and respect the governed context.

## Required Context Reading Order

1. `.cdad/project-context.md`
2. `.cdad/ai-rules.md`
3. `.cdad/governance.md`
4. `context/vision.md`
5. `context/architecture.md`
6. `context/principles.md`
7. `context/constraints.md`
8. `adr/`

## Core Rule

> When context doesn't govern AI, AI governs the solution.

AI must operate under the current governed context.

## Protected Files

The following files are **L0 protected context**:

- `context/vision.md`
- `context/architecture.md`
- `context/principles.md`
- `context/constraints.md`

AI may read, analyze, reference, and suggest improvements.

AI must not modify these files directly unless the Solution Designer explicitly approves the change.

## If Architecture Change Is Needed

Do not apply the change directly.

Return:

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

Status:
Requires Architect Approval
```

## Expected Behavior

- Follow the current architecture.
- Preserve the selected paradigm.
- Respect constraints and principles.
- Prefer ADRs for architectural changes.
- Avoid introducing new frameworks, paradigms, or patterns without approval.
- Ask for approval before changing L0 context.
