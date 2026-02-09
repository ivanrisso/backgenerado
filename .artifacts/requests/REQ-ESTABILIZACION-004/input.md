# REQ-ESTABILIZACION-004 - Recibos Full ABM

## Contexto
Actualmente existen stubs para las acciones de Eliminar, Modificar e Imprimir Recibos. La creación (Alta) ya existe.

## Objetivo
Implementar la funcionalidad completa de ABM:
1.  **Baja (Delete):** Permitir anular/eliminar un recibo.
2.  **Modificación (Update):** Permitir editar observaciones o fecha (limitado).
3.  **Impresión (Print):** Mostrar una vista de impresión simple.

## Alcance
-   **Frontend:** Reemplazar stubs `ReciboDeleteView`, `ReciboModifyView`, `ReciboPrintView`.
-   **Backend:** Implementar endpoints `DELETE /recibos/{id}` y `PUT /recibos/{id}`.

## Criterios de Aceptación
-   Se puede eliminar un recibo (o marcar como anulado).
-   Se puede editar un recibo.
-   Se puede visualizar la vista de impresión con datos reales.
