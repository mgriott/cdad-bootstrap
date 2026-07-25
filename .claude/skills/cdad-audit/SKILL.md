---
name: cdad-audit
description: Audit whether the governed context under cdad/context/ still matches the actual codebase. Use when the user asks to check context freshness, verify the docs are still accurate, review architectural drift, or run a CDAD audit — typically before a release, after a large merge, or when onboarding to an unfamiliar repo.
---

# Audit context freshness

Stale context is worse than no context: it makes every agent in the project
confidently wrong. This audit compares what the governed context claims against
what the repository actually does.

## Procedure

1. Read `cdad/context/stack.md` first — it is the densest set of falsifiable
   claims and most drift shows up there.
2. Read `architecture.md`, `principles.md`, `constraints.md`, and
   `solution-vision.md`.
3. Read the accepted ADRs in `cdad/adr/`.
4. Inspect the repository: dependency manifests, folder structure, deployment
   and pipeline definitions, module boundaries and their actual imports.
5. For each claim in the context, classify it.

## Checking the stack map specifically

| Map section | Check against |
|---|---|
| Stack at a glance | dependency manifests, lockfiles, image tags |
| Component map | actual network calls and client instantiations |
| Deployment topology | IaC files, pipeline definitions, or the live environment |
| Observability | actual exporters, collector config, alert rules in the repo |
| Dependency rules | real import graph |
| Map change log | one row per accepted ADR — missing rows mean skipped governance |

Every row in "Stack at a glance" with no ADR in its "Locked by" column is a
finding: a decision that entered the system without passing through governance.

## Classification

| Verdict | Meaning |
|---|---|
| Confirmed | The code matches the claim |
| Drifted | The code contradicts the claim |
| Unverifiable | The claim is too vague to check against code |
| Orphaned | The code does something significant that no context file covers |

Drift and orphans are the findings that matter. `Unverifiable` is a finding too:
it means the context is written in language too soft to govern anything, and it
should be rewritten to be concrete.

## Output

```text
CDAD Context Audit — <date>

Stack map
  <row> — map says X, repository shows Y — evidence: <path:line>
  Rows with no governing ADR: <list>

Drifted
  <file> — claims X, code does Y — evidence: <path:line>

Orphaned
  <what the code does that context never decided> — evidence: <path>

Unverifiable
  <file> — claim is not concrete enough to check

Confirmed
  <count> claims verified

Recommended action
  <per finding: update context, revert code, or open an ADR>
```

Report only. Do not edit `cdad/context/`, do not fix the drift in code, and do
not soften a finding because the code looks reasonable. The Solution Designer
decides whether the context or the implementation is the thing that is wrong.
