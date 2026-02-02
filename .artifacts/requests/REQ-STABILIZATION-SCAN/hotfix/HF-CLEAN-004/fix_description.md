# 🔧 Fix Description — HF-CLEAN-004

## Contexto
Vistas Maestras (`/provincias`, `/localidades`).

## Problema Detectado
- Infinite Loops ("Loading...").
- Errores de caché/watchers (console flooding).

## Causa Raíz
- `useUbicacion.ts` incompleto (faltaban métodos CRUD y estado reactivo para filtros).
- Watchers en Vistas ejecutando sobre datos `null`/`undefined` sin guard clauses.

## Alcance de la Corrección
- Refactor total de `useUbicacion.ts` (Implementación real de Stores/Repo).
- Adición de Guard Clauses (`if (!val) return`) en `ProvinciaView` y `LocalidadView`.

## Validación
- Carga estable de `/provincias`.
- Filtrado funcional País -> Provincia.
