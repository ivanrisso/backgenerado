# Analysis: HF-TECH-SIDEBAR-GAPS

## Causa Raíz Probable
1. **Hardcoding:** El componente `Sidebar` podría tener una lista estática que no incluye los items nuevos.
2. **Filtering Logic:** El composable `useSidebar` podría estar filtrando items por algún criterio (permiso faltante, flag `visible`, etc.) que estos items no cumplen.
3. **Router Link:** El link del Dashboard está mal definido en el template o configuración.

## Componentes Involucrados
- `frontend/src/shared/ui/components/Sidebar.vue`
- `frontend/src/shared/composables/useSidebar.ts` (si existe)

## Riesgos
- Al modificar el filtrado, podrían aparecer items no deseados o duplicados.
