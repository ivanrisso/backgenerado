# REQ-ID: REQ-001 — Pagos / Recibos / Cuenta Corriente

---

## Contexto

El sistema de facturación actualmente permite la emisión de comprobantes (facturas, notas, etc.), pero **no cuenta con un mecanismo formal de registro de pagos**, imputación de los mismos a facturas, ni gestión de **cuenta corriente de clientes**.

Esto genera:

* Falta de visibilidad del estado real de deuda.
* Imposibilidad de manejar pagos parciales, anticipos o saldos a favor.
* Dificultad para conciliación contable y seguimiento financiero.

---

## Objetivo

Implementar un **módulo de pagos basado en Recibos**, que permita:

* Registrar pagos de clientes.
* Imputar uno o más pagos a una o más facturas.
* Gestionar correctamente la **Cuenta Corriente** del cliente.
* Mantener trazabilidad financiera sin afectar la fiscalidad de AFIP.

---

## Alcance

### Funcional

* Creación de **Recibos de Pago**.
* Registro de pagos:

  * Totales.
  * Parciales.
  * Anticipos (sin factura asociada inicialmente).
* **Imputación de pagos a facturas** (total o parcial).
* Actualización automática de:

  * Saldo de la factura.
  * Saldo de la cuenta corriente del cliente.
* Visualización del estado de cuenta corriente:

  * Débitos (facturas).
  * Créditos (pagos / notas de crédito).
* Estados de factura:

  * Emitida.
  * Parcialmente Pagada.
  * Pagada.

### Técnico

* Backend (FastAPI + dominio).
* Persistencia en base de datos.
* API REST para frontend.
* UI básica para:

  * Registrar pagos.
  * Ver imputaciones.
  * Ver saldo del cliente.

---

## Fuera de alcance

* Integración con pasarelas de pago (MercadoPago, Stripe, etc.).
* Conciliación bancaria automática.
* Generación de asientos contables formales (ERP).
* Reportes contables avanzados.
* Facturación electrónica de pagos (no aplica).

---

## Reglas de negocio

1. **El Recibo NO es un comprobante fiscal AFIP**

   * Es un documento **interno / comercial**.
   * No genera CAE.
   * No se informa a AFIP.

2. **Separación estricta entre Factura y Pago**

   * La factura representa la obligación fiscal.
   * El pago representa un movimiento financiero.

3. **Imputación explícita**

   * Todo pago debe:

     * imputarse a una o más facturas **o**
     * quedar como **saldo a favor** del cliente.

4. **Pagos parciales**

   * Una factura puede recibir múltiples pagos.
   * El estado de la factura se actualiza automáticamente.

5. **Cuenta corriente como fuente de verdad**

   * El saldo del cliente se calcula por:

     ```
     saldo = sum(facturas emitidas) - sum(pagos imputados) - notas de crédito
     ```

6. **Inmutabilidad lógica**

   * Un recibo no se elimina.
   * En caso de error, se genera un recibo inverso (anulación / reverso).

7. **Moneda**

   * El pago debe respetar la moneda de la factura.
   * No se permite imputación cruzada entre monedas en esta fase.

---

## Si aplica: AFIP / fiscalidad

* **No se reportan pagos a AFIP**.
* La fiscalidad está determinada **únicamente por la factura emitida**.
* El pago:

  * No modifica IVA.
  * No modifica CAE.
  * No genera nuevos comprobantes fiscales.
* La anulación de una factura **NO se hace con pagos**, sino con **Nota de Crédito** (fuera de este REQ).

---

## Criterios de aceptación

### Funcionales

* Se puede crear un recibo de pago para un cliente.
* Se puede imputar un pago a:

  * una factura,
  * varias facturas,
  * ninguna (anticipo).
* El sistema calcula correctamente:

  * saldo de factura,
  * estado de factura,
  * saldo de cuenta corriente.
* Se puede visualizar el detalle de imputaciones.

### Técnicos

* API REST documentada.
* Tests unitarios para:

  * imputación total,
  * imputación parcial,
  * saldo a favor.
* CI verde.

---

## Riesgos / supuestos

### Riesgos

* Confusión entre fiscalidad (facturas) y finanzas (pagos).
* Errores de cálculo de saldo si no se maneja correctamente la imputación.
* Complejidad futura si se agregan múltiples monedas o pasarelas.

### Supuestos

* El cliente opera en una sola moneda por factura.
* El sistema no es un ERP contable completo.
* La cuenta corriente es **financiera**, no contable.

---

## Notas técnicas

* Entidades sugeridas:

  * `ReciboPago`
  * `ReciboPagoDetalle` (imputaciones)
  * `CuentaCorrienteMovimiento`
* Patrón recomendado:

  * **Ledger / movimientos** en lugar de saldo persistido.
* Evitar campos calculados persistentes sin respaldo en movimientos.
* Las consultas de saldo deben poder reconstruirse desde movimientos.

---

### Comentario de Arquitectura

> **Factura = obligación fiscal**
> **Pago = movimiento financiero**

Este diseño permite escalar a anticipos, notas de crédito, pasarelas de pago y conciliación bancaria sin romper el modelo actual.
