# Analysis — HF-TECH-002

## Causa Raíz
Inconsistencia entre las rutas definidas en `router/index.ts` y los enlaces hardcodeados o dinámicos en el componente `Sidebar` (o base de datos de menús).
- `/dashboard` vs `/`
- `/menu-items` vs `/menus`

## Componentes
- `router/index.ts`
- Tabla `menuitem` (si los menús vienen de DB)
- Componente `Sidebar` (si los links son estáticos)

## Riesgo
Bajo. Ajuste de configuración.
