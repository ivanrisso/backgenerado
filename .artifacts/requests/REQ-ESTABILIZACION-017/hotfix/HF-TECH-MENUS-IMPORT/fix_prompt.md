# Fix Prompt: HF-TECH-MENUS-IMPORT

## Contexto
El archivo `src/modules/Auth/ui/views/MenuItemTree.vue` tiene un import roto hacia la entidad `MenuItem`.

## Problema
Línea 5: `import type { MenuItem } from '../../../domain/entities/MenuItem';`
Ruta relativa incorrecta.

## Instrucción para Workflow 71
1. Editar `src/modules/Auth/ui/views/MenuItemTree.vue`.
2. Corregir el import de `MenuItem`.
   - Preferencia: `@domain/entities/MenuItem`.
   - Fallback: `../../../../domain/entities/MenuItem`.
3. Validar cargando la ruta `/menus`.

## Evidencia Requerida
- Screenshot de `/menus` cargando el árbol.
