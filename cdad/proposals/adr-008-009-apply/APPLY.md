# Apply ADR-008 + ADR-009

Everything an agent is permitted to write directly (hooks-adjacent scripts,
skills, `AGENTS.md`, `.kiro/permissions.yaml`, `.kiro/hooks/detect-drift.json`,
`README.md`, `cdad/docs/DOCS.md`) is already applied on the working tree.

What's staged here is exactly what the permission layer blocks an agent from
touching directly: `.claude/hooks/**`, `.claude/settings.json`, `cdad/adr/**`,
`cdad/context/stack.md`. Review each file below, then run the commands.

## 1. Review

- `hooks/protect-l0.py` → replaces `.claude/hooks/protect-l0.py`
- `hooks/detect-drift.py` → new `.claude/hooks/detect-drift.py`
- `settings.json` → replaces `.claude/settings.json`. Diff highlights:
  - Removes `cdad/context/**`, `cdad/adr/**`, `SOURCE-BRIEF.*` from
    `permissions.deny` (now regime-conditional, hook-only — a static file
    cannot express "unless `cdad/.frozen` exists").
  - Adds `AGENTS.md`, `.claude/settings.local.json`, `.claude/rules/**`,
    `.kiro/settings|steering|hooks/**`, `.kiro/permissions.yaml`,
    `cdad/.frozen` to `permissions.deny` (previously-open machinery gap).
  - Adds `MultiEdit` to the `PreToolUse` matcher (pre-existing gap,
    independent of the regime change — call it out separately in the commit).
  - Registers a new `PostToolUse` hook for `detect-drift.py`.
- `adr/ADR-001-context-governance.md` → amends the "Locked in" consequence to
  be regime-scoped, adds `Amended by: ADR-008` to the header.
