# Impact Analysis — Recibos Menu & ABM

## Componentes Afectados

### Frontend (`src/`)
1.  **`modules/Tesoreria/ui/views/ReciboListView.vue`**
    -   **Impacto Alto:** Reemplazar Autocomplete por Select.
    -   **Impacto Medio:** Agregar botones de acción (Imprimir, Eliminar, Modificar).
2.  **`router/index.ts`**
    -   **Impacto Bajo:** Verificar rutas (ya existen, solo asegurar consistencia).
3.  **Base de Datos / Menú Config**
    -   **Impacto Bajo:** Se requiere insertar el MenuItem "Recibos" en Tesorería.

### Backend (`app/`)
-   No se requieren cambios de lógica de negocio salvo endpoints stubs si las acciones fueran reales.
-   **Nota:** El requerimiento pide botones que *redirijan* a pantallas.
    -   Agregar -> `/recibos/nuevo` (Existe).
    -   Imprimir -> `/recibos/imprimir/{id}` (No existe stub).
    -   Eliminar -> `/recibos/eliminar/{id}` (No existe stub).
    -   Modificar -> `/recibos/modificar/{id}` (No existe stub).

## Evaluación de Riesgo
-   **UX/UI:** Cambio de autocomplete a select puede problemas de performance si hay miles de clientes. (Se asume carga completa de `loadClientes` para el Select).
-   **Funcional:** Bloqueante si no se selecciona cliente (Filtro obligatorio).

## Estrategia de Mitigación
-   Usar `v-select` o select nativo con `v-for`.
-   Validar que `loadClientes` no traiga data excesiva (o aceptar riesgo MVP).
