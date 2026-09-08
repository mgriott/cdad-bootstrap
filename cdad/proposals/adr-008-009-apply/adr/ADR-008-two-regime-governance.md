# ADR-008 — Two regimes: pre-freeze and governed

- Status: Accepted
- Date: 2026-09-08
- Approved by: Solution Designer
- Supersedes: none
- Amends: ADR-001 (scope of the L0 write protection)

## Context

ADR-001 established `cdad/context/` as write-protected for agents at the
permission and hook layers. That protection was written as a single,
unconditional regime, and implemented as one: a static `permissions.deny` list
plus a stateless PreToolUse hook.

It is correct once a project is governed. It is wrong at the moment a project
is created, when those six files are template placeholders and there is nothing
ratified to protect. The observed result: the `cdad-bootstrap` skill drafts the
completed context into `cdad/proposals/bootstrap/`, leaves `cdad/context/`
untouched, and hands the Solution Designer a `cp` command to run by hand. Every
fresh clone is non-functional until a manual step that is easy to skip and easy
to get wrong.

The gate was not doing its job here. It was applying a governed-operation rule
to a moment with nothing to govern.

## Decision

Enforcement is split into two regimes, discriminated by the presence of the
file `cdad/.frozen`.

| Regime | Condition | `cdad/context/`, `cdad/adr/`, `SOURCE-BRIEF.*` |
|---|---|---|
| Pre-freeze | marker absent | writable by the agent |
| Governed | marker present | denied |

Two rules hold in both regimes, without exception:

1. Governance machinery — `AGENTS.md`, `.claude/rules/`,
   `.claude/settings.json`, `.claude/hooks/`, `CHANGE-REQUEST.md`, `.kiro/`
   configuration, and `cdad/.frozen` itself — is denied to the agent at all
   times. An agent never drafts its own directives.
2. The agent never creates, edits or deletes `cdad/.frozen`. Freezing is a
   human act, performed by `cdad/scripts/cdad-freeze.sh`, which validates that
   L0 holds non-placeholder content before writing the marker.

Because a static configuration file cannot express a condition on filesystem
state, `cdad/context/**` and `cdad/adr/**` move out of `permissions.deny` and
rely on the state-aware hook alone. Machinery paths keep both layers: they have
no regime exception, so the redundancy still earns its place there.

The marker is versioned, not ignored, so that cloning a frozen project keeps it
frozen.

## Alternatives considered

| Option | Why it lost |
|---|---|
| Keep the status quo: stage to `cdad/proposals/bootstrap/`, human runs `cp` | This is the defect being fixed. Leaves every fresh clone non-functional pending a manual step. |
| Special-case the `cdad-bootstrap` skill with a narrower permission profile active only while it runs | `permissions.deny` is static and cannot be scoped to "while skill X runs". Would need the same hook-level state check anyway, keyed on something less durable and less inspectable than a marker file. Also does nothing for iterative context refinement between bootstrap and first freeze. |
| Drop `permissions.deny` entirely, enforce everything through the hook | Removes the one place where double-layer redundancy is unambiguously correct. Machinery paths have no regime exception, so the static layer costs nothing and catches hook bugs and bypasses on the most sensitive paths. |
| Keep the marker at `.cdad/.frozen`, outside the governed tree | Two root directories distinguished only by a leading dot, both appearing in every permission glob. Silent failure mode. The marker needs to be denied to the agent, not located outside `cdad/`; an explicit deny rule achieves that. |

## Consequences

Makes easy: bootstrapping a working project in one pass; iterating on context
before ratifying it; a design stage that has somewhere to run at all — the
pre-freeze regime is the precondition for any agent-assisted design work.

Makes hard: nothing that was previously easy. The governed regime behaves
exactly as before.

Locked in: freezing becomes a discrete, verified act rather than a file move.
`cdad-freeze.sh` refuses to ratify placeholder content, which means the marker
carries a real guarantee and not just a timestamp.

## Risks

**A previously governed project silently reopens on upgrade.** A project
bootstrapped before this ADR has populated context and no marker, which reads
as pre-freeze — so L0 becomes agent-writable again. Three independent surfaces
catch it: a migration note in `README.md` at upgrade time, a four-row state
table in `cdad-bootstrap` step 0 at skill-invocation time, and a hook-level
warning at the moment of the first write. The residual case is a project that
upgrades, never invokes the skill, and edits `cdad/context/` directly; the hook
warning is what covers it.

**Reduced defence in depth on governed paths.** They now rely on the hook
alone. This is logically necessary rather than a trade-off: the redundancy
being removed is exactly the redundancy that could never have expressed a
state-conditional rule. Detected by a hook test asserting deny under
`frozen=True` for both paths, independent of manual verification.

**On Kiro, the conditional rule cannot be declared.** `permissions.yaml` covers
the unconditional machinery paths; the governed paths fall back to the shared
hook plus the build plane.

## Affected context

None — this ADR changes the governance model itself, not the application stack.
