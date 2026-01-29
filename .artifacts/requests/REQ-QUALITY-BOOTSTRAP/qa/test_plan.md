# Test Plan — REQ-QUALITY-BOOTSTRAP

## Estrategia
Cobertura mínima orientada a detección temprana de errores críticos,
no a cobertura exhaustiva.

## Backend
- Framework: pytest
- Tipo: integration tests mínimos
- Mock AFIP: sí (obligatorio)

## Frontend
- Framework: vitest
- Tipo: smoke test

## Criterio de salida
- Todos los tests pasan localmente.
- Evidencia de ejecución documentada.
- Ninguna llamada real a AFIP.
