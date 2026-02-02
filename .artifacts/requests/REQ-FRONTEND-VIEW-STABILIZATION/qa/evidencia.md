# Evidencia de Estabilización de Vistas (Maestros)

**Fecha:** 30/01/2026
**Responsable:** Senior Frontend Architect
**Request:** REQ-FRONTEND-VIEW-STABILIZATION

## 1. Resumen Ejecutivo
Se han analizado y saneado todas las vistas del módulo `Maestros` (`src/modules/Maestros/ui/views/`). El objetivo fue eliminar los errores de "Failed to fetch dynamically imported module" causados por imports a archivos inexistentes o paths relativos rotos. Se logró estabilizar la carga de módulos mediante la normalización de imports y la creación de stubs de infraestructura faltante.

## 2. Acciones Realizadas

### A. Creación de Stubs (Dependencias Faltantes)
Se detectó que múltiples vistas dependían de composables que no existían físicamente. Para evitar el crash en tiempo de ejecución y permitir el lazy loading, se crearon los siguientes archivos "stub" (placeholder) en `src/modules/Maestros/composables/`:

1. `useConceptos.ts`
2. `useIvas.ts`
3. `useMonedas.ts`
4. `useOperadores.ts`
5. `useTelefonos.ts`
6. `useTiposComprobante.ts`
7. `useArticulos.ts`

También se creó un stub para el componente faltante:
- `@modules/Maestros/components/config/UbicacionSelector.vue`

### B. Normalización de Imports (Bulk Update)
Se ejecutó una refactorización masiva en las vistas para eliminar imports relativos frágiles y utilizar alias robustos:

| Patrón Anterior (Relativo) | Patrón Nuevo (Alias) | Estado |
|----------------------------|----------------------|--------|
| `../../../domain/` | `@domain/` | ✅ Type Safe |
| `../../composables/` | `@modules/Maestros/composables/` | ✅ Type Safe |
| `../../components/` | `@modules/Maestros/components/` | ✅ Safe (con stub) |

### C. Corrección Específica
- Se reemplazó el uso de `useTiposContacto` (inexistente) por `useTiposTel` (existente) en `ContactosView.vue` y `TipoTelView.vue`.

## 3. Verificación de Calidad

### Type Check
Comando: `npm run typecheck` (`vue-tsc --noEmit`)
Resultado: **EXITO**. Todos los módulos ahora resuelven sus dependencias correctamente.

### Linting
Comando: `npm run lint` & `npm run lint:fix`
Resultado: **EXITO**. Código acorde a estándares.

## 4. Conclusión
El módulo `Maestros` ahora es compilable y navegable. Las vistas ya no fallarán al intentar cargarse dinámicamente porque todas sus dependencias internas son resolubles.
> **Nota:** Los composables creados son "stubs" funcionales (retornan arrays vacíos y flags de carga), por lo que las vistas renderizarán pero no mostrarán datos reales hasta que se implemente la lógica de negocio real en cada composable.
