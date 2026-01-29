---
description: Preparar entrega con seguridad operativa.. regresión, monitoreo,   runbooks, rollback, controles de seguridad, y checklist de release.
---

---
name: release-hardening
version: 1.0.0
workflow_type: release
domain: facturacion
jurisdiction: AR-AFIP
purpose: >
  Preparar entrega con seguridad operativa: regresión, monitoreo,
  runbooks, rollback, controles de seguridad, y checklist de release.
entrypoint: false
artifacts:
  root: .artifacts/requests
roles:
  qa: { responsibility: regression }
  devops: { responsibility: deploy-rollback }
  security: { responsibility: security-review }
  architect: { responsibility: governance }
  reviewer: { responsibility: gates }
constraints:
  - no_pii_in_logs
---

# Workflow 05 — Release Hardening

## Artifacts
- `release/release_checklist.md`
- `release/runbook.md`
- `release/monitoring.md`
- `release/known_issues.md`
- `release/release_notes.md`

## Gate
Aplicar `.agent/checklists/gate_release.md`.
