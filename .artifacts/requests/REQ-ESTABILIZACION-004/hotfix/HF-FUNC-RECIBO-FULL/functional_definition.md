# Recibos - ABM Completo

## Problema
El sistema permite crear y listar recibos, pero las acciones de Modificación, Eliminación e Impresión son placeholders (stubs).

## Comportamiento Esperado

### 1. Eliminación (Baja)
-   **Acción:** Botón "Eliminar" en el listado.
-   **Frontend:** Navegar a vista de confirmación o modal. Al confirmar, llamar API DELETE.
-   **Backend:** Endpoint `DELETE /recibos/{id}`.
    -   **Lógica:** Soft Delete (marcar como anulado) o eliminación física si es el último y no afecta cierres (MVP: Soft Delete o eliminación simple).
    -   **Validación:** Solo admin puede eliminar.

### 2. Modificación (Update)
-   **Acción:** Botón "Modificar" en el listado.
-   **Frontend:** Vista con formulario precargado (similar a Create pero editando).
-   **Backend:** Endpoint `PUT /recibos/{id}`.
    -   **Alcance:** Permitir editar observaciones y fecha (si no está cerrado el período). No permitir editar montos/imputaciones por complejidad contable en este MVP.

### 3. Impresión (Print)
-   **Acción:** Botón "Imprimir" en el listado.
-   **Frontend:** Vista de impresión (HTML simple con estilos `@media print`).
-   **Datos:** Cabecera (Empresa), Cliente, Detalle de filas, Totales.
