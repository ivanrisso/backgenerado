# PRD — REQ-CI-BOOTSTRAP-001

## Resumen
Agregar CI mínimo para validar backend y frontend mediante tests automatizados.

## Fuente de verdad
- `REQ-QUALITY-IMPLEMENTATION-001`
- Tests existentes en backend y frontend.

## Pipeline esperado
- Trigger: pull_request, push.
- Job backend:
  - setup Python
  - install deps
  - pytest
- Job frontend:
  - setup Node
  - install deps
  - vitest

## Done
- Pipeline definido.
- Pipeline verde.
- Evidencia registrada.
