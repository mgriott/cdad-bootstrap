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
CDAD:
Cambio: <what needs to change in the design or system architecture>
Motivo: <why this change is needed>
Trigger: <what event caused the request: bug, cost, limit, requirement, review, etc.>
Alcance: <what is included and what is intentionally out of scope>
Impacto: <systems, modules, teams, dependencies, adoption cost, migration implications>
Riesgo: <technical, operational, delivery, and adoption risk>
Prioridad: <critical / high / medium / low>
```

### Example

```text
CDAD:
Cambio: Introducir autenticación basada en OAuth2 con soporte para SSO multi-tenant.
Motivo: El sistema actual depende de credenciales locales y no escala para clientes con políticas de identidad centralizadas.
Trigger: Nuevo requisito de negocio y auditoría de seguridad.
Alcance: Cambia el flujo de autenticación, la capa de sesión y la configuración de proveedores; no modifica la lógica de negocio de dominios internos.
Impacto: Se afectan los servicios de acceso, la gestión de sesiones, la configuración de entorno y la experiencia de onboarding.
Riesgo: Alto por compatibilidad con usuarios existentes, integración con proveedores externos y fallos de migración.
Prioridad: High
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
