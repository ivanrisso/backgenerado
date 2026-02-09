Contexto:
Existen inconsistencias en el Sidebar de la aplicación (Vue 3).
1. Faltan items críticos de "Maestros": Domicilios, Teléfonos, Tipos Domicilio.
2. El link "Dashboard" apunta a `/dashboard`, pero la ruta correcta es `/`.

Objetivo:
Reparar la configuración o lógica del Sidebar para que estos items se muestren y el Dashboard navegue correctamente.

Restricciones:
- No modificar lógica de permisos compleja si no es necesario (haz que aparezcan si el usuario es Admin).
- Usar rutas existentes (`routes_inventory.md`).
- Verificar si es un hardcoding en `Sidebar.vue` o un problema data-driven.

Pasos:
1. Inspeccionar `Sidebar.vue` y `useSidebar.ts`.
2. Corregir lista de items.
3. Corregir `to="/dashboard"` a `to="/"`.
