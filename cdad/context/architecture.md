# Architecture

The current architecture of this solution. Loaded on demand, not at session
start — so it can be longer than `constraints.md`, but every section should
still be something an agent would act on.

## Architectural style

<layered / hexagonal / event-driven / microservices / modular monolith>

State the style explicitly. Ambiguity here is what produces silent paradigm
drift.

## Modules and boundaries

| Module | Responsibility | May depend on | Must not depend on |
|---|---|---|---|

## Integration strategy

How modules and external systems talk to each other. Protocols, contracts,
where the boundaries are enforced.

## Data model ownership

Which module owns which data. Where the write path is. What is derived.

## Deployment topology

What gets deployed as what, and to where.

## Known deviations

Places where the implementation knowingly diverges from the ideal, and why.
Recording these prevents an agent from "fixing" a deliberate trade-off.

---
Governance: L0. Read-only for AI agents. Changes require an approved ADR.
