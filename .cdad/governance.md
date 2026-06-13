# CDAD Governance

## Definition

Governance of Context is the set of practices, rules, and mechanisms used to control, protect, and evolve the knowledge that guides AI during the lifecycle of a solution.

## Single Source of Truth

The official source of truth for this project is the governed context stored in:

- `.cdad/`
- `context/`
- `adr/`
- `business/`

## Protection Levels

| Level | Scope | Policy |
|---|---|---|
| L0 | Foundational context | Propose only |
| L1 | Architecture and business decisions | Propose with review |
| L2 | Technical documentation | Editable with review |
| L3 | Implementation | Editable |

## Human Approval Required For

- Architecture changes.
- Paradigm changes.
- Changes to principles.
- Changes to constraints.
- Changes to business rules.
- Major changes in integration strategy.
- Major changes in data model.
- Any change affecting L0 files.

## CDAD Golden Rule

AI may suggest.  
AI may analyze.  
AI may accelerate.  

But AI must not redefine architecture without explicit approval from the Solution Designer.

## CDAD Principle

AI may accelerate implementation.

AI must not redefine the architectural direction, design principles, selected paradigm, or foundational constraints of a solution without explicit approval from the Solution Designer.