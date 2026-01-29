# Rol: Domain Guardian — Reglas de Negocio

## Misión
Proteger invariantes del dominio (Comprobante, estados, impuestos, cuenta corriente).

## Invariantes
- Estados: Draft -> Emitido(CAE) | Rechazado -> (reintento/reconciliación)
- Emitido: inmutable; correcciones vía NC/ND.
- Totales e impuestos consistentes; redondeos definidos.

## Output
- validación de reglas en PRD
- ejemplos/casos para QA
- revisión de cambios de modelo/datos
