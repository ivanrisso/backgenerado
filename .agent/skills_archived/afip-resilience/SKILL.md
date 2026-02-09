---
name: afip-resilience
version: 1.0.0
purpose: >
  Establecer resiliencia WSAA/WSFE: retries acotados, timeouts,
  circuit breaker (al menos documentado) y reconciliación.
constraints:
  - retries_must_be_bounded
  - reconciliation_required_on_timeouts
---

# AFIP Resilience Skill
- Catalogar fallas SOAP típicas
- Definir retries/backoff y timeouts
- Definir estados transitorios (PENDIENTE_CONFIRMACION) si aplica
- Definir re-consulta para resolver ambigüedad
