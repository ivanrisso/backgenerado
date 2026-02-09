# Impact Analysis: HF-FUNC-MENU-FE-ORDER-COLLAPSE

## 1. Componentes Afectados
- **`MenuItemTree.vue`**: Requiere lógica de colapsado (UI state) y visualización del campo orden.
- **`MenuItemForm.vue`**: Requiere agregar el input `orden` (numérico) para editar.
- **`MenuItem` Entity (Frontend)**: Verificar si ya incluye `orden` (Probablemente no, si el backend recién se actualizó).
- **`useMenuItems.ts`**: Verificar mapeo de datos.

## 2. Endpoints Afectados
- `GET /api/v1/menus/tree` (o `GET /api/v1/menus`): El backend ya envía `orden`. No requiere cambios.
- `POST/PUT /api/v1/menus/{id}`: El backend ya acepta `orden`. No requiere cambios.

## 3. Riesgo Funcional
- **Bajo**. Se trata de cambios puramente visuales y de un campo adicional en un formulario existente.
- **Regresiones Posibles**:
  - Que el colapsado oculte ítems incorrectamente.
  - Que el ordenamiento rompa la jerarquía visual si no se maneja bien (ej. hijos mezclados).

## 4. Estrategia de Mitigación
- Validar que por defecto los menús aparezcan expandidos o colapsados consistentemente.
- E2E Test para verificar que el cambio de orden en CRUD se refleje en Sidebar.
