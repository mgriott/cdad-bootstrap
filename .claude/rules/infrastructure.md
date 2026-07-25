---
paths:
  - "infra/**/*"
  - "deploy/**/*"
  - "**/*.bicep"
  - "**/*.tf"
  - "**/Dockerfile"
  - "**/docker-compose*.yml"
  - ".github/workflows/**/*"
---

# Infrastructure and deployment

Infrastructure choices are architectural. Changing the deployment target,
the orchestration model, the IaC tool, or a managed service is an architecture
change, not a config edit.

Read section 3 of `cdad/context/stack.md` (deployment topology) before
proposing anything here. `cdad/context/constraints.md` records which platform
decisions are already locked and why.

Requires a proposal via `cdad-propose-change`, never a direct edit:

- changing the compute model (containers, serverless, VMs, orchestrator)
- adding or replacing a managed service
- introducing or swapping an IaC tool
- changing the network or identity topology
- changing how secrets are stored or injected

Routine work that does not need a proposal: adjusting resource sizing, adding an
environment variable already covered by an accepted decision, fixing a broken
pipeline step, updating an image tag.
