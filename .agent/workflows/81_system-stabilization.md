---
description: Workflow 06 — System Stabilization / Hotfix
---

# Workflow 06 — System Stabilization / Hotfix

## Objetivo
Corregir fallas detectadas por workflows de coverage, calidad o CI,
sin introducir nuevas funcionalidades.

Este workflow se ejecuta SOLO cuando existe evidencia de fallos
documentados en un workflow previo.

---

## REQ recomendado
REQ-SYSTEM-STABILIZATION-001

---

## Stage A — Input Validation

Verificar existencia de:
- `architecture/api_inventory.md`
- `qa/crud_failures.md`
- `ui/orphan_routes.md`

Si no existen → ABORTAR.

---

## Stage B — Backend Hotfixes

Responsable: Backend + Architect

Acciones permitidas:
- Corregir endpoints que devuelven 500.
- Ajustar repositorios para:
  - devolver lista vacía en lugar de excepción.
- Crear seeds mínimos de desarrollo.
- Agregar manejo de errores controlado.
- Ajustar auth inconsistente (JWT / roles).

Acciones prohibidas:
- Cambiar contratos API.
- Introducir lógica fiscal nueva.
- Usar AFIP real.

Artifacts:
- `backend/fixes.md`
- `backend/seeds.md`

---

## Stage C — Frontend Hotfixes

Responsable: Frontend Architect

Acciones permitidas:
- Corregir imports rotos.
- Corregir SVG inválidos.
- Manejar respuestas vacías de backend.
- Ajustar guards de auth.

Artifacts:
- `frontend/fixes.md`

---

## Stage D — Verification

- Re-ejecutar:
  - CRUD checks
  - UI smoke
- Confirmar:
  - No 500
  - No loops de login
  - CRUD core funcional

Artifacts:
- `qa/post_fix_verification.md`

---

## Gate — Stabilization Gate

Checklist:
- Todos los fallos críticos corregidos.
- No regresiones.
- CI verde.

Checklist:
`.agent/checklists/gate_stabilization.md`
