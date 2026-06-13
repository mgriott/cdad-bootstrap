# CDAD Guardrails

Guardrails are operational boundaries that help AI agents, ADEs, and platform engines work safely under CDAD.

They do not replace human judgment.

They make the CDAD governance model explicit and actionable.

## Guardrail 1 — Context First

Before implementation, AI must read the governed context.

Required files:

- `cdad/AGENTS.md`
- `cdad/project-context.md`
- `cdad/ai-rules.md`
- `cdad/governance.md`
- `cdad/guardrails.md`
- `cdad/context/vision.md`
- `cdad/context/architecture.md`
- `cdad/context/principles.md`
- `cdad/context/constraints.md`

## Guardrail 2 — L0 Protection

AI must not directly modify L0 files:

- `cdad/context/vision.md`
- `cdad/context/architecture.md`
- `cdad/context/principles.md`
- `cdad/context/constraints.md`

AI may propose changes, but approval is required before modification.

## Guardrail 3 — Architecture Protection

AI must not change:

- Architectural direction
- Architectural style
- Main design paradigm
- Core module boundaries
- Integration strategy
- Deployment strategy

without explicit approval.

## Guardrail 4 — ADR Required for Architecture Change

Any relevant architectural change must be captured as an ADR.

The ADR should include:

- Context
- Decision
- Alternatives considered
- Consequences
- Risks
- Approval status

## Guardrail 5 — No Silent Paradigm Shift

AI must not silently move the project from one paradigm to another.

Examples:

- Monolith to microservices
- REST to event-driven
- Layered architecture to clean architecture
- Synchronous to asynchronous communication
- Local runtime to cloud-native deployment

Such changes require an explicit Proposed Architecture Change.

## Guardrail 6 — Framework and Platform Control

AI must not introduce or replace major frameworks, runtimes, cloud services, infrastructure tools, or platform engines without approval.

Examples:

- Express to NestJS
- PostgreSQL to MongoDB
- Docker Compose to Kubernetes
- Terraform to Pulumi
- AWS to Azure
- ECS to EKS

## Guardrail 7 — Context Conflict Reporting

If code and governed context disagree, AI must report the conflict.

It must not silently adapt the project to the code.

## Guardrail 8 — Module-by-Module Delivery

AI should implement incrementally.

Each module should remain aligned with:

- Vision
- Architecture
- Principles
- Constraints
- Relevant ADRs

## Guardrail 9 — Human Approval for Context Evolution

Context may evolve.

But context evolution must be intentional, reviewed, and approved.

AI can propose.

Humans approve.

## Guardrail 10 — Context Freshness

A stale context file can misguide AI.

If AI detects outdated context, it should request review instead of continuing blindly.
