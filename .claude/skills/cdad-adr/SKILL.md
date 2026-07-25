---
name: cdad-adr
description: Draft an Architecture Decision Record for a change the Solution Designer has already approved. Use when the user says a proposal is approved, asks to record or document a decision, asks to write an ADR, or asks to update the ADR index. Do not use for proposing changes that are not yet approved.
---

# Draft an ADR

Only draft an ADR for a decision a human has explicitly approved. If approval is
unclear, ask. An ADR records a decision that was made — it is not a place to
argue for one.

`cdad/adr/` is write-protected. Write the draft to
`cdad/proposals/ADR-DRAFT-<slug>.md` and tell the user the target filename under
`cdad/adr/`. They promote it. Do not attempt to write into `cdad/adr/` yourself.

If a proposal for this change exists in `cdad/proposals/`, base the ADR on it
rather than restating the reasoning from scratch.

## Numbering

Read the existing filenames in `cdad/adr/` and take the next sequential number.
Filename: `ADR-NNN-short-kebab-title.md`.

## Template

```markdown
# ADR-NNN — <Title>

- Status: Accepted
- Date: YYYY-MM-DD
- Approved by: <Solution Designer>
- Supersedes: <ADR-NNN, or none>

## Context

What forced this decision. The constraint, the problem, the trigger. Written so
that someone reading it in a year understands the situation without asking.

## Decision

The decision, stated in one or two sentences, in the active voice.

## Alternatives considered

| Option | Why it lost |
|---|---|

## Consequences

What this makes easy. What this makes hard. What is now locked in.

## Risks

What could make this decision wrong later, and what signal would reveal it.

## Stack map delta

The exact rows this decision changes in `cdad/context/stack.md`, as before/after
pairs. Write `No change to the map` only if that is literally true.

| Section | Row | Before | After |
|---|---|---|---|

Plus the line to append to the map change log:

| YYYY-MM-DD | ADR-NNN | <what changed> |

## Affected context

Which other files under `cdad/context/` this decision changes, and how. The
Solution Designer applies those edits — you do not.
```

## After drafting

An ADR without a stack map delta is incomplete. `cdad/context/stack.md` is the
one artifact everyone reads to understand the system; a decision recorded in an
ADR but absent from the map is invisible in practice.

State plainly which `cdad/context/` files now need updating so the governed
context and the ADR stay consistent. A decision recorded but not reflected in
context is the stale-context failure CDAD exists to prevent.
