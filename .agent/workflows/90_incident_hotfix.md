---
description: Gestionar incidentes minimizando riesgo y manteniendo trazabilidad,   especialmente cuando afecta emisión CAE o certificados.
---

---
name: incident-hotfix
version: 1.0.0
workflow_type: incident
domain: facturacion
jurisdiction: AR-AFIP
purpose: >
  Gestionar incidentes minimizando riesgo y manteniendo trazabilidad,
  especialmente cuando afecta emisión CAE o certificados.
entrypoint: false
artifacts:
  root: .artifacts/requests
roles:
  orchestrator: { responsibility: coordination }
  backend: { responsibility: fix }
  devops: { responsibility: mitigation }
  qa: { responsibility: validate }
  security: { responsibility: assess }
constraints:
  - minimum_change
  - reversible_fix_preferred
---

# Workflow 90 — Incident / Hotfix

## Artifacts obligatorios
- `incident/summary.md`
- `incident/timeline.md`
- `incident/mitigation.md`
- `incident/fix.md`
- `incident/validation.md`
- `incident/postmortem.md` (si afecta emisión/CAE o datos fiscales)

## Gate
Aplicar `.agent/checklists/gate_hotfix.md`.
