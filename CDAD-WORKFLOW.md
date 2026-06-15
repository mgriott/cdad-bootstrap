# CDAD Workflow

> Human-governed context. AI-accelerated implementation.

This document describes a recommended workflow for applying **CDAD — Context-Driven AI Development** in real-world projects.

The objective is simple:

* Humans define intent.
* CDAD governs context.
* AI accelerates implementation.

---

## Workflow Overview

1. Human Discovery
2. AI-Assisted Analysis
3. CDAD Context Definition
4. Project Foundation and Scaffolding
5. Incremental Development
6. Evolution Through Approval

---

## 1. Human Discovery → Human-Governed Design

Every project starts with human understanding.

The Solution Designer defines the initial direction of the solution, including:

* Requirements
* Business objectives
* Solution vision
* Expected outcomes
* Architectural direction
* Design principles
* Technical constraints
* Frameworks and technology stack
* Cloud strategy (if applicable)

This phase establishes the initial intent behind the solution.

At this stage, the objective is not implementation.

The objective is understanding the problem, defining the desired outcome, and establishing an initial architectural direction.

Human intent is the starting point of CDAD.

---

## 2. AI-Assisted Analysis → Human + AI

Once the initial proposal exists, AI agents and ADEs assist in analyzing and challenging the proposed solution.

The objective is to refine and validate:

* Requirements
* Solution vision
* Expected outcomes
* Architectural decisions
* Design alternatives
* Technology stack
* Constraints
* Risks and trade-offs

AI may contribute by:

* Refining requirements
* Identifying inconsistencies
* Challenging assumptions
* Evaluating alternatives
* Proposing improvements
* Improving architecture documentation
* Enriching design decisions

The goal is not to replace architectural thinking.

The goal is to amplify it.

The final decision remains under human ownership.

Before moving forward, the Solution Designer reviews and validates the proposed direction.

---

## 3. CDAD Context Definition → Governed Context

Once the solution direction has been approved, the governed context is formalized through CDAD.

The approved knowledge is captured in the context files:

* `solution-vision.md`
* `architecture.md`
* `principles.md`
* `constraints.md`
* ADRs
* Governance rules
* Guardrails

These artifacts become the official source of truth for the project.

From this point forward:

* AI agents operate under the governed context.
* ADEs operate under the governed context.
* Platform engines operate under the governed context.

The project does not evolve from isolated prompts.

The project evolves from governed context.

This is the core principle of CDAD.

---

## 4. Project Foundation and Scaffolding → ADEs, AI, and Platform Engines

After the governed context has been established, the technical foundation is generated.

The ADE consumes the governed context before generating the project structure.

This may be performed using:

* Kiro
* Codex
* Cursor
* Windsurf
* Claude Code
* Framework CLIs
* Templates
* Infrastructure generators
* Platform-specific engines

Examples:

* `dotnet new`
* `npm create`
* NestJS CLI
* Spring Initializr
* Terraform
* Kubernetes generators

The generated foundation may include:

* Project structure
* Modules
* Parent classes and abstractions
* Interfaces and contracts
* Framework configuration
* Initial integrations
* Infrastructure skeletons
* CI/CD foundations
* Deployment foundations

At this stage, the objective is to establish a coherent technical baseline aligned with the governed architecture.

The focus is structure and integration rather than deep business implementation.

The generated foundation must remain aligned with the governed context.

---

## 5. Incremental Development → Human + ADEs + AI

Development proceeds incrementally and module by module.

The governed context guides implementation.

ADEs and AI may accelerate:

* Business logic
* Services
* APIs
* User interfaces
* Integrations
* Tests
* Infrastructure
* Automation

The Solution Designer remains responsible for:

* Architectural integrity
* Design consistency
* Context evolution
* Strategic decisions

CDAD protects architectural intent through governance, guardrails, and context protection patterns.

Human intent remains the governing force behind the solution.

---

## 6. Evolution Through Approval → Governed Change

Architectures evolve.

Requirements change.

Technologies mature.

CDAD does not prevent change.

CDAD governs change.

When significant architectural, technological, or strategic changes are required:

* ADEs or AI propose.
* Humans review.
* Humans approve.
* Context evolves.
* Implementation follows.

Major changes should be reflected in:

* Governed context files
* ADRs
* Architecture documentation

Architecture remains intentional rather than accidental.

---

## CDAD Visual Flow

```text
Human Discovery
        ↓
AI-Assisted Analysis
        ↓
CDAD Context Definition
        ↓
Project Foundation & Scaffolding
        ↓
Incremental Development
        ↓
Controlled Evolution
```

---

## CDAD in One Sentence

The Solution Designer governs the context.

CDAD governs the development process.

ADEs, AI agents, and platform engines accelerate implementation.
