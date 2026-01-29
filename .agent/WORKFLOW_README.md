# Agent Operating System (AOS) — Facturación AR (AFIP)

## Objetivo
Gobernar el proyecto con Antigravity en modo AI-First SDLC:
- Workflows (contratos ejecutables)
- Roles (prompts persistidos)
- Skills (capacidades repetibles)
- Artifacts (evidencia versionable)
- Gates (control de calidad/compliance)

## Principios
1) **Artifacts over chat**: si no está en `.artifacts/requests/<REQ-ID>/...` no existe.
2) **Baseline primero**: REQ-BASELINE es fuente de verdad del AS-IS.
3) **Cambios fiscales/AFIP = ADR obligatorio**.
4) **Idempotencia** en emisión CAE y acciones críticas.
5) **No PII en logs** + auditoría con IDs y referencias.
6) **No destructive commands** sin aprobación explícita.

## Convención de REQ
- Carpeta: `.artifacts/requests/<REQ-ID>/`
- Input mínimo: `input.md`
- Outputs: según workflow (PRD, ADR, delivery, QA, AFIP, release)

## Cómo se usa (operación)
1) Orchestrator lee `.agent/workflows/00_master_facturacion_ar.md`
2) Orchestrator asigna tareas a roles (sub-agentes)
3) Cada rol produce artifacts (paths exactos)
4) Reviewer aplica gates con `.agent/checklists/*`
5) Solo después se proponen cambios de código (PRs/commits)

## Baseline requerido
Debe existir:
- `.artifacts/requests/REQ-BASELINE/current_state.md`
- `.artifacts/requests/REQ-BASELINE/architecture/domain_map.md`
- `.artifacts/requests/REQ-BASELINE/architecture/tech_debt.md`
- `.artifacts/requests/REQ-BASELINE/architecture/risks.md`
