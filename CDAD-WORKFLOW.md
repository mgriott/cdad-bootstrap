# CDAD Workflow

> Human-governed context. AI-accelerated implementation.

This document describes a typical workflow for applying **CDAD — Context-Driven AI Development** in a real project.

## 1. Solution Vision, Architecture, and Constraints → Human-Governed Design

The Solution Designer defines the initial solution vision, architecture, principles, and constraints of the solution.

AI agents and ADEs may actively assist during this phase by:

- Refining requirements
- Identifying inconsistencies
- Proposing alternatives
- Challenging assumptions
- Improving architecture documentation
- Enriching design decisions

The goal is to leverage AI as a design partner while maintaining human ownership of the solution.

Before moving to implementation, the governed context should be reviewed and validated by the Solution Designer.

Once approved, these documents become the governed context and the source of truth for the project.

## 2. Project Foundation and Scaffolding → ADEs, AI, and Platform Engines

The initial project structure is generated using Agentic Development Environments (ADEs), AI agents, framework CLIs, templates, or platform-specific engines.

Examples:

- Kiro
- Codex
- Cursor
- Windsurf
- Claude Code
- `dotnet new`
- `npm create`
- NestJS CLI
- Spring Initializr
- Terraform
- Kubernetes generators

The generated structure must align with the governed context and architectural direction defined by the Solution Designer.

## 3. Context Governance → CDAD

The governed context is loaded and becomes the reference point for all future decisions.

AI agents, ADEs, and platform engines must operate under this context.

The project does not evolve from isolated prompts.

The project evolves from governed context.

## 4. Incremental Development → Human + ADEs + AI

Development proceeds module by module.

- ADEs and AI accelerate implementation.
- The Solution Designer governs context and architecture.
- CDAD protects architectural intent through governance, guardrails, and context protection.

## 5. Evolution Through Approval

If architectural changes are required:

- ADEs or AI propose.
- Humans review and approve.
- Context evolves.
- Implementation follows.

Architecture remains intentional rather than accidental.

## CDAD in One Sentence

The Solution Designer governs the context.

CDAD governs the development process.

ADEs, AI, and platform engines accelerate implementation.
