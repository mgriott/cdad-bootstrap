# Migrating from CDAD v1

## What changed and why

v1 was correct as a methodology and expensive as an implementation. Every file
loaded on every session, whether relevant or not, and the same rules were
restated across four files.

| Problem in v1 | Fix in v2 |
|---|---|
| `AGENTS.md` ordered the agent to read 9 files at session start | Nothing is read at startup; content loads when relevant |
| L0 file list repeated 6 times across 4 files | Stated once, in `.claude/CLAUDE.md` |
| `Proposed Architecture Change` template duplicated in 3 files | One copy, in the `cdad-propose-change` skill |
| L0–L3 table in both `governance.md` and `project-context.md` | One copy, in `cdad/docs/METHODOLOGY.md` |
| 518 lines of methodology vs 263 lines of actual project context | Methodology moved out of the context window entirely |
| L0 protection written as prose the model may ignore | `permissions.deny` plus a PreToolUse hook |

Always-loaded context drops from roughly 826 lines to roughly 80.

## File mapping

| v1 | v2 |
|---|---|
| `cdad/AGENTS.md` | `.claude/CLAUDE.md` (rules) + `cdad/docs/METHODOLOGY.md` (rationale) |
| `cdad/ai-rules.md` | `.claude/CLAUDE.md` + `.claude/skills/cdad-propose-change/` |
| `cdad/governance.md` | `cdad/docs/METHODOLOGY.md` |
| `cdad/guardrails.md` | `.claude/settings.json` + `.claude/rules/` |
| `cdad/project-context.md` | `cdad/docs/METHODOLOGY.md` |
| `cdad/context/*` | unchanged in purpose; trimmed and marked read-only |
| *(new)* | `cdad/context/stack.md` — the visual stack and architecture map |
| *(new)* | `cdad/CHANGE-REQUEST.md` — the single entry point for changes |
| *(new)* | `cdad/proposals/` — agent-writable staging area |
| *(new)* | `INDEX.md` — map of every file |
| `cdad/adr/*` | unchanged; template added |

## Steps

1. Copy `.claude/` (includes `.claude/CLAUDE.md`) and `cdad/` (includes
   `cdad/docs/`) into your project root.
2. Port your real content into the files under `cdad/context/`. Copy from your
   v1 files; the governed content itself did not change.
3. Fill in `cdad/context/stack.md`. This file is new in v2 and has no v1
   equivalent. Set the "Locked by" column to the ADR that made each decision;
   blanks are findings, not omissions.
4. Delete `cdad/AGENTS.md`, `ai-rules.md`, `governance.md`, `guardrails.md`, and
   `project-context.md`.
5. Adjust the `paths:` globs in `.claude/rules/` to match your folder layout.
   They ship with `src/`, `tests/`, `infra/`, `deploy/`.
6. Start a session and run `/context`. Confirm `.claude/CLAUDE.md` appears under
   memory files and that nothing from `cdad/docs/` or `.claude/skills/` is
   loaded.
7. Wire `cdad/scripts/cdad-check-stack.sh` into CI against your default branch.
8. Verify the protection holds: ask the agent to edit
   `cdad/context/architecture.md`. It must be blocked, not merely reluctant.

## If you use other agents too

v2 ships this way already: `AGENTS.md` holds the portable core and
`.claude/CLAUDE.md` imports it. Kiro and Codex read `AGENTS.md` natively, so
they pick up the core with no adapter. See `cdad/docs/PORTABILITY.md` for what
each tool does and does not enforce.

If you only ever use Claude Code, you can inline `AGENTS.md` into
`.claude/CLAUDE.md` and delete it — but the indirection costs nothing and keeps
the door open.

## Verifying the token saving

Run `/context` before and after. The `Memory files` section shows what loaded
and what it costs. If you still see files from `cdad/` other than
`constraints.md`, something is importing more than it should.
