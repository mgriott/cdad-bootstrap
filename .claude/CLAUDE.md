@../AGENTS.md

## Claude Code specifics

Use these skills instead of improvising the format:

| Situation | Skill |
|---|---|
| First time populating `cdad/context/`, or `cdad/context/` still holds template placeholders | `cdad-bootstrap` |
| "process the change request" | `cdad-propose-change` |
| Architectural or context change needed | `cdad-propose-change` |
| A change was approved and needs recording | `cdad-adr` |
| Verify the governed context still matches the code | `cdad-audit` |

`cdad/context/`, `cdad/adr/`, `CHANGE-REQUEST.md`, and `SOURCE-BRIEF.*` are
blocked at the permission layer and by a PreToolUse hook. A denial there is
the system working as designed — write to `cdad/proposals/` instead, and
never look for another way to reach a blocked path.

Hard constraints, always in context:

@../cdad/context/constraints.md
