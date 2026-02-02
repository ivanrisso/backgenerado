# 🔧 Fix Description — HF-CLEAN-008

## Contexto
Navegación general.

## Problema Detectado
Rutas huérfanas sin acceso desde Menú Lateral (Tipos Comp, Recibos, Domicilios).

## Causa Raíz
Falta de configuración en `menu.ts`.

## Alcance de la Corrección
Agregar items faltantes al menú.

## Archivos / Capas Afectadas
- `src/shared/config/menu.ts`

## Restricciones
- No romper CI.

## Validaciones Esperadas
- Items visibles y funcionales en menú.

## Notas
Este archivo **NO ejecuta correcciones**.  
Es input directo del Workflow 71.
