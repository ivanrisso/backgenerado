# REQ-ID: REQ-QUALITY-IMPLEMENTATION-001 — Implementación del Quality Bootstrap

## Contexto
Existe un REQ cerrado `REQ-QUALITY-BOOTSTRAP` que definió el estándar mínimo de calidad:
tests mínimos, estrategia de mocking AFIP, disciplina Alembic y smoke test FE.

## Objetivo
Implementar en código exactamente lo definido en `REQ-QUALITY-BOOTSTRAP`,
incluyendo instalación de dependencias de test, creación de estructura de tests
y ejecución local con evidencia.

## Alcance
Backend:
- Agregar dependencias dev (pytest, pytest-mock, httpx, opcional pytest-socket).
- Crear estructura `tests/`.
- Implementar tests mínimos definidos en `backend/test_scaffold.md`.
- Implementar mocks AFIP según `backend/mocking_strategy_afip.md`.

Frontend:
- Agregar dev deps (vitest, @vue/test-utils, jsdom).
- Crear smoke test definido en `frontend/smoke.md`.

DB:
- Verificar disciplina Alembic según `backend/migrations_playbook.md` (sin cambios de esquema si no es necesario).

## Fuera de alcance
- Aumentar cobertura más allá del mínimo.
- Refactor general.
- Cambios funcionales o fiscales.

## Criterios de aceptación
- `pytest` corre y pasa localmente.
- `vitest` corre y pasa localmente.
- No hay llamadas a AFIP real en tests.
- Evidencia de ejecución guardada en artifacts.
- Gate Delivery PASS.
