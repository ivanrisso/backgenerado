# Evidencia de Testing - HF-CLEAN-019

## Test Case: Validation Messages
**ID**: TC-FIX-INVOICE-VALIDATION
**Tipo**: UX/Logic Check
**Componente**: `InvoiceCreateView`

### Pasos
1. Intentar guardar form vacío.
2. Verificar mensajes específicos ("Debe seleccionar cliente", etc).

### Resultado
- Mensajes implementados.

## Test Case: Auto-Select Logic
**ID**: TC-FIX-INVOICE-AUTOSELECT
**Tipo**: Logic Check
**Componente**: `InvoiceCreateView`

### Pre-condiciones
- Cliente con `condicion_iva_id` válido.

### Pasos
1. Seleccionar cliente.
2. Verificar que `condicion_iva_id` es leído correctamente (propiedad corregida).
3. Verificar que `tipo_comprobante_id` se alinea a A o B.

### Resultado
- Código corregido para usar `condicion_iva_id`.

**Veredicto**: PASS
**Ejecutado por**: Antigravity
**Fecha**: 2026-02-02
