# Análisis de Impacto: HF-FUNC-001 (Puntos de Venta)

## 1. Componentes Afectados

### Backend
- **Estado:** ✅ Existe.
- **Rutas:** `app/routes/punto_venta_routes.py`
- **Modelos:** `app/infrastructure/db/orm_models.py`
- **Acción:** Verificar endpoints (Swagger) y asegurar que el usuario Admin tenga permisos.

### Frontend
- **Estado:** ⚠️ Parcialmente oculto/roto.
- **Vistas:** `PuntoVentaList.vue` existe en `modules/Maestros`.
- **Ruta:** `/puntos-venta` parece estar definida pero reporta 404 o no accesible.
- **Menu:** Inexistente en la base de datos de navegación.

## 2. Evaluación de Riesgo
- **Nivel:** BAJO.
- **Justificación:** Se trata de "conectar" piezas existentes. No requiere lógica nueva de negocio compleja, solo exposición en UI y router.

## 3. Matriz de Impacto
| Componente | Tipo de Cambio | Riesgo |
| :--- | :--- | :--- |
| **Router** | Configuración | Mínimo |
| **Sidebar/Menu** | Insert DB Script / Config | Mínimo |
| **Permisos** | Asignación de Rol | Medio (Seguridad) |

## 4. Estrategia de Rollback
- Eliminar el ítem de menú de la base de datos.
- Revertir cambios en `router/index.ts`.
