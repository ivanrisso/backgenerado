# Evidencia E2E - HF-CLEAN-019

## Flujo Verificado
**Facturación - Alta de Comprobante**

### Pasos
1. Ingreso a "Nueva Factura".
2. Selección de Cliente.
3. Verificación de Auto-selección de Tipo de Comprobante (basado en Condición Tributaria).
4. Completado de Items.
5. Guardado exitoso.

### Resultados
- Mensajes de validación específicos implementados.
- Lógica de auto-selección corregida (`condicion_iva_id`).
- Interfaz `CondicionTributaria` actualizada.

**Estado**: PASS
**Fecha**: 2026-02-02
