# Casos de Prueba - HF-FUNC-RECIBO-ABM

## Case 1: Listado de Recibos
- **Precondición:** Existen recibos en base de datos.
- **Acción:** Navegar a `/recibos`.
- **Resultado Esperado:** Se visualiza la grilla con fecha, número, cliente y monto.
- **Verificación:** `curl /api/v1/recibos/` devuelve JSON con array.

## Case 2: Filtrado por Fecha
- **Acción:** Seleccionar rango de fechas en filtro y clicar "Filtrar".
- **Resultado:** La grilla se actualiza mostrando solo recibos en rango.

## Case 3: Detalle de Recibo
- **Acción:** Clicar en "Ver" en una fila.
- **Resultado:** Navega a `/recibos/{id}` y muestra detalles (Cliente, Total, Saldo).
- **Verificación:** `curl /api/v1/recibos/{id}` devuelve JSON correcto.
