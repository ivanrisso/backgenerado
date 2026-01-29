# AFIP Integration Plan — REQ-XXXX

## Alcance AFIP
WSAA / WSFE

## Tokens
- origen
- cache seguro (no archivo frágil)
- expiración/refresh
- concurrencia/locking

## Emisión CAE (WSFE)
- request mapping
- manejo de respuesta
- persistencia (atomicidad)
- idempotencia

## Errores SOAP
- clasificación retryable / non-retryable
- timeouts
- bounded retries

## Auditoría
- campos auditables
- masking PII
