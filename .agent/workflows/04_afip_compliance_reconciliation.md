---
description: Asegurar consistencia local vs AFIP, idempotencia, retries acotados,   re-consulta, auditoría y continuidad operativa (certs/tokens).
---

---
name: afip-compliance-reconciliation
version: 1.0.0
workflow_type: compliance
domain: facturacion
jurisdiction: AR-AFIP
purpose: >
  Asegurar consistencia local vs AFIP: idempotencia, retries acotados,
  re-consulta, auditoría y continuidad operativa (certs/tokens).
entrypoint: false
artifacts:
  root: .artifacts/requests
roles:
  fiscal_guardian: { responsibility: compliance }
  architect: { responsibility: design }
  backend: { responsibility: implementation }
  qa: { responsibility: scenarios }
  devops: { responsibility: ops }
constraints:
  - retries_must_be_bounded
  - reconciliation_required_on_timeouts
  - no_direct_afip_calls_in_tests
---

# Workflow 04 — AFIP Compliance & Reconciliation

## Artifacts obligatorios
- `afip/integration_plan.md`
- `afip/reconciliation_plan.md`
- `afip/error_catalog.md`
- `afip/observability.md`
- `afip/credentials_ops.md`

## Contenido mínimo exigido
- Idempotency key + storage/locking (documentado y/o implementado)
- Política de retries/backoff y circuit breaker (al menos como ADR/plan)
- Re-consulta de estado en caso de timeout / respuesta incierta
- Auditoría de emisión/anulación fiscal (IDs, timestamps, usuario, resultado)
- Operación certs/tokens: expiración, rotación, secretos, alertas

## Gate
Aplicar `.agent/checklists/gate_afip.md`.
