---
description: Entregar features por slices verticales con PRD, ADR, evidencia y no-regresión.
---

---
name: feature-evolution
version: 1.0.0
workflow_type: feature
domain: facturacion
jurisdiction: AR-AFIP
purpose: >
  Entregar features por slices verticales con PRD, ADR, evidencia y no-regresión.
entrypoint: false
artifacts:
  root: .artifacts/requests
roles:
  product_owner: { responsibility: prd }
  domain_guardian: { responsibility: business-rules }
  architect: { responsibility: adr-impact }
  backend: { responsibility: delivery }
  frontend: { responsibility: delivery }
  qa: { responsibility: validation }
  security: { responsibility: controls }
  reviewer: { responsibility: gates }
constraints:
  - fiscal_changes_require_adr
  - idempotent_emission_required
---

# Workflow 03 — Feature Evolution (Facturación AR)

## Stage 1 — PRD (PO + Domain Guardian)
Artifacts:
- `prd.md`
- `user_stories.md`
- `reglas_fiscales_ar.md` (si aplica)
Gate: `gate_prd.md`

## Stage 2 — Impact + ADR (Architect + Security + DevOps)
Artifacts:
- `impact_analysis.md`
- `architecture/adrs/ADR-<REQ-ID>.md`
- `architecture/security_controls.md`
Gate: `gate_architecture.md`

## Stage 3 — Delivery (Backend + Frontend)
Artifacts:
- `delivery/iteration-01.md` (y N si hace falta)
- `delivery/change_log.md` (qué cambió y por qué)
Gate: `gate_delivery.md`

## Stage 4 — QA (QA)
Artifacts:
- `qa/test_plan.md` (si cambia)
- `qa/evidencia.md`
Gate: `gate_delivery.md`

## Regla AFIP
Si el REQ toca CAE/WSAA/WSFE/estados/tokens/certs/errores SOAP:
- ejecutar `04_afip_compliance_reconciliation.md` y pasar `gate_afip.md`.
