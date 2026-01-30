# QA Evidence - REQ-001 (Pagos)

## Backend Verification
Se ha implementado el módulo de Recibos con tests unitarios e integración simulada.

**Comando:** `poetry run pytest tests/test_recibo.py`
**Resultado:** ✅ PASS
```text
tests/test_recibo.py::test_create_recibo_basic PASSED                                [ 50%]
tests/test_recibo.py::test_create_recibo_with_imputation PASSED                      [100%]
============================== 2 passed, 46 warnings in 0.05s ==============================
```

## Frontend Verification
Se ha creado la vista de creación de recibos y el servicio API.

**Comando:** `vitest src/modules/Tesoreria/ui/views/ReciboCreateView.spec.ts`
**Resultado:** ✅ PASS
```text
 Test Files  1 passed (1)
      Tests  1 passed (1)
```

## Cobertura Funcional
- [x] **Creación de Recibo**: Backend valida y crea Comprobante tipo 'RC'.
- [x] **Imputación**: Se descuenta saldo de factura y se genera registro en tabla Imputacion.
- [x] **Cuenta Corriente**: Se genera movimiento (Haber) en tabla CuentaCorriente.
- [x] **UI**: Formulario permite seleccionar cliente y facturas con deuda.

## Notas
- Se reutilizó la entidad `Comprobante` para Recibos, garantizando compatibilidad con reportes existentes.
- La vista de Cuenta Corriente (`CurrentAccountView`) mostrará los recibos automáticamente al ser `Comprobantes`.
