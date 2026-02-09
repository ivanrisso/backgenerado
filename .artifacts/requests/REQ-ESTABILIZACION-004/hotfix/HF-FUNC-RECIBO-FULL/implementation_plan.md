# Plan de Implementación - HF-FUNC-RECIBO-FULL

## Objetivo
Implementar la lógica real para las acciones de Eliminar, Modificar e Imprimir Recibos.
Agregar en el menu el item Recibos y borrar del menu el item Nuevo Recibo

## Backend
1.  **`app/routes/recibo_routes.py`**:
    -   Agregar `DELETE /{id}`: Llama a `ReciboService.delete`.
    -   Agregar `PUT /{id}`: Llama a `ReciboService.update`.
2.  **`app/services/recibo_service.py`**:
    -   Implementar `delete_recibo(id)`: Invocar repositorio para eliminar (físico por simplicidad MVP, o soft delete si el modelo lo permite).
    -   Implementar `update_recibo(id, data)`: Invocar repositorio para actualizar `observaciones` y `fecha_emision`.
3.  **`app/repositories/comprobante_repository.py`**:
    -   Verificar métodos `delete` y `update`. (Probablemente usar `session.delete` y `session.merge` o `update`).

## Frontend
1.  **`ReciboService.ts`**:
    -   Agregar método `delete(id)`.
    -   Agregar método `update(id, payload)`.
2.  **`ReciboDeleteView.vue`**:
    -   Cargar datos del recibo.
    -   Mostrar advertencia.
    -   Botón "Confirmar Eliminación" -> llama `ReciboService.delete` -> `router.push('/recibos')`.
3.  **`ReciboModifyView.vue`**:
    -   Reutilizar form o crear uno simple con Fecha y Observaciones.
    -   Botón "Guardar" -> llama `ReciboService.update`.
4.  **`ReciboPrintView.vue`**:
    -   Diseño HTML limpio (blanco y negro).
    -   Tabla de items (imputaciones si las hubiera, o solo totales).
    -   Botón `window.print()`.

## Verificación
-   **Delete:** Crear recibo -> Eliminar -> Verificar que no sale en lista.
-   **Update:** Crear recibo -> Modificar obs -> Verificar en detalle.
-   **Print:** Verificar vista preliminar.
