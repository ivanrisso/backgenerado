# PRD — REQ-QUALITY-BOOTSTRAP

## Resumen
Este PRD define el bootstrap de calidad técnica para habilitar un SDLC seguro
en un sistema de facturación electrónica con AFIP.

## Usuarios / Roles
- Developers (Backend / Frontend)
- QA
- Arquitectura
- DevOps

## Problema
Actualmente no existen tests automatizados ni gates de calidad, lo que impide
detectar regresiones en paths fiscales críticos.

## Solución propuesta
Introducir un set mínimo de tests, contratos y disciplina operativa,
sin alterar el comportamiento del sistema.

## Alcance
- Tests mínimos BE/FE.
- Verificación de contratos OpenAPI.
- Disciplina Alembic documentada.

## Métricas de éxito
- Tests ejecutan en < 1 min localmente.
- Al menos 1 test cubre un path crítico.
- No se rompen features existentes.

## Riesgos y supuestos
- Supuesto: el código permite inyección de mocks.
- Riesgo: dependencias AFIP difíciles de aislar (mitigado con stubs).