- `adr/ADR-008-two-regime-governance.md` → new.
- `adr/ADR-009-drift-detection-loop.md` → new.
- `context/stack.md` → adds `ADR-008`/`ADR-009` to "Governing ADRs", appends
  the `Drift signals` view (with an example `cdad-drift-signals` block — adjust
  the globs to this project's real stack once it has one), adds the two
  change-log rows. Everything else in the file is untouched template
  placeholder text, as it was before this change.

## 2. Apply

```bash
cp cdad/proposals/adr-008-009-apply/hooks/protect-l0.py .claude/hooks/protect-l0.py
cp cdad/proposals/adr-008-009-apply/hooks/detect-drift.py .claude/hooks/detect-drift.py
cp cdad/proposals/adr-008-009-apply/settings.json .claude/settings.json
cp cdad/proposals/adr-008-009-apply/adr/ADR-001-context-governance.md cdad/adr/ADR-001-context-governance.md
cp cdad/proposals/adr-008-009-apply/adr/ADR-008-two-regime-governance.md cdad/adr/ADR-008-two-regime-governance.md
cp cdad/proposals/adr-008-009-apply/adr/ADR-009-drift-detection-loop.md cdad/adr/ADR-009-drift-detection-loop.md
cp cdad/proposals/adr-008-009-apply/context/stack.md cdad/context/stack.md
chmod +x .claude/hooks/protect-l0.py .claude/hooks/detect-drift.py cdad/scripts/cdad-freeze.sh cdad/scripts/cdad-check-stack.sh
rm -rf cdad/proposals/adr-008-009-apply
```

## 3. Verify (Part A — regimes)

Run these in a scratch clone or branch, not against the real bootstrap of this
repo — `cdad/context/` here is still template text, so these are true
pre-freeze tests as-is.

| # | Test | Expected |
|---|---|---|
| 1 | No marker, template context: agent edits `cdad/context/stack.md` | Allowed, no warning |
| 2 | Agent edits `AGENTS.md`, `.claude/settings.json`, or `.claude/hooks/*` | Blocked, in every regime |
| 3 | Agent runs `echo x > cdad/.frozen` or any shell mutator on that path | Blocked |
| 4 | Populate `cdad/context/` with real content, no marker, edit again | Allowed **with the A.3 warning** |
| 5 | Invoke `cdad-bootstrap` in that same state | Stops at step 0, migration-case row |
| 6 | Run `cdad-freeze.sh` | Marker written, `cdad/proposals/bootstrap/` removed if present |
| 7 | Repeat test 1 post-freeze | Now blocked |
| 8 | Run `cdad-freeze.sh` again | Exit 2, does not rewrite it |
| 9 | `cdad-check-stack.sh` with no marker | Exit 0 immediately |
| 10 | Cite `ADR-042` in `stack.md`, run the check post-freeze | FAIL — referential integrity |

## 4. Verify (Part B — drift loop)

| # | Test | Expected |
|---|---|---|
| 1 | No marker, edit `infra/main.tf` | Silence — detector does not run pre-freeze |
| 2 | With marker, edit `docker-compose.yml` | `CDAD DRIFT SIGNAL`, category `paths`, same turn |
| 3 | Repeat that edit in the same session | Silence |
| 4 | **Repeat it in a new session** | Warns again. If still silent, dedup is not keying on `session_id` |
| 5 | Edit `src/utils/format.ts` | Silence — not a declared signal |
| 6 | Edit `package.json` | Warns, category `manifests` |
| 7 | Try to edit `cdad/context/stack.md` post-freeze | Blocked by `protect-l0.py`; detector never runs |
| 8 | Remove the signals block, run the check post-freeze | WARNING, exit 0 — not FAIL |
| 9 | Ask the agent to promote a proposal itself | Refuses, hands back the command |
| 10 | Run `cdad-audit` on a repo with a real divergence | Reports it and invokes `cdad-drift-response`; does not draft on its own |

Test 4 is the one that validates the actual fix (session-scoped dedup, not a
repo-lifetime file). If it fails, everything else works and the detector goes
silent forever after first use.

## 5. Commit

Suggested, as two commits (Part A, then Part B — B depends on A's marker
convention, don't squash them):

```
ADR-008: two-regime bootstrap governance

Splits L0 enforcement into pre-freeze and governed regimes, keyed on
cdad/.frozen. Closes the moment-zero blocker where a fresh clone was left
non-functional pending a manual copy.

Also closes, independently: AGENTS.md, .claude/rules/ and CHANGE-REQUEST.md
were absent from permissions.deny, and MultiEdit was absent from the hook
matcher. Neither is part of the regime change.
```

```
ADR-009: drift detection and remediation loop

Extends the control plane from paths to decisions: a PostToolUse hook watches
the drift-signals block declared in L0 and warns when an L3 write may have made
ratified context stale. Advisory, never blocking.

Subordinates cdad-audit to the same loop: one signals block, one response
skill, two triggers (write-time and sweep). Prevents three parallel definitions
of drift from diverging.
```

## Note — two corrections made to the source design

**`protect-l0.py`'s Bash coarse-match regex was broken and has been fixed
here.** The source document's `ALWAYS_PROTECTED`/`GOVERNED` patterns anchor on
`(^|/)` — a boundary that only matches at the start of a string or right after
a slash. For `file_path`-style targets that's fine, but for `Bash` commands the
whole command string is checked as one blob (e.g. `echo x > cdad/.frozen`),
and the protected path there is preceded by a space or `>`, not `/` — so the
anchor never matched and every shell-mutation case silently passed. This is a
real regression against the *currently live* `protect-l0.py`, whose
`MUTATING_SHELL` regex does catch that case a different way. Verified with a
17-case test harness run against both the old and fixed regex — 16/17 passed
before the fix (the `cdad/.frozen` shell-mutation case failed), 17/17 after.
The staged `hooks/protect-l0.py` here already has the fix: the boundary is
`(?:^|[/\\\s>;&|])` instead of `(^|/)`.

**`cdad-freeze.sh`'s placeholder check didn't actually mirror
`protect-l0.py`'s, despite the comment saying it does.** The bash regex was
missing the generic `<...>` bracket pattern the Python `PLACEHOLDER` regex has
(it only had `<rellenar>`, a leftover Spanish token in an English-only repo).
Confirmed against this repo's own still-templated `cdad/context/` — before the
fix, freezing would have wrongly passed `architecture.md`, `principles.md` and
`constraints.md` even though they're all angle-bracket placeholder text.
Already fixed in the applied `cdad/scripts/cdad-freeze.sh` on the working tree
(not staged — that file wasn't blocked).

## Note — one correction made to the source design

`AGENTS.md` rule 3 (already applied on the working tree) treats
`CHANGE-REQUEST.md` as **always** read-only, in both regimes — not
regime-conditional. The staged `protect-l0.py` and `settings.json` agree:
`CHANGE-REQUEST.md` is in `ALWAYS_PROTECTED`, never in the regime-conditional
`GOVERNED` set, and `.kiro/permissions.yaml` denies it unconditionally too.
The source change document's own A.7 wording briefly implied `CHANGE-REQUEST.md`
was regime-conditional like the other three paths; that reading was dropped in
favor of matching the actual hook and permissions code, since the Solution
Designer's own request desk should never become agent-writable pre-freeze
either.
