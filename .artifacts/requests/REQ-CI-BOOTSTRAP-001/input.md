# REQ-ID: REQ-CI-BOOTSTRAP-001 — CI mínimo (Backend + Frontend)

## Contexto
El proyecto ya cuenta con una base de testing funcional:
- Pytest en backend con mocks AFIP.
- Vitest en frontend con smoke test.

Estos tests se ejecutan localmente, pero aún no están integrados
en un pipeline de Integración Continua (CI).

## Objetivo
Incorporar un pipeline de CI mínimo que ejecute automáticamente
los tests de backend y frontend en cada Pull Request.

## Alcance
- Backend: ejecutar pytest.
- Frontend: ejecutar vitest.
- Ejecutar en cada PR y push a branches principales.
- Fallar el pipeline si algún test falla.

## Fuera de alcance
- Deploy.
- Publicación de artefactos.
- Escaneo de seguridad.
- Pruebas E2E o de performance.

## Restricciones
- No usar credenciales reales.
- No permitir llamadas externas (AFIP).
- No modificar lógica productiva.

## Criterios de aceptación
- Pipeline CI definido en el repo.
- CI corre automáticamente.
- Tests backend y frontend pasan.
- Evidencia de ejecución guardada como artifact del REQ.
