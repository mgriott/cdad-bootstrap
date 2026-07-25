@AGENTS.md

## Claude Code specifics

Use these skills instead of improvising the format:

| Situation | Skill |
|---|---|
| "process the change request" | `cdad-propose-change` |
| Architectural or context change needed | `cdad-propose-change` |
| A change was approved and needs recording | `cdad-adr` |
| Verify the governed context still matches the code | `cdad-audit` |

`cdad/context/`, `cdad/adr/` and `cdad/CHANGE-REQUEST.md` are blocked at the
permission layer and by a PreToolUse hook. A denial there is the system working
as designed — write to `cdad/proposals/` instead, and never look for another way
to reach a blocked path.

Hard constraints, always in context:

@cdad/context/constraints.md
