# ADR-001 — Context is the source of truth

- Status: Accepted
- Date: 2026-01-01
- Approved by: Solution Designer
- Supersedes: none
- Amended by: ADR-008 (scope of the write protection)

## Context

AI agents generate implementation faster than humans review it. Without a
governed reference, the codebase becomes the de facto specification, and
architectural intent erodes one reasonable-looking commit at a time. The erosion
is invisible because every individual change is defensible.

## Decision

The governed context under `cdad/context/` is the source of truth for this
project. Generated code is an artifact of that context, never a replacement for
it. Where code and context disagree, the disagreement is escalated to a human
rather than resolved by an agent.

## Alternatives considered

| Option | Why it lost |
|---|---|
| Code as source of truth | Architectural intent is unrecoverable once lost |
| Prose docs with no enforcement | Ignored under delivery pressure; drifts silently |
| Review gates only | Catches drift after it is written, not before |

## Consequences

Makes easy: onboarding agents and humans to architectural intent; detecting
drift as a discrete event rather than a slow slide.

Makes hard: fast unilateral architectural change — deliberately.

Locked in: under the governed regime, `cdad/context/` is write-protected for
agents at the permission and hook layers, not merely by instruction. ADR-008
defines the pre-freeze regime, in which no ratified context yet exists to
protect.

## Risks

The context goes stale and misleads every agent that reads it. Detected by
running the `cdad-audit` skill on a schedule and before releases.

## Affected context

None — this ADR establishes the model itself.
