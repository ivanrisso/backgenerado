---
description: Validar y completar el AS-IS del proyecto existente para operar con AOS,   sin modificar código. Establece baseline de riesgos y controles mínimos.
---

---
name: baseline-review
version: 1.0.0
workflow_type: retrofit
domain: facturacion
jurisdiction: AR-AFIP
purpose: >
  Validar y completar el AS-IS del proyecto existente para operar con AOS,
  sin modificar código. Establece baseline de riesgos y controles mínimos.
entrypoint: false
artifacts:
  root: .artifacts/requests
roles:
  architect: { responsibility: baseline-owner }
  backend: { responsibility: inventory }
  frontend: { responsibility: inventory }
  qa: { responsibility: risk-to-tests }
  security: { responsibility: controls }
  devops: { responsibility: operability }
constraints:
  - no_code_changes
---

# Workflow 01 — Baseline Review

## Inputs
- Baseline REQ-BASELINE (archivos mencionados en master)

## Outputs (si faltan, crearlos en REQ-BASELINE)
- `.artifacts/requests/REQ-BASELINE/architecture/observability.md`
- `.artifacts/requests/REQ-BASELINE/architecture/security_controls.md`
- `.artifacts/requests/REQ-BASELINE/blocking_issues.md` (si falta evidencia)

## Gate
Aplicar `.agent/checklists/gate_baseline.md`.
