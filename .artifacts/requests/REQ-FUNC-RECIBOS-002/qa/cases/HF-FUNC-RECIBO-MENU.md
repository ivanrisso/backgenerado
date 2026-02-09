# Casos de Prueba - HF-FUNC-RECIBO-MENU

## Case 1: Filtro de Clientes (Select)
- **Precondición:** Existen clientes y recibos asociados.
- **Acción:** Seleccionar un cliente del dropdown "Cliente".
- **Resultado Esperado:** La grilla se actualiza mostrando solo los recibos de ese cliente.
- **Verificación:** `applyFilters` se dispara al cambiar el select.

## Case 2: Navegación de Acciones
- **Acción:** Clicar en botón "Imprimir" (ícono impresora).
- **Resultado:** Navega a `/recibos/imprimir/{id}` (Stub).
- **Acción:** Clicar en botón "Eliminar" (ícono basura).
- **Resultado:** Navega a `/recibos/eliminar/{id}` (Stub).
- **Acción:** Clicar en botón "Modificar" (ícono lápiz).
- **Resultado:** Navega a `/recibos/modificar/{id}` (Stub).

## Case 3: Menú Principal
- **Acción:** Verificar barra lateral / menú.
- **Resultado:** Existe ítem "Tesorería" -> "Recibos".
- **Resultado Negativo:** NO existe "Nuevo Recibo" en el menú.
