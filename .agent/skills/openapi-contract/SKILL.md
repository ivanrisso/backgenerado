---
name: openapi-contract
version: 1.0.0
purpose: >
  Verificar gobierno de contrato OpenAPI: sincronía entre FastAPI y openapi.yaml,
  y definir estrategia de generación/validación.
constraints:
  - request_approval_for_commands
---

# OpenAPI Contract Skill
- Determinar si `openapi.yaml` es manual o generado
- Proponer: generar desde FastAPI en CI y compararlo (diff)
- Documentar endpoints críticos (facturación/emisión)
