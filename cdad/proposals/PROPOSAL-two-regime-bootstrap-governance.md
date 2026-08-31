# Proposed Architecture Change

**Source:** `CDAD-CHANGE-two-regime-bootstrap.md` (Solution Designer's own
design document, dropped at the project root in place of the
`CHANGE-REQUEST.md` block — read and processed as the change request; see
note at the end on where it should end up).

## Current decision

ADR-001 established that `cdad/context/` (and, by extension, `cdad/adr/`) is
"write-protected for agents at the permission and hook layer, not merely by
instruction" — a single, unconditional regime. The current implementation
enforces that with two static, always-on layers:

- `.claude/settings.json` → `permissions.deny` blocks `Write`/`Edit` on
  `/cdad/context/**`, `/cdad/adr/**`, `/CHANGE-REQUEST.md`, `/SOURCE-BRIEF.*`,
  plus the machinery paths (`.claude/settings.json`, `.claude/hooks/**`).
- `.claude/hooks/protect-l0.py` → a `PreToolUse` hook that closes the shell
  workaround gap (`sed -i`, `tee`, `mv`, redirection, etc.) for the same set
  of paths, using a single `ALWAYS_PROTECTED` regex with no state check.

Because this regime is unconditional, it also applies at the moment a project
has just cloned the kit and `cdad/context/` is still six files of angle-bracket
placeholders. The `cdad-bootstrap` skill (`.claude/skills/cdad-bootstrap/SKILL.md`
step 5) works around this today by drafting the six completed files to
`cdad/proposals/bootstrap/` and handing the Solution Designer a `cp` command to
run by hand — the project is left non-functional (context still placeholders)
until that manual step happens.

## Suggested change

Split enforcement into two regimes, discriminated by a marker on disk
(`.cdad/.frozen`):

| Regime | Condition | `cdad/context/`, `cdad/adr/`, `SOURCE-BRIEF.*` |
|---|---|---|
| Pre-freeze | `.cdad/.frozen` absent | writable by the agent |
| Governed | `.cdad/.frozen` present | deny, as today |

Two rules hold in both regimes, unconditionally:

1. Governance machinery (`AGENTS.md`, `.claude/rules/`, `.claude/settings.json`,
   `.claude/hooks/`, `CHANGE-REQUEST.md`, `.cdad/`) stays denied to the agent
   at all times. The agent never drafts its own directives.
2. The agent can never create, edit, or delete `.cdad/.frozen` itself. Freeze
   is exclusively a human act (`cdad/scripts/cdad-freeze.sh`, run by the
   Solution Designer).

Concretely, this moves:

- **`cdad/context/**` and `cdad/adr/**` enforcement out of the static
  `permissions.deny`** and entirely into the hook, which is state-aware and can
  check `.cdad/.frozen`. Machinery paths stay double-enforced (deny +
  hook) — that rule has no exceptions, so the redundancy is still earning its
  keep there.
- **`cdad-bootstrap` skill step 5** from "stage to `cdad/proposals/bootstrap/`,
  hand the Solution Designer a `cp` command" to "write the six files directly
  to `cdad/context/`, write `SOURCE-BRIEF.md` to the root, write `ADR-001` if
  missing, then stop and tell the Solution Designer to run
  `cdad-freeze.sh` to ratify." **Step 0's gate also needs to be reconciled**
  against the new regime marker — see "Recommended corrections" below; the
  source document didn't specify this and it's the part most likely to be
  gotten wrong by whoever applies the diff literally.
- Adds `.cdad/` (tracked, not gitignored, so a clone of an already-frozen
  project stays governed) and `cdad/scripts/cdad-freeze.sh` — a human-run
  script that validates the six L0 files are non-placeholder and non-empty,
  confirms `ADR-001` exists, then writes the marker.
- `cdad/scripts/cdad-check-stack.sh` gets an early exit when unfrozen (no
  changelog to audit yet) and a new referential-integrity check: every
  `ADR-NNN` cited in `stack.md`'s change log must exist under `cdad/adr/`.
- `AGENTS.md` gets a short "Regime" section as the portable fallback for
  Kiro/Codex, where the Claude Code hook doesn't run.

Full file-by-file diffs are in the source document, with the corrections below
applied on top before anything is merged.

## Reason

