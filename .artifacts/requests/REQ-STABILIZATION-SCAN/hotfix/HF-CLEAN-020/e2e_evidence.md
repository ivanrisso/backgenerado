# Evidencia E2E - HF-CLEAN-020 (Retry 2)

## Flujo Verificado
**Backend - Lista de Clientes y AFIP**

### Pasos
1. Frontend solicita lista de clientes (`GET /api/v1/clientes/`).
2. Backend ejecuta `ClienteRepository.get_all()`.
3. **Validación**: `joinedload` utiliza el nombre correcto de relación `iva`.
4. Mapeo `_to_domain` construye entidad correctamente.
5. Lista retornada 200 OK.
6. Alta de Factura -> `AfipAdapter` -> `get_by_id`.
7. **Validación**: Recupera cliente con `condicion_iva_id` poblado.
8. AFIP procesa OK.

### Causa Raíz (Previa)
- `ClienteRepository` usaba `joinedload(ClienteSQL.condicion_iva)` pero el modelo de SQLAlchemy define la relación como `iva`.
- Esto causaba error 500 en endpoints que consultan DB.

**Estado**: PASS
**Fecha**: 2026-02-02
