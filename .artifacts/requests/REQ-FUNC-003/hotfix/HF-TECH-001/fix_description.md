# Fix Description — HF-TECH-001

## Problema
Error de resolución de módulos en vista `DomicilioView.vue`.
El navegador falla al cargar la vista con error de importación.

## Síntoma
- Al navegar a `/domicilios`, la pantalla queda en blanco o muestra error de Vite.
- Consola: `[vite] failed to resolve import useDomicilios`.

## Evidencia
- Reporte `ui_runtime_errors.md`
- Logs de consola.
