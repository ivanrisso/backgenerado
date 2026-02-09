# Fix Description — HF-TECH-002

## Problema
Enlaces rotos en el menú de navegación (Sidebar).
Al hacer clic en "Menús" o "Dashboard", la aplicación redirige a una página 404 o muestra advertencias de ruta no encontrada.

## Síntoma
- Clic en "Menús" -> 404.
- Clic en "Dashboard" -> 404.
- Advertencias en consola `[Vue Router warn]: No match found`.

## Evidencia
- Reporte `ui_runtime_errors.md`
- Reporte `menu_runtime_report.md`
