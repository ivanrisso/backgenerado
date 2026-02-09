# Plan de Implementación — HF-FUNC-RECIBO-MENU

## Objetivo
Cumplir con los requerimientos de gestión de Recibos: Menu, Filtro Select y Acciones.

## Componentes

### Frontend
1.  **`modules/Tesoreria/ui/views/ReciboListView.vue`**
    -   [MODIFY] Reemplazar `<input>` de cliente por `<select>` (Dropdown).
    -   [MODIFY] Agregar columnas de acciones o menú de acciones por fila.
    -   [NEW] Implementar botones/enlaces para: Imprimir, Eliminar, Modificar.
2.  **`modules/Tesoreria/ui/views/` (Stubs)**
    -   [NEW] `ReciboPrintView.vue` (Placeholder).
    -   [NEW] `ReciboDeleteView.vue` (Placeholder).
    -   [NEW] `ReciboModifyView.vue` (Placeholder).
3.  **`router/index.ts`**
    -   [MODIFY] Agregar rutas para Print, Delete, Modify apuntando a los stubs.
4.  **Menú / Base de Datos**
    -   [SCRIPT] Crear script Python `scripts/add_recibo_menu.py` para insertar el MenuItem "Recibos" en la DB si no existe.

## Pasos
1.  Crear Script de Corrección de Menú y ejecutarlo.
2.  Crear Vistas Placeholder (Print/Delete/Modify).
3.  Actualizar Router.
4.  Refactorizar `ReciboListView.vue`:
    -   Cambiar Autocomplete -> Select.
    -   Agregar Botones de Acción.
5.  Verificar navegación y filtros.

## Verificación
-   El menú "Recibos" debe aparecer en Tesorería.
-   El menú "Nuevo Recibo" debe desaparecer.
-   El filtro de Cliente debe ser un Dropdown.
-   Al filtrar, solo deben verse recibos del cliente.
-   Los botones deben navegar a sus respectivas rutas (aunque estén vacías).
