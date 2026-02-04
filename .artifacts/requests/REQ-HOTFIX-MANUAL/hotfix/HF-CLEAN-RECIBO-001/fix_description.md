# HF-CLEAN-RECIBO-001 — Inicialización incompleta de ReciboService

## Problema
El constructor de `ReciboService` requiere un argumento adicional
`cliente_repo`, el cual no está siendo inyectado en los tests ni en
la inicialización del servicio.

## Impacto
- Falla el pipeline de CI
- Tests de recibos no ejecutan
- Bloqueo total de entrega

## Causa probable
Cambio reciente en la firma del constructor sin actualización
de factories y tests asociados.

## Criterio de corrección
- El constructor debe recibir correctamente `cliente_repo`
- Los tests deben instanciar el servicio sin errores
- El CI debe pasar en verde
