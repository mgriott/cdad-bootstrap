---
inclusion: fileMatch
fileMatchPattern: 'infra/**/*'
---

# Infrastructure and deployment

Mirror of `.claude/rules/infrastructure.md` for Kiro.

Infrastructure choices are architectural. Changing the deployment target, the
orchestration model, the IaC tool, or a managed service is an architecture
change, not a config edit.

Read section 3 of `cdad/context/stack.md` (deployment topology) before proposing
anything here.

Requires a proposal, never a direct edit: compute model, managed services, IaC
tooling, network or identity topology, secret storage.

Routine and allowed: resource sizing, environment variables already covered by
an accepted decision, fixing a broken pipeline step, image tag updates.