The bootstrap-time block is not a case where the gate is doing its job — it's
the gate applying a governed-operation rule (`cdad/context/` is read-only) to
a moment when there is nothing yet to govern. The result today is a kit that
requires a manual `cp` before a fresh clone is usable, and that manual step is
easy to skip or get wrong. The fix is to make the regime itself
state-conditional instead of adding another special case to the instruction
layer.

## Recommended corrections to the source document

These are not new ideas layered on top of the design — the two-regime model
itself is sound and is adopted as-is. These are gaps found by reading the
*current* files the source document proposes to replace and by pressure-testing
the one risk (see "Risk") that the source document didn't surface: an
already-governed project silently reopening on upgrade. Applying the source
document's diffs verbatim, without these five corrections, would ship that
risk unmitigated and reintroduce two small regressions.

**1. Preserve the hook's deny-reason contract.** The current
`protect-l0.py` returns `{"hookSpecificOutput": {"permissionDecision": "deny",
"permissionDecisionReason": ...}}` on stdout before exiting 2 — that's almost
certainly what Claude Code reads to surface the reason to the agent/user,
not stderr. The source document's replacement hook only writes to stderr. The
new hook must emit the same `hookSpecificOutput` JSON shape for every `deny()`
call (machinery, governed, and the new warning case below), or every denial
in the new hook silently gets worse UX than the one it replaces.

