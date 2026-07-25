# Principles

Design principles in force. A principle earns its place only if it rules
something out. If a principle would never cause you to reject a pull request,
delete it.

## Format

Each principle: the rule, then the trade-off it accepts.

- **<Principle>** — <what it rules out>. Accepts: <cost of holding this line>.

## Examples of the right shape

- **Boundaries are enforced at compile time, not by convention** — rules out
  cross-module imports that rely on discipline. Accepts: more ceremony when
  adding a module.
- **Failure is explicit in the type signature** — rules out exceptions as
  control flow. Accepts: more verbose call sites.

## Anti-examples

"Write clean code", "prefer simplicity", "follow best practices". These rule
nothing out and cost context tokens to carry.

---
Governance: L0. Read-only for AI agents.
