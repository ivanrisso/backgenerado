# Definición Funcional - HF-GAP-001 (Imputación Parcial)

## Problema
Actualmente, al crear una Nota de Crédito (NC), el sistema imputa automáticamente el saldo disponible de la factura asociada hasta cubrir el total de la NC. No existe mecanismo para que el usuario (o el sistema llamante) especifique un monto parcial a imputar.

## Solución Propuesta
Modificar la estructura de `cbtes_asociados` en el Payload de creación de comprobante para permitir un campo opcional `importe_imputar`. 

## Comportamiento
1. Si `cbtes_asociados` incluye `importe_imputar` > 0:
   - Se usará este valor como monto de imputación.
   - Se validará que `importe_imputar <= factura.saldo`.
   - Se validará que `importe_imputar <= nc.total`.
2. Si NO se especifica `importe_imputar` (o es 0/null):
   - Se mantiene el comportamiento actual (automático: `min(factura.saldo, nc.saldo)`).

## Alcance
- **Backend**: `ComprobanteFullUseCase`, Schema `CbteAsoc`.
- **Frontend**: Fuera de alcance (se asume uso API).
