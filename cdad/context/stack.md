# Stack & Architecture Map

> The single view of this solution. If it is not on this page, it is not part of
> the architecture. Every approved architectural change updates this file in the
> same commit as the ADR that approves it.

- **Last verified:** `YYYY-MM-DD` — run the `cdad-audit` skill to refresh
- **Governing ADRs:** ADR-001

---

## 1. Stack at a glance

One row per layer. If a cell is empty, the decision has not been made — say so
rather than leaving a plausible guess in place.

| Layer | Technology | Version | Locked by |
|---|---|---|---|
| Language | | | |
| Runtime | | | |
| Application framework | | | |
| Compute model | | | |
| Datastore (primary) | | | |
| Datastore (cache) | | | |
| Messaging / events | | | |
| Identity & authz | | | |
| Secrets | | | |
| IaC | | | |
| CI/CD | | | |
| Observability | | | |
| Testing | | | |

"Locked by" points at the ADR that made the decision. A row with no ADR is a
decision nobody made on purpose — treat it as technical debt.

---

## 2. Component map

What talks to what, and over which protocol. Keep it to components that exist;
this is not a roadmap.

```mermaid
flowchart LR
    Client["Client"]

    subgraph Edge["Edge"]
        GW["API Gateway"]
    end

    subgraph App["Application"]
        SvcA["Service A"]
        SvcB["Service B"]
    end

    subgraph Data["Data"]
        DB[("Primary store")]
        Cache[("Cache")]
    end

    Ext["External system"]

    Client -->|HTTPS| GW
    GW -->|HTTP| SvcA
    SvcA -->|async| SvcB
    SvcA --> DB
    SvcA --> Cache
    SvcB -->|HTTPS| Ext
```

Label every edge with its protocol. An unlabelled edge is where paradigm drift
starts: sync and async look identical in a box diagram and behave nothing alike.

---

## 3. Deployment topology

Where each component actually runs, and what the trust boundaries are.

```mermaid
flowchart TB
    subgraph Cloud["Cloud provider — region"]
        subgraph Net["Network boundary"]
            C1["Container / function 1"]
            C2["Container / function 2"]
            DB[("Managed datastore")]
        end
        Registry["Image registry"]
        Secrets["Secret store"]
        Obs["Logs & metrics"]
    end

    CI["CI/CD pipeline"] -->|push image| Registry
    Registry -->|pull| C1
    Registry -->|pull| C2
    C1 --> DB
    C2 --> DB
    C1 -.->|read| Secrets
    C1 -.->|emit| Obs
    C2 -.->|emit| Obs
```

---

## 4. Observability

Where signals come from and where they land. This view answers "if it breaks at
3am, what do I look at" — keep it accurate or it is worse than absent.

```mermaid
flowchart LR
    subgraph Sources["Signal sources"]
        App["Application"]
        Infra["Platform / runtime"]
    end

    subgraph Pipeline["Collection"]
        Agent["Collector / agent"]
    end

    subgraph Sinks["Destinations"]
        Logs[("Logs")]
        Metrics[("Metrics")]
        Traces[("Traces")]
    end

    Alerts["Alerting"]
    Dash["Dashboards"]

    App -->|structured logs| Agent
    App -->|metrics| Agent
    App -->|spans| Agent
    Infra -->|platform logs| Agent
    Agent --> Logs
    Agent --> Metrics
    Agent --> Traces
    Metrics --> Alerts
    Logs --> Dash
    Metrics --> Dash
    Traces --> Dash
```

| Signal | Emitted by | Collected via | Stored in | Retention |
|---|---|---|---|---|
| Logs | | | | |
| Metrics | | | | |
| Traces | | | | |
| Audit events | | | | |

**What is alerted on, and who receives it:**

| Condition | Threshold | Routed to |
|---|---|---|

An observability stack with no row in the alerting table is a dashboard nobody
watches. Record what actually pages someone.

---

## 5. Dependency rules

The boundaries the code must respect. This table is what makes drift
detectable — without it, "Service A calls the database directly" is an opinion.

| Module | May depend on | Must not depend on |
|---|---|---|
| | | |

---

## 6. Map change log

Every row here corresponds to an accepted ADR. If an architectural change
happened without a row, the governance loop was skipped.

| Date | ADR | What changed in this map |
|---|---|---|
| | | |

---
Governance: L0. Read-only for AI agents. Changes require an approved ADR and are
applied by the Solution Designer.
