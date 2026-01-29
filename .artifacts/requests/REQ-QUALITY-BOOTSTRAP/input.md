# REQ-ID: REQ-QUALITY-BOOTSTRAP — Bootstrap de Calidad Técnica

## Contexto
El sistema de facturación AR (AFIP) carece de tests automatizados, gates de calidad
y disciplina mínima de contratos y migraciones. Dado que se trata de un sistema
fiscal crítico (emisión de comprobantes con CAE), esta situación representa un
riesgo alto de regresiones y fallas de compliance ante cualquier cambio.

## Objetivo
Instalar un **mínimo viable de calidad técnica** que permita evolucionar el sistema
de forma segura, sin reescrituras ni refactors masivos.

## Alcance
- Backend: base mínima de tests (pytest) y estrategia de mocking AFIP.
- Frontend: smoke test mínimo.
- Contratos: verificación de OpenAPI como contrato FE/BE.
- Base de datos: disciplina Alembic documentada.
- Evidencia reproducible de ejecución.

## Fuera de alcance
- Refactor de arquitectura.
- Aumento de cobertura más allá del mínimo crítico.
- Cambios funcionales o fiscales.
- Integración real con AFIP en tests.

## Riesgos
- Falsa sensación de seguridad si se excede el alcance mínimo.
- Subestimar paths fiscales críticos (mitigado con QA critical paths).

## Criterio de aceptación
- Existen tests mínimos ejecutables con comandos documentados.
- No se realizan llamadas reales a AFIP en tests.
- OpenAPI tiene fuente de verdad definida.
- Alembic tiene un playbook claro y reproducible.
- Todos los artifacts están versionados.
