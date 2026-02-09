# Fix Description: HF-TECH-SIDEBAR-GAPS (REQ-020)

## Qué falla
- **Items Missing:** Los items `Domicilios`, `Teléfonos` y `Tipos Domicilio` NO se renderizan en el Sidebar bajo "Maestros".
- **Broken Link:** El item `Dashboard` apunta a `/dashboard` (404), debería apuntar a `/`.

## Dónde ocurre
- Componente `Sidebar.vue` (frontend).
- Base de datos de menús / API `/menuitems` (configuración).

## Cómo se manifiesta
- El usuario Admin no puede acceder a los ABM de Domicilios/Teléfonos desde el menú (aunque las rutas funcionan si se escriben manualmente).
- Al hacer clic en "Dashboard", recibe un error 404 (o pantalla blanca).

## Impacto técnico
- Inconsistencia entre configuración (DB) y UI.
- Navegación rota.
