---
name: test-bootstrap
version: 1.0.0
stack:
  backend: fastapi
  frontend: vue
purpose: >
  Instalar base mínima de tests: pytest/httpx (mock AFIP) y vitest (smoke).
constraints:
  - no_direct_afip_calls_in_tests
  - request_approval_for_commands
---

# Test Bootstrap Skill

## Backend (FastAPI)
- Agregar pytest + httpx
- Definir fixtures para app/db (según estructura existente)
- Mock AFIP (wsaa/wsfe) para evitar llamadas reales
- Crear 1-3 tests críticos (health + emisión/estado si existen endpoints)

## Frontend (Vue)
- Agregar vitest + @vue/test-utils
- 1 test smoke de ruta/store/componente crítico

## Output
- Documento con comandos y resultados
- Lista de tests creados y qué cubren
