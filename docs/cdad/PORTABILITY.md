# Portability: Claude Code, Kiro, Codex

CDAD v2 separates **content** from **mechanism**. The governed context under
`cdad/` is plain markdown and is fully portable. What differs per tool is how
that content is loaded and how the L0 protection is enforced.

Nothing in `cdad/` needs to change to move between tools. Only the adapter does.

## Compatibility matrix

| Capability | Claude Code | Kiro | Codex |
|---|---|---|---|
| Always-loaded instructions | `CLAUDE.md` | `AGENTS.md`, or steering `inclusion: always` | `AGENTS.md` |
| Reads `AGENTS.md` natively | no — imports it | yes | yes |
| Path-scoped rules | `.claude/rules/` + `paths:` | `.kiro/steering/` + `inclusion: fileMatch` | nested `AGENTS.md` only |
| On-demand procedures | Skills | steering `inclusion: manual` / `auto` | prompt or custom command |
| Declarative file-write blocking | `permissions.deny` | not equivalent | `[permissions.*.filesystem]` globs |
| Programmatic pre-tool block | PreToolUse hook | agent hooks (different model) | hooks / sandbox |
| Governed context in `cdad/` | works | works | works |
| CI gate (`scripts/`) | works | works | works |

**Short version:** Claude Code runs everything. Kiro runs everything except the
deterministic write block, which it approximates. Codex runs the content and the
write block, but loses conditional loading — its instruction file is
all-or-nothing.

## Claude Code

Native target. `CLAUDE.md` imports `AGENTS.md` and adds the Claude-specific
layer: skill routing and a note that permission denials are by design.

Verify with `/context`: only `CLAUDE.md`, `AGENTS.md`, and `constraints.md`
should appear under memory files.

## Kiro

Kiro reads `AGENTS.md` from the workspace root automatically, so the portable
core loads with no adapter at all. Note that `AGENTS.md` in Kiro does not
support inclusion modes — it is always included.

The path-scoped rules are mirrored in `.kiro/steering/` using
`inclusion: fileMatch` with a `fileMatchPattern`. Kiro accepts one pattern per
file, so a rule covering several globs becomes several steering files.

What Kiro does not have is an equivalent of `permissions.deny`. The L0
protection degrades to instruction only. Two workarounds, in order of strength:

1. Make `cdad/context/` read-only on disk: `chmod -R a-w cdad/context`. Crude,
   tool-independent, and effective — the write fails at the filesystem.
2. Rely on the CI gate. `scripts/cdad-check-stack.sh` plus a branch rule
   requiring review on `cdad/**` catches what reaches a pull request.

Known issue: global steering in `~/.kiro/steering/` has had reports of
`fileMatch` not triggering. Keep CDAD steering in the workspace, not global.

## Codex

Codex reads `AGENTS.md` from the global config directory, the project root, and
nested directories, with more local files taking priority. The portable core
loads with no adapter.

Two adjustments matter:

**Conditional loading does not exist.** Codex has no `paths:` equivalent. The
closest approximation is nested `AGENTS.md` files that apply when Codex works in
that subtree:

```
AGENTS.md              # portable core
src/AGENTS.md          # implementation rules
infra/AGENTS.md        # infrastructure rules
```

This is coarser than path globs but preserves the principle: rules load near the
code they govern rather than all at once.

**Size cap.** Codex caps project docs at `project_doc_max_bytes`, 32 KiB by
default. CDAD v2's core is far under that. CDAD v1 was not obviously safe.

**Write protection** is available through filesystem permission globs in
`~/.codex/config.toml`:

```toml
[permissions.cdad.filesystem]
"cdad/context/**" = "deny"
"cdad/adr/**" = "deny"
```

Combine with `sandbox_mode` and `writable_roots` for a harder boundary. Verify
against the current Codex config reference — this surface has been changing
quickly.

## If you use all three

Keep `AGENTS.md` as the single source for the core rules. Never restate a rule
in `CLAUDE.md` that already lives in `AGENTS.md` — that duplication is exactly
the defect v2 was built to remove.

The two path-scoped rule files are the one place duplication is unavoidable,
since `.claude/rules/` and `.kiro/steering/` use incompatible front matter. They
are short and change rarely. If you only use one tool, delete the other
directory rather than maintaining both.
