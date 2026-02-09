# Casos de Prueba: REQ-FUNC-003 (Menú Dinámico)

## Precondiciones
- Usuario logueado (Admin).
- Ítem "Puntos de Venta" existe en Base de Datos (insertado en HF-FUNC-001).
- Ítem "Puntos de Venta" NO existe en `config/menu.ts` (verificado por omisión).

## Casos

### TC-01: Carga Dinámica de Menú
**Pasos:**
1. Login como Admin.
2. Observar Sidebar.
3. Verificar que aparece el grupo "Maestros" (o Configuración).
4. Verificar que aparece el ítem "Puntos de Venta".
**Resultado Esperado:** El ítem es visible por estar en DB, demostrando que el sidebar ya no es estático.

### TC-02: Navegación desde Menú Dinámico
**Pasos:**
1. Click en "Puntos de Venta" en el Sidebar.
**Resultado Esperado:** Navega a `/puntos-venta`.

### TC-03: Filtrado de Roles (Básico)
**Pasos:**
1. Verificar iconos de candado o items restringidos si existen en la DB.
(Opcional: Si el admin ve todo, es suficiente por ahora confirmar que ve lo de la DB).
**Resultado Esperado:** Renderizado correcto de items con roles.
