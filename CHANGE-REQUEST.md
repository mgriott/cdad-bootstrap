# Change Request

**This is the front door. To change anything governed — stack, architecture,
principles, constraints, vision, or product-level design intent — write it here
and nowhere else.**

This file is not a decision log and not a pull request. It is a formal request
for architectural review. The agent may read it, analyze it, and draft a
proposal, but it does not modify the governed context or ADRs directly.

Overwrite the block below each time. This file is a desk, not an archive — the
history lives in `cdad/adr/`.

---

## CDAD Request

```text
Change: <what needs to change in the design or system architecture>
Reason: <why this change is needed>
Trigger: <what event caused the request: bug, cost, limit, requirement, review, etc.>
Scope: <what is included and what is intentionally out of scope>
Impact: <systems, modules, teams, dependencies, adoption cost, migration implications>
Risk: <technical, operational, delivery, and adoption risk>
Priority: <critical / high / medium / low>
```

### Example

```text
Change: Introduce OAuth2-based authentication with multi-tenant SSO support.
Reason: The current system depends on local credentials and does not scale for clients with centralized identity policies.
Trigger: New business requirement and a security audit.
Scope: Changes the authentication flow, the session layer, and provider configuration; does not modify internal domain business logic.
Impact: Affects access services, session management, environment configuration, and the onboarding experience.
Risk: High, due to compatibility with existing users, integration with external providers, and possible migration failures.
Priority: High
```

---

## How to use this

1. Fill in the request block above with the architectural intent.
2. Tell your agent: *"process the change request"*.
3. The agent reads this file and the governed context, then writes a full
   proposal to `cdad/proposals/`.
4. Review the proposal. Reject it, request changes, or approve it.
5. On approval, the agent drafts the ADR and the exact stack map delta. You
   apply both.

If you are only asking a question ("is this even possible?", "what would this
cost us?"), ask in chat instead. This file is for changes you intend to make.

## What does not belong here

Implementation work. Bugs, feature requests, refactors inside existing
boundaries, and anything under `src/` never belongs here — that is L3 and can be
handled directly in implementation.

If you find yourself filling this in for routine work, the constraints in
`cdad/context/` are written too broadly. Narrow them.
