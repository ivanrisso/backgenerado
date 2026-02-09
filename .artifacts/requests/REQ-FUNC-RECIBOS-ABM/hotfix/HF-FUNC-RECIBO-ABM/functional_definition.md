# Definición Funcional — Recibo ABM

## Comportamiento Actual
- El usuario puede crear recibos pero no puede verlos.
- No existe endpoint para listar recibos.
- No existe vista de grilla de recibos.

## Comportamiento Esperado
1. **Menú Tesorería:**
   - Ítem "Recibos" que lleva al listado.
2. **Listado de Recibos (`/recibos`):**
   - Grilla con columnas: Número, Fecha, Cliente, Importe, Saldo, Estado (si aplica).
   - Botón "Nuevo Recibo" (navega a `/recibos/nuevo`).
   - Acciones por fila: "Ver Detalle" (lupa).
3. **Detalle de Recibo (Modal o Nueva Vista):**
   - Visualización de datos de cabecera e imputaciones.
   - (MVP: Solo visualización).

## Alcance
- **Backend:**
  - `GET /recibos/` (Paginado standard).
  - `GET /recibos/{id}`.
- **Frontend:**
  - `ReciboService.getAll()`.
  - `ReciboService.getById()`.
  - `ReciboListView.vue`.
  - Router link.

## Fuera de Alcance
- Anulación de recibos (Workflow futuro).
- Reimpresión PDF (Workflow futuro, aunque deseable).
