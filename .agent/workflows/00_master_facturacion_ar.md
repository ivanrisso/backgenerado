---
description: Orquestación end-to-end del sistema de facturación electrónica (AFIP)   sobre proyecto existente, usando multiagentes con gates de arquitectura,   fiscalidad, calidad y operación.
---

---
name: master-facturacion-ar
version: 1.0.0
workflow_type: master
domain: facturacion
subdomain: facturacion-electronica
jurisdiction: AR-AFIP
purpose: >
  Orquestación end-to-end del sistema de facturación electrónica (AFIP)
  sobre proyecto existente, usando multiagentes con gates de arquitectura,
  fiscalidad, calidad y operación.
entrypoint: true
artifacts:
  root: .artifacts/requests
  per_request: true
language:
  default: es
  code: en
roles:
  orchestrator: { responsibility: orchestration }
  architect: { responsibility: technical-governance }
  domain_guardian: { responsibility: business-rules }
  fiscal_guardian: { responsibility: afip-compliance }
  implementer: { responsibility: delivery }
  reviewer: { responsibility: quality-gates }
constraints:
  - no_destructive_commands_without_approval
  - fiscal_changes_require_adr
  - idempotent_emission_required
  - no_pii_in_logs
dependencies:
  baseline_required: true
  baseline_id: REQ-BASELINE
---

# Master Workflow — Facturación AR (AFIP)

## Fuente de verdad
- `.artifacts/requests/REQ-BASELINE/current_state.md`
- `.artifacts/requests/REQ-BASELINE/architecture/domain_map.md`
- `.artifacts/requests/REQ-BASELINE/architecture/tech_debt.md`
- `.artifacts/requests/REQ-BASELINE/architecture/risks.md`

## Flujo recomendado (orden)
1) `01_baseline_review.md` (si AOS es nuevo o hay dudas)
2) `02_quality_bootstrap.md` (prioridad inmediata por tests inexistentes)
3) `03_feature_evolution.md` (cada requerimiento)
4) `04_afip_compliance_reconciliation.md` (si toca CAE/WSAA/WSFE/estados/tokens/certs)
5) `05_release_hardening.md` (cada entrega)
6) `90_incident_hotfix.md` (urgencias)

## Definiciones globales (invariantes fiscales)
- “Anulación” operacional se implementa fiscalmente vía **Nota de Crédito**.
- Comprobantes emitidos son **inmutables** (cambios sólo vía NC/ND).
- Numeración y PV: monotónicos y consistentes por tipo.
- Emisión CAE: idempotente, auditable, reconciliable.
