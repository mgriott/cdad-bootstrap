# Constraints

## Technical Constraints

TODO: Define known technical constraints.

Examples:

- Programming language
- Framework
- Runtime
- Database
- Cloud provider
- Deployment platform
- Security requirements
- Compliance requirements

## Business Constraints

TODO: Define business constraints.

Examples:

- Budget
- Timeline
- Operational limitations
- Existing contracts
- Legacy dependencies

## Architectural Constraints

TODO: Define architectural constraints.

Examples:

- Must remain modular.
- Must use REST APIs.
- Must avoid direct database access from UI.
- Must preserve current domain boundaries.
- Must not introduce async messaging without approval.

## Cloud and Infrastructure Constraints

TODO: Define cloud and infrastructure constraints.

Examples:

- Must use AWS / Azure / GCP.
- Must use Terraform.
- Must deploy to Kubernetes.
- Must remain serverless.
- Must not introduce managed services without approval.
- Must follow security baseline.

## AI Constraints

AI must not:

- Change the project paradigm without approval.
- Add major dependencies without approval.
- Replace architectural patterns without approval.
- Modify L0 context files directly.
- Replace cloud provider or infrastructure approach without approval.

## CDAD Rule

Constraints are binding. AI may propose changes, but must not silently remove or bypass constraints.
