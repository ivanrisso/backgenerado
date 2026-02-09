# Hotfix Status - HF-FUNC-RBAC-CLIENTES

**Estado:** CERRADO
**Tipo:** FUNCIONAL
**Fecha:** 2026-02-04
**Responsable:** Antigravity

## Check
- [x] functional_definition.md
- [x] impact_analysis.md
- [x] implementation_plan.md
- [x] e2e_evidence.md (PASS)
- [x] Runtime Verification (Browser)

## Resolución
Se relajó la seguridad en `GET /api/v1/clientes/` para permitir el acceso a cualquier usuario autenticado (`get_current_user`), eliminando la restricción de rol `admin`.
Esto corrige el bloqueo en los filtros de módulos operativos como Tesorería.
