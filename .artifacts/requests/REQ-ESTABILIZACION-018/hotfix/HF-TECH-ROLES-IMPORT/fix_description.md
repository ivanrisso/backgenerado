# Fix Description: HF-TECH-ROLES-IMPORT

## Problema
El componente `RolForm.vue` intenta importar `Rol` usando `../../../domain/entities/Rol` (incorrecto).

## Impacto
Crash de la vista `/roles`.

## Criterio
Corregir import a `@domain/entities/Rol` o ruta relativa válida.
