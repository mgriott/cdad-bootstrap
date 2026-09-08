# ADR-009 — Drift detection and remediation loop

- Status: Accepted
- Date: 2026-09-08
- Approved by: Solution Designer
- Supersedes: none
- Depends on: ADR-008 — this loop operates only under the governed regime

## Context

The control plane protects paths, not decisions.

`cdad/context/` and `cdad/adr/` are denied, so an agent cannot rewrite what was
ratified. But L3 — `src/`, `tests/`, `infra/` — is free by design, and a change
there can contradict L0 without touching any denied path. The database engine is
decided in `stack.md` and locked by an ADR; changing it in practice means
editing `docker-compose.yml`, a dependency manifest and a migration. None of
those is denied. The change lands in silence and the map starts lying.

This is post-freeze architectural drift: the failure CDAD exists to prevent,
entering through the door that was left open on purpose.

A second problem compounds it. Drift detection already existed in one form —
the `cdad-audit` skill, a full sweep run on demand — and the v3 roadmap
proposed an Analyst role that would "audit drift" as well. Adding a third,
reactive mechanism would leave three definitions of drift ageing separately.
That is the duplication defect v2 was built to remove.

## Decision

**One engine, two triggers.**

A single machine-readable block, `cdad-drift-signals`, is declared inside
`cdad/context/stack.md`. It names the paths that carry architectural weight
despite sitting outside the governed tree. Being inside `stack.md` means it is
L0: only the human edits it. An agent able to narrow that block could switch off
its own surveillance.

A single skill, `cdad-drift-response`, is the only path from a detected
divergence to a draft. It assesses, classifies the change as fast track or full
track, writes a proposal to `cdad/proposals/`, and emits the ratification
commands without running them.

Two triggers feed it:

1. **Write-time.** A `PostToolUse` hook, `detect-drift.py`, compares each write
   against the signals block and warns through stderr, which returns the signal
   to the model in the same turn. It never blocks — L3 is free by design, and
   stopping a legitimate edit mid-flow would make CDAD an obstacle. The write
   happens; what is triggered is the conversation about whether the map is still
   true. Deduplicated per session, so a category warns once per session rather
   than once in the lifetime of the repository.
2. **Sweep.** `cdad-audit` is subordinated to the same loop. It reads the same
   signals block, sweeps every matching file rather than one, keeps its existing
   checks of each map view against manifests and the real import graph, and on
   finding a divergence invokes `cdad-drift-response` instead of drafting in its
   own format.

The detector is not a fifth plane. It lives in the control plane — a
deterministic hook, zero tokens — but its output is advisory. It extends the
reach of the control plane from paths to decisions without making L3 governed
territory.

The asymmetry is untouched. The agent writes to `proposals/`, which is an
assertion; the human promotes to `adr/`, which is a ratified fact. What is
accelerated is the drafting, not the signature.

## Alternatives considered

| Option | Why it lost |
|---|---|
| A `PreToolUse` hook that blocks writes to architecture-bearing paths | Makes L3 governed by the back door. Every legitimate infrastructure edit becomes a change request, which is precisely the friction that makes people work around governance rather than through it. |
| Leave `cdad-audit` as an independent mechanism alongside the new loop | Two definitions of drift, two output formats, ageing separately. The reactive one would drift from the sweep one, and neither would be trusted. |
| Detect drift only in the build plane, by extending `cdad-check-stack.sh` | CI runs on demand and often only against ADR diffs. A project whose CI never runs this script gets no signal at all. The hook fires at the moment a human is actually watching agent output. |
| Warn the human directly rather than the agent | `exit 2` on `PostToolUse` returns stderr to the model, which can raise the proposal in the same turn. Routing to the human adds a hop and loses the turn. |
| Keep the signals list in a dedicated file outside `stack.md` | It would sit outside L0 unless separately denied, and a separate deny is a second rule to keep in sync. Inside `stack.md` it is already protected, and it belongs next to the dependency rules it extends. |
| Include `Bash` in the hook matcher | Bash `tool_input` is a command string, not a path; mapping it to files means parsing shell. Accepted gap: shell mutations of L3 are not detected, and the build plane is the net for that case. This differs from `protect-l0.py`, which does scan Bash, because there a false positive is cheap and a bypass is not. |

## Consequences

Makes easy: noticing that a ratified decision has been overtaken by
implementation, at the moment it happens rather than at the next audit; keeping
one format for every drift proposal regardless of how it was found.

Makes hard: nothing in day-to-day L3 work. The loop is silent unless a declared
signal is touched, and silent again for the rest of the session once it has
spoken.

Locked in: `cdad-audit` is no longer an independent mechanism. Any future drift
capability — including the Analyst role planned for v3 — reads the findings of
this loop rather than defining drift again.

## Risks

**The signals block goes stale or is never filled in.** A `stack.md` without it
leaves the detector blind and nobody notices. `cdad-check-stack.sh` warns when
the block is absent under the governed regime. It is a warning rather than a
failure on purpose: making it fail immediately would break the build of every
already-frozen project at the moment of upgrade, with nobody having changed
anything. It becomes a hard failure in a later version, once the warning has had
time to be seen.

**Alert fatigue.** Signals written too broadly turn every infrastructure edit
into a warning, and warnings that always fire are warnings nobody reads. Per
session deduplication limits the volume; the real control is keeping the globs
narrow. If the loop is firing on routine work, the signals are written too
broadly — narrow them, rather than disabling the hook.

**Shell mutations are invisible.** Accepted and documented above. The build
plane covers it.

**Session-scoped deduplication depends on the harness supplying a session
identifier.** Where it does not, all writes fall into one bucket and the
category warns once until the temporary file is cleared.

## Affected context

`cdad/context/stack.md` — gains the `Drift signals` view, holding the
`cdad-drift-signals` block, appended to the dependency rules section.
