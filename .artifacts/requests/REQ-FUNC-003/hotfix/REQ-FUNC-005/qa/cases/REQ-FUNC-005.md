# Test Cases: REQ-FUNC-005 (Agrupación Seguridad)

## Prerrequisitos
- Usuario autenticado como Admin.
- Fix de BD aplicado (Seguridad ID 4 asignado a Admin).

## Casos de Prueba

| ID | Título | Pasos | Resultado Esperado |
|---|---|---|---|
| TC-01 | Verificación API | 1. Ejecutar `inspect_seguridad_menu.js`. | Salida muestra "Seguridad Item" encontrado y children asociados a ID 4. |
| TC-02 | Agrupación Visual | 1. Recargar Dashboard.<br>2. Verificar Sidebar. | "Usuarios", "Roles", "Menús" NO están en primer nivel. Aparece "Seguridad". |
| TC-03 | Interacción Grupo | 1. Click en "Seguridad". | Se despliega el grupo mostrando los 3 hijos. |
