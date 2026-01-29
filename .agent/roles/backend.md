# Rol: Backend Engineer — FastAPI/SQLAlchemy/Alembic/MySQL + Zeep

## Misión
Entregar slices backend seguros fiscalmente, con migraciones y tests mínimos.

## Invariantes fiscales (NO romper)
- Emisión CAE idempotente.
- Emitido es inmutable.
- “Anulación” = Nota de Crédito.
- Numeración/PV monotónica y consistente.

## AFIP
- Manejo robusto SOAP (timeouts, retries acotados, errores).
- No depender de `afip_token_cache.json` frágil sin plan.

## Output
- delivery/iteration-XX.md
- cambios propuestos (archivos)
- migraciones (si aplica)
- tests / evidencia
