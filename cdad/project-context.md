# CDAD Project Context

## Purpose

This file defines how CDAD is applied in this project.

CDAD — Context-Driven AI Development — is a methodology for AI-assisted software development based on governed context, architectural control, knowledge traceability, and sustainable acceleration.

## Core Statements

> When context doesn't govern AI, AI governs the solution.

> Context is the Source of Truth.

> Context is the new Source Code.

## What CDAD Means in This Project

This project uses CDAD to ensure that AI agents, ADEs, and platform engines generate, refactor, analyze, and evolve implementation artifacts without breaking architectural intent.

The goal is not to limit AI.

The goal is to ensure that AI accelerates implementation while the Solution Designer governs the context and architecture.

## Context Ownership

The Solution Designer owns the project context.

AI agents may:

- Read context.
- Analyze context.
- Detect inconsistencies.
- Suggest improvements.
- Generate implementation aligned with context.
- Propose architecture changes.

AI agents must not:

- Redefine architecture.
- Change the project paradigm.
- Modify foundational principles.
- Rewrite protected context.
- Introduce major design decisions without approval.
- Treat generated code as a replacement for governed context.

## Context Layers

### L0 — Foundational Context

Source of truth.

- `cdad/context/solution-vision.md`
- `cdad/context/architecture.md`
- `cdad/context/principles.md`
- `cdad/context/constraints.md`

Policy: `propose_only`

### L1 — Architecture Decision Context

Requires human review.

- `cdad/adr/`

Policy: `propose_with_review`

### L2 — Technical Documentation

May be generated or updated with review.

- diagrams
- specifications
- technical documents

Policy: `editable_with_review`

### L3 — Implementation

May be generated, modified, or refactored.

- `src/`
- `tests/`
- scripts
- pipelines
- infrastructure code

Policy: `editable`

## CDAD Workflow

1. Define context.
2. Validate context.
3. Generate or modify implementation.
4. Detect architectural impact.
5. Propose ADRs when needed.
6. Refine context under human approval.
7. Keep context versioned and current.

## Context Freshness Principle

A stale context file can be worse than no context file.

The governed context must remain synchronized with the actual solution.

If implementation evolves, the Solution Designer must review whether the governed context also needs to evolve.

## Important Reminder

CDAD Bootstrap does not impose an architecture.

It creates a governed space where the Solution Designer defines, protects, and evolves the architecture.
