# Change Request

**This is the front door. To change anything governed — stack, architecture,
principles, constraints, vision — write it here and nowhere else.**

Keep it short. You are stating intent, not writing the decision. The agent turns
this into a full proposal; you approve it; then it becomes an ADR and the map is
updated.

Overwrite the block below each time. This file is a desk, not an archive — the
history lives in `cdad/adr/`.

---

## Request

**What I want to change:**


**Why:**


**What made this come up:**
<!-- a bug, a cost, a limit hit, a new requirement, a review comment -->


**How urgent:**
<!-- blocking work now / next sprint / just thinking out loud -->


---

## How to use this

1. Fill in the block above. Four lines is enough.
2. Tell your agent: *"process the change request"*.
3. The agent reads this file plus the governed context, and writes a full
   proposal to `cdad/proposals/`. It does not touch `cdad/context/` or
   `cdad/adr/` — those stay yours.
4. Read the proposal. Reject it, send it back, or approve it.
5. On approval, the agent drafts the ADR and the exact stack map delta. You
   apply both.

If you are only asking a question ("is this even possible?", "what would this
cost us?"), just ask in chat. This file is for changes you intend to make.

## What does not belong here

Implementation work. Bugs, features, refactors inside existing boundaries, and
anything under `src/` never touches this file — that is L3 and the agent can
just do it.

If you find yourself filling this in for routine work, the constraints in
`cdad/context/` are written too broadly. Narrow them.
