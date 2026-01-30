# REQ-ID: REQ-002 — Listado de clientes con saldo deudor

## Contexto
El sistema de facturación requiere contar con una vista consolidada que permita identificar de forma clara y confiable a los clientes que mantienen **saldos deudores** en su cuenta corriente.  
Actualmente, la información de comprobantes, pagos y notas se encuentra distribuida, lo que dificulta el análisis rápido del estado financiero de los clientes y la toma de decisiones operativas (cobranza, seguimiento).

## Objetivo
Proveer un **listado consultable de clientes con saldo deudor**, calculado en base a los movimientos registrados en el sistema, que permita:
- Identificar clientes con deuda vigente.
- Visualizar el monto total adeudado.
- Facilitar acciones de seguimiento y cobranza.

## Alcance
Incluye:
- Cálculo del **saldo deudor** por cliente.
- Listado ordenable y filtrable de clientes con saldo > 0.
- Visualización de datos básicos del cliente:
  - Identificador / código
  - Razón social / nombre
  - CUIT / documento
  - Saldo total deudor
- Fecha de cálculo del saldo.
- Posibilidad de filtrar por:
  - Rango de saldo
  - Cliente
  - Estado (activo / inactivo)

## Fuera de alcance
- Gestión de cobranzas o pagos.
- Envío de notificaciones automáticas.
- Cálculo de intereses, punitorios o recargos.
- Conciliación bancaria automática.
- Exportaciones contables avanzadas (asientos, reportes fiscales).

## Reglas de negocio
- El **saldo deudor** se calcula como:  
  **Total de comprobantes emitidos – pagos imputados – notas de crédito aplicadas**.
- Solo se listan clientes cuyo saldo final sea **mayor a cero**.
- Los clientes inactivos pueden ser incluidos o excluidos según filtro.
- El cálculo del saldo debe ser **determinístico e idempotente** para una misma fecha de corte.
- Movimientos anulados, rechazados o inválidos no deben considerarse en el cálculo.

## Si aplica: AFIP / fiscalidad
- Los comprobantes considerados deben ser **comprobantes fiscales válidos** (facturas, notas de débito/crédito).
- Las notas de crédito deben estar correctamente asociadas a comprobantes originales.
- No se realiza validación online con AFIP; se trabaja sobre información previamente registrada en el sistema.

## Criterios de aceptación
- Dado un cliente con facturas impagas, el sistema muestra su saldo deudor correcto.
- Un cliente con saldo cero o acreedor **no aparece** en el listado.
- El listado refleja correctamente la suma de comprobantes, pagos y notas.
- El usuario puede ordenar el listado por saldo deudor (ascendente y descendente).
- El tiempo de respuesta del listado es aceptable para volúmenes medios y altos de clientes.
- La fecha/hora de cálculo del saldo es visible o accesible desde la vista.

## Riesgos / supuestos
- Se asume que los datos de pagos y comprobantes están correctamente imputados.
- Errores históricos de carga pueden impactar en el saldo mostrado.
- El rendimiento puede verse afectado si no existe una estrategia adecuada de agregación o cache.
- Se asume un único esquema de moneda, o que los saldos ya estén normalizados.

## Notas técnicas (si hay)
- Se recomienda resolver el cálculo mediante:
  - Vista materializada o query agregada por cliente, o
  - Servicio de dominio de **Cuenta Corriente**.
- Considerar indexación por `cliente_id` y fechas de emisión.
- Definir explícitamente la **fecha de corte** del cálculo.
- En escenarios multi-moneda, definir conversión previa o excluir del alcance.
