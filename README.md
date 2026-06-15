# CDAD Bootstrap

> When context doesn't govern AI, AI governs the solution.

The official starter kit for **Context-Driven AI Development (CDAD)**.

**Context is the Source of Truth.**

## What is CDAD?

CDAD is a methodology for AI-assisted software development based on governed context.

AI accelerates implementation.

Humans govern context and architecture.

## CDAD Core Components

- Governance of Context
- Context Protection Pattern (CPP)
- Guardrails
- Context Layers
- ADE Integration

## Getting Started

1. Download or clone this repository.
2. Copy the `cdad/` directory into your project.
3. Complete the files under `cdad/context/`.
4. Configure your ADE to read and follow `cdad/AGENTS.md` before making implementation decisions.

## Repository Structure

```text
cdad/
├── AGENTS.md
├── project-context.md
├── ai-rules.md
├── governance.md
├── guardrails.md
│
├── context/
│   ├── solution-vision.md
│   ├── architecture.md
│   ├── principles.md
│   ├── constraints.md
│   └── glossary.md
│
└── adr/
    └── ADR-001-context-governance.md
```

## What Should Be Customized?

CDAD Bootstrap provides the governance structure and AI operating rules.

In most cases, users should focus on maintaining the files under:

```text
cdad/context/
```

Specifically:

- `cdad/context/solution-vision.md`
- `cdad/context/architecture.md`
- `cdad/context/principles.md`
- `cdad/context/constraints.md`

These files represent the governed context and the source of truth for the project.

The files under `cdad/` such as `AGENTS.md`, `ai-rules.md`, `governance.md`, and `guardrails.md` are part of the CDAD runtime structure and typically require little or no modification.

The Solution Designer defines and evolves the context.

AI agents, ADEs, and platform engines consume and operate under that context.

## Learn More

To understand how CDAD is applied in real projects, see:

[CDAD Workflow](./CDAD-WORKFLOW.md)

## Related Projects

- **CDAD Framework** — Methodology, whitepapers, principles, and governance model.
- **CDAD Bootstrap** — Project scaffolding and context governance starter kit.

CDAD Bootstrap is the practical implementation of the CDAD methodology.

## Evolution

CDAD is an evolving methodology focused on the governance of context in AI-assisted development.

Future contributions may expand its application across:

- Software Solutions
- Cloud and Infrastructure
- Agentic Systems
- Documentation
- Knowledge Governance

while preserving the core principle:

> Context is the Source of Truth.

## License

This work is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

You are free to share, adapt, and build upon this work, including for commercial purposes, provided appropriate attribution is given.

License:  
https://creativecommons.org/licenses/by/4.0/

Copyright © 2026 Moisés Griott
