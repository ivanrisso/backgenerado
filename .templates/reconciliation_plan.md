# Plan de Reconciliación AFIP — REQ-XXXX

## Escenarios
- Timeout WSFE
- Retry emisión
- Rechazo WSFE
- Desfase estado local vs AFIP

## Estrategia
- Idempotency key + storage
- Re-consulta comprobante
- Política de retries/backoff acotada
- Estado local y transiciones

## Evidencia
- logs (sin PII)
- métricas/alertas
- casos QA
