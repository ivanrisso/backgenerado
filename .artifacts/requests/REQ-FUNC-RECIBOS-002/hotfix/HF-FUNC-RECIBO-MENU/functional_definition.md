# Recibos - Mejoras de Menu y ABM

## Problema
- El listado de recibos no es accesible desde el menú principal.
- La funcionalidad de filtrado y gestión es precaria.
- Faltan acciones de gestión (Imprimir, Eliminar, Modificar).

## Comportamiento Actual
- Vista `/recibos` escondida (sin link en menu).
- Filtro por cliente usando autocomplete (no select).
- Solo acción "Ver".

## Comportamiento Esperado
1. **Menú Tesorería:** Agregar opción "Recibos" visible.
2. **Listado de Recibos:**
   - Filtro obligatorio por CLIENTE usando un **SELECT** (Dropdown).
   - Mostrar todos los recibos del cliente seleccionado.
   - Botones de acción explícitos:
     - [Agregar Recibo] -> `/recibos/nuevo`
     - [Imprimir] -> Acción de impresión (simulada/stub)
     - [Eliminar] -> Acción de eliminación (simulada/stub)
     - [Modificar] -> Acción de modificación (simulada/stub)
