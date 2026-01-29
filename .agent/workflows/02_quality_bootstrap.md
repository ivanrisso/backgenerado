---
description: Crear el mínimo de calidad para evolucionar sin romper, tests críticos,smoke FE,contract OpenAPI, disciplina Alembic y base operativa.
---

---
name: quality-bootstrap
version: 1.0.0
workflow_type: quality
domain: facturacion
jurisdiction: AR-AFIP
purpose: >
  Crear el mínimo de calidad para evolucionar sin romper: tests críticos,
  smoke FE, contract OpenAPI, disciplina Alembic y base operativa.
entrypoint: false
artifacts:
  root: .artifacts/requests
roles:
  qa: { responsibility: critical-paths }
  backend: { responsibility: test-scaffold }
  frontend: { responsibility: smoke }
  architect: { responsibility: contract-governance }
  devops: { responsibility: repeatability }
constraints:
  - no_destructive_commands_without_approval
---

# Workflow 02 — Quality Bootstrap (CRÍTICO)

## REQ recomendado
`REQ-QUALITY-BOOTSTRAP`

## Stage A — Critical Paths (QA)
Artifacts:
- `qa/test_plan.md`
- `qa/critical_paths.md`

## Stage B — Backend test scaffold (Backend)
Usar skill: `.agent/skills/test-bootstrap/SKILL.md`
Artifacts:
- `backend/test_scaffold.md`
- `backend/mocking_strategy_afip.md`

## Stage C — OpenAPI contract (Architect + Backend)
Usar skill: `.agent/skills/openapi-contract/SKILL.md`
Artifacts:
- `architecture/openapi_contract.md`

## Stage D — Alembic discipline (Backend + DevOps)
Usar skill: `.agent/skills/alembic-discipline/SKILL.md`
Artifacts:
- `backend/migrations_playbook.md`

## Stage E — Frontend smoke (Frontend)
Artifacts:
- `frontend/smoke.md`

## Gate
Aplicar `.agent/checklists/gate_delivery.md`.