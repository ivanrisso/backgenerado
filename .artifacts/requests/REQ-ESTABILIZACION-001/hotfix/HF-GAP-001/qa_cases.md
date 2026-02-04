# Casos de Prueba - HF-GAP-001 (Imputación Parcial)

## Introducción
Validar la capacidad de imputar montos parciales de Notas de Crédito a Facturas asociadas.

## Casos de Prueba

### [TEST-01] Imputación Automática (Default)
- **Descripción**: Crear NC asociada sin campo `importe_imputar` (o 0).
- **Precondición**: Factura con saldo 1000. NC por 1000.
- **Input**: `cbtes_asociados: [{...}]`
- **Resultado Esperado**:
  - Imputación creada por 1000.
  - Saldo Factura: 0.

### [TEST-02] Imputación Parcial Explícita
- **Descripción**: Crear NC asociada con `importe_imputar` menor al saldo.
- **Precondición**: Factura con saldo 1000. NC por 500. `importe_imputar=300`.
- **Input**: `cbtes_asociados: [{..., "importe_imputar": 300}]`
- **Resultado Esperado**:
  - Imputación creada por 300.
  - Saldo Factura: 700.
  - Saldo NC: 200 (Discrepancia posible: La NC se crea por su total, el saldo de la NC debería reflejar lo que no se usó? O la imputación es solo un vínculo? En el modelo actual, `Comprobante` tiene `saldo`. Si imputo 300, la NC debería quedar con saldo 200).

### [TEST-03] Validación: Exceso de Saldo Factura
- **Descripción**: Intentar imputar más del saldo pendiente de la factura.
- **Precondición**: Factura saldo 500. NC 1000. `importe_imputar=600`.
- **Resultado Esperado**: Error de validación (400 Bad Request) o ajuste automático al máximo (según definición, plan dice "Validar" -> asumimos Error o Tope? El plan dice "Validar importe_imputar <= invoice.saldo", implicando Error o lógica de tope. Definiremos "Error" para mayor control).

### [TEST-04] Validación: Exceso de Monto NC
- **Descripción**: Intentar imputar más del total de la propia NC.
- **Precondición**: Factura saldo 1000. NC 500. `importe_imputar=600`.
- **Resultado Esperado**: Error de validación.

## Datos de Prueba
- Cliente ID: Test Client.
- Puntos de Venta: 1.
