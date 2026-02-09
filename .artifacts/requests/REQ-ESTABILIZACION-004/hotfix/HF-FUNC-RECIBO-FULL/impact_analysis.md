# Impact Analysis - Recibos Full ABM

## Componentes Afectados

### Backend (`app/`)
1.  **`routes/recibo_routes.py`**:
    -   [NEW] `DELETE /{id}`
    -   [NEW] `PUT /{id}`
2.  **`services/recibo_service.py`**:
    -   [NEW] `delete_recibo(id)`
    -   [NEW] `update_recibo(id, data)`
3.  **`repositories/comprobante_repository.py`**:
    -   Revisar si `delete` y `update` genéricos son suficientes o se requiere específicos.

### Frontend (`src/`)
1.  **`modules/Tesoreria/infrastructure/api/ReciboService.ts`**:
    -   [NEW] `delete(id)`
    -   [NEW] `update(id, data)`
2.  **`modules/Tesoreria/ui/views/ReciboDeleteView.vue`**:
    -   [MODIFY] Implementar lógica real.
3.  **`modules/Tesoreria/ui/views/ReciboModifyView.vue`**:
    -   [MODIFY] Implementar formulario de edición.
4.  **`modules/Tesoreria/ui/views/ReciboPrintView.vue`**:
    -   [MODIFY] Implementar diseño de factura/recibo.

## Riesgos
-   **Integridad de Datos:** Eliminar un recibo que tiene imputaciones podría dejar inconsistencias en Cuentas Corrientes. 
    -   **Mitigación:** En este MVP se asume que la eliminación revierte el saldo del cliente (si la lógica de CC está atada a la existencia del comprobante).
-   **Complejidad de Edición:** Editar montos requiere recalcular todo.
    -   **Mitigación:** Solo permitir editar Observaciones y Fecha.

