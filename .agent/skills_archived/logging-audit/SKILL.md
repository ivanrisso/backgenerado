---
name: logging-audit
version: 1.0.0
purpose: >
  Definir logging seguro y auditoría de acciones críticas (emisión/NC),
  sin PII, con correlación y trazabilidad.
constraints:
  - no_pii_in_logs
---

# Logging & Audit Skill
- Definir correlation_id/request_id
- Definir audit trail (actor, acción, timestamp, resultado, ids)
- Definir campos prohibidos (CUIT completo si no hace falta, direcciones, etc.)