**2. Reconcile `cdad-bootstrap` step 0 against the regime marker — the
concrete fix for the migration risk.** Step 0 today asks one question ("does
`cdad/context/` already have real content?"). The regime marker adds a second,
independent one ("does `.cdad/.frozen` exist?"). Cross them explicitly instead
of bolting the new check on loosely:

| Context has real content? | `.cdad/.frozen` exists? | Action |
|---|---|---|
| No | No | Normal case. Proceed with bootstrap. |
| No | Yes | Anomaly — `cdad-freeze.sh` validates non-placeholder content before writing the marker, so this shouldn't happen. Stop, report the inconsistency, do not guess which is right. |
| Yes | Yes | Normal governed state. Offer `cdad-audit` instead (current behavior, unchanged). |
| Yes | No | **The migration risk case.** A project that has populated context but no freeze marker — most likely one bootstrapped under the old single-regime model, upgraded to this change, and hasn't frozen yet. Stop, same as the row above, but say specifically: *"Context is populated but `.cdad/.frozen` is absent — if this project was already governed before this update, run `cdad-freeze.sh` now rather than treating this as a fresh bootstrap."* Do not offer to overwrite it as a bootstrap target. |

This turns the silent-reopening risk into a message the Solution Designer
actually sees, at the one moment it matters — when an agent is about to touch
`cdad/context/` in a project that looks like it shouldn't be pre-freeze.

**3. Back the same check with a hook-level warning, not just the skill.** The
skill-level check above only fires if `cdad-bootstrap` is invoked. An agent
editing `cdad/context/stack.md` directly (not through the skill) in a
populated-but-unfrozen project hits no such warning under the source
document's hook — it just silently succeeds, because pre-freeze means
writable, full stop. Add one more condition to `protect-l0.py`'s pre-freeze
path: before allowing a write under `cdad/context/`, run the same
non-placeholder heuristic `cdad-freeze.sh` already implements (file exists,
>5 lines, no `TODO|PLACEHOLDER|<rellenar>|REPLACE ME`). If it looks populated,
allow the write (pre-freeze still means writable — this is not a new deny) but
emit a warning through the same `hookSpecificOutput` channel:
`"cdad/context/ looks already populated but .cdad/.frozen is absent — if this
project was previously governed, run cdad-freeze.sh before continuing."` A CI
script only catches this on the next `cdad-check-stack.sh` run against an ADR
change; the hook catches it at the point of the actual edit, which is where a
Solution Designer reviewing agent output will actually see it.

**4. Match the existing file conventions instead of silently changing them.**
Current `settings.json` uses leading-slash patterns (`/cdad/context/**`) and a
matcher of `Write|Edit|NotebookEdit|Bash` — no `MultiEdit`. The source
document's replacement drops the leading slash and adds `MultiEdit`. Keep the
leading-slash convention (no functional difference, just consistency with
every other entry staying in the file). Adding `MultiEdit` to the matcher,
however, is a real pre-existing gap independent of this change — `MultiEdit`
already mutates files today and isn't currently gated by the hook's matcher.
Take the fix, but call it out as a separate, piggy-backed bug fix in the
commit/PR description so it doesn't get attributed to the regime change if
someone later asks "why did this file's matcher change."

**5. Drop §3.8's "minimal" Kiro option as written; §5 does not apply here.**
`.kiro/` in this repo has no `permissions.yaml` — only `.kiro/steering/*.md`.
The source document's "minimal" option assumes narrowing an existing deny
list; here one has to be authored from scratch (`.cdad/`, `AGENTS.md`,
`CHANGE-REQUEST.md`, `.kiro/settings/`, `.kiro/steering/` in deny). Treat that
as new file creation, not a patch. Separately, §5 (promoting `ADR-002..007`
from `proposals/` to `adr/`) doesn't apply to this repo's current state —
`cdad/proposals/` contains only `README.md`. Drop that step for this
application; it appears to describe a different checkout.

## Impact

**Files changed:**
- `.cdad/.gitkeep` (new — creates the tracked, ungitignored directory)
- `.claude/hooks/protect-l0.py` (rewritten — regime-aware, plus the
  populated-but-unfrozen warning from correction 3)
- `.claude/settings.json` (governed paths removed from static deny; `MultiEdit`
  added to the hook matcher as a piggy-backed fix — correction 4)
- `cdad/scripts/cdad-freeze.sh` (new)
- `cdad/scripts/cdad-check-stack.sh` (two additions: pre-freeze early exit,
  ADR referential-integrity check)
- `AGENTS.md` (new "Regime" section)
- `.claude/skills/cdad-bootstrap/SKILL.md` (step 5 rewritten; step 0 rewritten
  to the four-row table in correction 2)
- `.kiro/permissions.yaml` (new file, not a patch — correction 5)
- `README.md` (new short "Upgrading" note — see Migration below)
- `cdad/context/stack.md` (change-log row for the new ADR — see resolution
  below)
- New ADR (see below)

**Systems/modules touched:** the governance/permission layer that every
downstream project inherits by cloning this starter kit — this is a change to
the kit's own machinery, not to an application built with it. `cdad/context/`
in *this* repo is still template placeholders (only `ADR-001` governs it),
which is correct — the kit itself has no application stack to describe.

**Resolved: the `stack.md` change-log row.** ADR-001 itself hit the same
situation — a decision about the governance model, not about an application
stack — and its "Affected context" field reads: *"None — this ADR establishes
the model itself."* Follow that precedent: the new ADR's "Affected context"
says the same, and the change-log row records the ADR number and date with
"What changed in this map: none — governance-model change, no stack row
applies," rather than a fabricated stack entry. This keeps the rule
("every approved architectural change updates `stack.md`") satisfied by
recording *that* the ADR was considered against the map, without inventing
content that isn't there.

**Migration note (new — addresses the risk below at the point of upgrade,
not just at the point of use).** Add a short paragraph to `README.md`, next to
wherever the kit's own update/upgrade instructions live: *"If you're pulling
this change into a project that was bootstrapped before it existed, run
`./cdad/scripts/cdad-freeze.sh` immediately after upgrading if `cdad/context/`
already has real content. Until you do, that content is agent-writable again."*
This is a second, independent line of defense on top of corrections 2 and 3 —
one at upgrade time, two at first-write time — rather than relying on any
single one of them being noticed.

**Drift from the source document's assumptions**, folded into corrections 1–5
above rather than repeated here.

## Risk

- **Backward compatibility on upgrade, technical — mitigated by corrections 2,
  3 and the migration note.** Three independent surfaces now catch it: the
  README migration note at upgrade time, the `cdad-bootstrap` step-0 table at
  skill-invocation time, and the hook-level warning at edit time. Residual
  risk is a project that upgrades, never invokes `cdad-bootstrap`, and edits
  `cdad/context/` through raw `Write`/`Edit` rather than the skill — the hook
  warning (correction 3) is what catches that case; without it, only the
  README note (easy to miss) would.
- **Reduced defense-in-depth, technical.** `cdad/context/` and `cdad/adr/`
  lose the static `permissions.deny` layer and rely on the hook alone.
  Machinery paths are unaffected (still both layers). Mitigation: this is
  logically necessary, not optional — a static, stateless config file cannot
  express a condition on filesystem state, so the redundancy being removed
  here is exactly the redundancy that couldn't have worked for a
  state-conditional rule in the first place (§2 of the source document's own
  reasoning). Detected by: a hook unit test asserting deny under `frozen=True`
  for both paths, independent of the manual verification checklist below.
- **Skill gate ambiguity, technical — resolved by correction 2's table**,
  which is the concrete fix; no longer an open risk once applied.
- **Delivery/adoption.** Five files gate every write permission in every
  downstream project. Apply in the order below and run the full verification
  checklist before merging — do not merge on the strength of code review
  alone, this is exactly the kind of change where the diff can look correct
  and the runtime behavior still be wrong.

## Alternatives considered

| Option | Why it loses |
|---|---|
| Keep the status quo: `cdad-bootstrap` stages to `cdad/proposals/bootstrap/` and a human runs `cp` | This is the problem being fixed — leaves every fresh clone non-functional until a manual step that's easy to forget or get wrong. |
| Special-case only the `cdad-bootstrap` skill (e.g., a distinct, narrower settings profile active only during that skill) rather than introducing a filesystem regime marker | `permissions.json` is static and can't be scoped to "while skill X is running"; would need the same hook-level state check anyway, just keyed on something less durable and less inspectable than a marker file. Also doesn't help iterative context refinement between bootstrap and first freeze — only the initial run. |
| Drop `permissions.deny` entirely and enforce everything through the hook, including machinery paths | Removes the one place where double-layer redundancy is unambiguously correct — machinery paths have no regime exception, so the static layer costs nothing and catches hook bugs/bypasses for the most sensitive paths. |
| Catch the migration risk only via a CI script (e.g., extend `cdad-check-stack.sh` to warn if unfrozen-but-populated) instead of the hook-level warning in correction 3 | CI only runs on demand (e.g., against an ADR diff) — a project that upgrades and never triggers CI, or whose CI doesn't run this script on every push, gets no signal at all. The hook runs on every actual write attempt, which is the one moment a human is likely to be watching agent output. |

## Affected files

See "Impact" above for the full list. The source document
(`CDAD-CHANGE-two-regime-bootstrap.md`) contains ready-to-apply diffs for the
core mechanism (marker, hook skeleton, freeze script, check-stack additions);
apply corrections 1–5 on top before merging, and add the two net-new files
(`.kiro/permissions.yaml`, the `README.md` migration note) the source
document didn't include.

## Verification checklist (expanded)

The source document's four checks, plus the cases the corrections above
specifically add:

1. Unfrozen, empty context: agent edits `cdad/context/stack.md` → **allowed**,
   no warning (nothing looks populated yet).
2. Agent edits `AGENTS.md`, `.claude/settings.json`, or `.claude/hooks/`, in
   either regime → **blocked**, `hookSpecificOutput` reason present.
3. Agent runs `echo x > .cdad/.frozen` or any shell mutator targeting `.cdad/`
   → **blocked**, in either regime.
4. Populate `cdad/context/` with real content (no `.cdad/.frozen`), then have
   the agent edit `cdad/context/stack.md` again directly → **allowed, with the
   correction-3 warning present** in the hook output.
5. Invoke `cdad-bootstrap` in that same populated-but-unfrozen state →
   **stops at step 0** with the correction-2 message, does not offer to
   overwrite as a fresh bootstrap.
6. Run `cdad-freeze.sh` → marker written, `cdad/proposals/bootstrap/` removed
   if present.
7. Repeat check 1 post-freeze → **now blocked**, same reason format as check 2.
8. `cdad-check-stack.sh` against a base ref with no `.cdad/.frozen` → exits 0
   immediately (pre-freeze early exit), does not attempt the changelog/ADR
   integrity check.

---

*Housekeeping, not part of the decision:* the source document
`CDAD-CHANGE-two-regime-bootstrap.md` currently sits at the project root
outside the normal `CHANGE-REQUEST.md → proposal` flow. It's yours, not
governed, and not something I'll move or delete unasked — flagging only so
the loop closes visibly: once this proposal is decided, you may want to fold
its content into `CHANGE-REQUEST.md`'s block for the record, or just delete it
since its content now lives here.

Status: Requires Architect approval
