# Análisis de Impacto - HF-GAP-001

## Componentes Afectados
1. **Schema**: `app/schemas/comprobante.py` (CbteAsoc).
   - Agregar campo opcional `importe_imputar`.
2. **Use Case**: `app/use_cases/comprobante_full_use_case.py`.
   - Modificar lógica de cálculo de `monto_imputar`.
   - Agregar validaciones de tope.

## Riesgos
- **Integridad de Saldos**: Si se imputa más de lo debido, el saldo de la factura podría quedar negativo (Validación requerida).
- **Retrocompatibilidad**: Los clientes actuales que no envían el campo deben seguir funcionando igual (Default logic).

## Estrategia de Mitigación
- Tests unitarios extensivos cubriendo casos:
  - Sin importe (Auto).
  - Con importe parcial válido.
  - Con importe excesivo (Error).
