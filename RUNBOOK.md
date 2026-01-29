# Operating Manual — Sistema de Facturación AR (AFIP)

## Cómo se trabaja (AI-First SDLC)
1) Crear REQ: `.artifacts/requests/<REQ-ID>/input.md` (usar `.templates/input_request.md`)
2) Orchestrator ejecuta el master workflow:
   - `.agent/workflows/00_master-facturacion-ar.md`
3) Se generan artifacts por etapa:
   - PRD, ADR, Impact, Delivery, QA, AFIP, Release, Incident
4) No se avanza si gates no pasan:
   - `.agent/checklists/*`

## Reglas fiscales operativas
- No borrar comprobantes emitidos: Nota de Crédito/Débito.
- Emisión CAE idempotente.
- Reconciliar estados ante timeouts.

## Seguridad
- No secretos/certs en repo.
- No PII en logs (mascarar).

## Baseline
REQ-BASELINE es la fuente de verdad del AS-IS.
