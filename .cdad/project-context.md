# CDAD Project Context

## Purpose

This file defines how CDAD is applied in this project.

CDAD — Context-Driven AI Development — is a methodology for AI-assisted software development based on governed context, architectural control, knowledge traceability, and sustainable acceleration.

## Core Statements

> When context doesn't govern AI, AI governs the solution.

> Context is the new Source Code.

## What CDAD Means in This Project

This project uses CDAD to ensure that AI agents and ADEs generate, refactor, and analyze code without breaking architectural intent.

The goal is not to limit AI.

The goal is to ensure that AI accelerates implementation while the Solution Designer governs the context.

## Context Ownership

The Solution Designer owns the project context.

AI agents may:

- Read context.
- Analyze context.
- Detect inconsistencies.
- Suggest improvements.
- Generate implementation aligned with context.

AI agents must not:

- Redefine architecture.
- Change the project paradigm.
- Modify foundational principles.
- Rewrite protected context.
- Introduce major design decisions without approval.

## Context Layers

### L0 — Foundational Context

Source of truth.

- `context/vision.md`
- `context/architecture.md`
- `context/principles.md`
- `context/constraints.md`

Policy: `propose_only`

### L1 — Architecture and Business Context

Requires human review.

- `adr/`
- `business/`

Policy: `propose_with_review`

### L2 — Technical Documentation

May be generated or updated with review.

- `docs/`
- diagrams
- specifications

Policy: `editable_with_review`

### L3 — Implementation

May be generated, modified, or refactored.

- `src/`
- `tests/`
- scripts
- pipelines

Policy: `editable`

## CDAD Workflow

1. Define context.
2. Validate architecture.
3. Generate or modify implementation.
4. Detect impact.
5. Propose ADRs when needed.
6. Refine context under human approval.
7. Keep context versioned.

## Important Reminder

CDAD Bootstrap does not impose an architecture.

It creates a governed space where the Solution Designer defines the architecture.

## CDAD Evolution

This project structure represents the Bootstrap layer of the CDAD ecosystem.

Future CDAD components include:

- CDAD CLI
- CDAD Inspector
- CDAD Context Platform

The long-term vision is to enable governed context to be consumed by any Agentic Development Environment (ADE) or AI agent.