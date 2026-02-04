# Plan de Implementación - HF-GAP-001

## Objetivo
Habilitar la imputación parcial de Notas de Crédito mediante un campo opcional en la API.

## Cambios Propuestos

### Backend

#### [MODIFY] [app/schemas/comprobante.py](file:///home/irisso/proyectos/facturacion/app/schemas/comprobante.py)
- Agregar `importe_imputar: float = 0` al modelo `CbteAsoc`. 

#### [MODIFY] [app/use_cases/comprobante_full_use_case.py](file:///home/irisso/proyectos/facturacion/app/use_cases/comprobante_full_use_case.py)
- En el bucle de procesamiento de `cbtes_asociados`:
  - Leer `assoc.importe_imputar`.
  - Si es mayor a 0:
    - Validar `importe_imputar <= invoice.saldo`.
    - Validar `importe_imputar <= saldo_disponible_nc`.
    - Usar `importe_imputar` como monto.
  - Si es 0 o None:
    - Usar lógica actual (`min(invoice.saldo, saldo_disponible_nc)`).

## Plan de Verificación

### Automated Tests
 crear `qa/cases/HF-GAP-001.md` con los siguientes casos:
1. **Caso Base**: Sin importe explícito -> Comportamiento actual (Total).
2. **Caso Parcial**: Importe explícito válido -> Imputa solo ese monto.
3. **Caso Exceso**: Importe > Saldo Factura -> Error.
4. **Caso Exceso NC**: Importe > Total NC -> Error.

### Ejecución
Script `repro_hf_gap_001.py` para validar los 4 casos.
