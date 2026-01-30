# PRD — REQ-001 Pagos / Recibos / Cuenta Corriente

---

## Resumen

Este requerimiento incorpora la **gestión de pagos mediante Recibos**, permitiendo imputar pagos a facturas y administrar la **Cuenta Corriente de clientes**. El objetivo es reflejar correctamente la situación financiera (deuda, pagos parciales, anticipos y saldos a favor) **sin alterar la fiscalidad AFIP**, que continúa determinada exclusivamente por la emisión de facturas.

---

## Usuarios / Roles

* **Usuario Administrativo / Facturación**

  * Registra pagos.
  * Imputa pagos a facturas.
  * Consulta cuenta corriente de clientes.

* **Usuario Supervisor / Contable (lectura)**

  * Consulta estados de cuenta.
  * Verifica imputaciones y saldos.

*(No se contemplan usuarios finales ni portales de pago en este REQ)*

---

## Problema

Actualmente el sistema permite emitir facturas, pero:

* No existe un registro formal de pagos.
* No se puede determinar fácilmente si una factura está paga o parcialmente paga.
* No hay cuenta corriente que consolide débitos y créditos por cliente.
* El seguimiento financiero depende de procesos manuales o externos.

Esto genera inconsistencias operativas y riesgo en la gestión de cobranzas.

---

## Solución propuesta

Implementar un **modelo de pagos basado en Recibos**, desacoplado de la facturación fiscal, que permita:

* Registrar pagos de clientes.
* Imputar pagos total o parcialmente a una o más facturas.
* Mantener una **Cuenta Corriente** como ledger de movimientos financieros.
* Calcular saldos de clientes y estados de factura de forma automática y trazable.

---

## Alcance / Fuera de alcance

### Alcance

* Creación de Recibos de Pago.
* Imputación de pagos a facturas.
* Pagos parciales y anticipos.
* Cálculo de saldo por factura y por cliente.
* Visualización de cuenta corriente.

### Fuera de alcance

* Pasarelas de pago (MercadoPago, Stripe, etc.).
* Conciliación bancaria.
* Asientos contables formales (ERP).
* Reportes contables avanzados.
* Emisión de comprobantes fiscales por pagos.

---

## Reglas de negocio

1. El **Recibo de Pago** es un documento interno, no fiscal.
2. Una factura puede recibir múltiples pagos.
3. Un pago puede imputarse a múltiples facturas.
4. Un pago no imputado genera **saldo a favor** del cliente.
5. El estado de la factura se deriva de su saldo:

   * Emitida (saldo > 0, sin pagos).
   * Parcialmente Pagada (saldo > 0, con pagos).
   * Pagada (saldo = 0).
6. Los recibos son **inmutables**: no se eliminan, solo se revierten.
7. La cuenta corriente es la **fuente de verdad financiera**.

---

## Si aplica: Reglas fiscales AFIP

* Los pagos **no se informan a AFIP**.
* No generan CAE ni afectan IVA.
* La obligación fiscal nace y se extingue solo por comprobantes fiscales (facturas / notas de crédito).
* La anulación de una factura se realiza exclusivamente mediante Nota de Crédito (fuera de este REQ).

---

## Casos de ejemplo

### Caso 1 — Pago total de una factura

* Factura: $100.000
* Pago: $100.000
* Resultado:

  * Factura: Pagada
  * Cuenta corriente: saldo 0

### Caso 2 — Pago parcial

* Factura: $100.000
* Pago: $40.000
* Resultado:

  * Factura: Parcialmente Pagada
  * Saldo factura: $60.000

### Caso 3 — Anticipo

* Pago: $50.000
* Sin factura imputada
* Resultado:

  * Saldo a favor del cliente: $50.000

### Caso 4 — Imputación múltiple

* Factura A: $30.000
* Factura B: $20.000
* Pago: $50.000
* Resultado:

  * Ambas facturas: Pagadas

---

## Métricas de éxito

* % de facturas con estado de pago correcto.
* Reducción de ajustes manuales.
* Tiempo promedio de registro de pagos.
* Cero inconsistencias entre saldo de facturas y cuenta corriente.
* Tests de imputación pasando en CI.

---

## Riesgos y supuestos

### Riesgos

* Confundir pagos con fiscalidad.
* Errores de cálculo si no se respeta el modelo de imputación.
* Complejidad futura por múltiples monedas.

### Supuestos

* Una factura se maneja en una única moneda.
* El sistema no reemplaza un ERP contable.
* Los usuarios comprenden la diferencia entre factura y recibo.

---

 **Nota de Arquitectura:**
 Este PRD sigue el principio de separación estricta entre obligación fiscal (facturas) y movimientos financieros (pagos), permitiendo escalar el sistema sin comprometer la integridad fiscal ni operativa.
