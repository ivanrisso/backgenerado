# Test Cases: REQ-FUNC-004 (Corrección Jerarquía Menú)

## Prerrequisitos
- Usuario autenticado como Admin.
- Base de datos con menú "Puntos de Venta" (ID X) hijo de "Maestros/Configuración" (ID Y).

## Casos de Prueba

| ID | Título | Pasos | Resultado Esperado |
|---|---|---|---|
| TC-01 | Verificación de Logs | 1. Abrir DevTools (Consola).<br>2. Recargar Dashboard. | Consola muestra "Raw Menu Items" y el array de items. No hay Warnings de Huérfanos. |
| TC-02 | Jerarquía Visual | 1. Observar Sidebar.<br>2. Verificar items de primer nivel. | Sidebar muestra grupos (ej. "Configuración"). "Puntos de Venta" NO está en primer nivel. |
| TC-03 | Navegación Anidada | 1. Expandir "Configuración".<br>2. Click en "Puntos de Venta". | Se despliega el submenú y navega a `/puntos-venta`. |
| TC-04 | Manejo de Huérfanos | (Opcional, requiere manipulación de DB) | Si se asigna un `parent_id` inexistente, el item aparece en el raíz con Warning en consola. |
