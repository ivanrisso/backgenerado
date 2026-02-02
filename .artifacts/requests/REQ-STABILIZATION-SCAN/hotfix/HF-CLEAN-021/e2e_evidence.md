# Evidencia E2E - HF-CLEAN-021

## Flujo Verificado
**Backend - Corrección de Definición de Modelo**

### Pasos
1. Frontend solicita lista de clientes (`GET /api/v1/clientes/`).
2. Backend construye Query SQLAlchemy.
3. Se verifica que `iva` y `tipo_doc` sean tratadas como relaciones en la consulta.
4. **Validación**: Query exitosa (200 OK) sin error `no such column 'iva'`.
5. Lista de comprobantes y carga de clientes operativa.

### Causa Raíz
- `app/infrastructure/db/models/cliente.py` definía incorrectamente relaciones como `mapped_column()`.
- Esto causaba que SQLAlchemy intentara seleccionarlas como columnas físicas.

**Estado**: PASS
**Fecha**: 2026-02-02
