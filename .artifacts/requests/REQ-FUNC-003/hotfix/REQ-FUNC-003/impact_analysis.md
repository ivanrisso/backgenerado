# Impact Analysis: REQ-FUNC-003 (Menú Dinámico)

## Componentes Afectados

### Backend
- **Archivo:** `app/routes/menuitem_routes.py`
- **Cambio:** Agregar endpoint `GET /all` (o `/public`) accesible para usuarios autenticados (no solo admin).
- **Riesgo:** Bajo. Exponer la estructura del menú a usuarios autenticados es estándar.

### Frontend
- **Archivo:** `src/shared/ui/components/Sidebar.vue`
- **Cambio:** Reemplazar `menuConfig` estático por `useMenuItems().menuTree`.
- **Lógica:**
    - Mantener lógica de filtrado recursivo `filterItems`.
    - **Adaptación:** Mapear `item.roles` (Array de Objetos) a `item.roles.map(r => r.nombre)` (Array de Strings) para compatibilidad con `authStore.canAccess`.
- **Composable:** `src/modules/Auth/ui/composables/useMenuItems.ts`
    - Puede requerir ajuste si `getTree` usa el endpoint de Admin. Debería usar el nuevo endpoint `/public` o detectar permisos.
    - Alternativa: Crear `useSidebarMenu` que use el endpoint `/public`.
    - **Decisión:** Modificar `AxiosMenuItemRepository` para usar endpoint público si no es admin, o simplemente usar siempre el endpoint público para la estructura (ya que el admin también lo ve).
    - *Corrección:* `GET /menuitems/` devuelve lista plana. El repositorio construye el árbol. Si "abrimos" `GET /menuitems/` a autenticados, el mismo endpoint sirve para todos.

## Riesgos y Mitigación
1. **Performance:** Fetch en cada carga de Sidebar.
    - *Mitigación:* Pinia Store (`authStore` o `menuStore`) podría cachear el árbol.
    - *Decisión MVP:* Fetch en `onMounted` de Sidebar es aceptable por ahora (navegación SPA no recarga Sidebar a menos que se refresque página).
2. **Compatibilidad de Tipos:** `MenuItem` tiene `roles: Rol[]`, `authStore` espera `string[]`.
    - *Mitigación:* Transformación en el template o computed de Sidebar.

## Estimación de Esfuerzo
- Backend: 15 min.
- Frontend: 30 min.
- Testing: 15 min.
- Total: ~1 hora.
