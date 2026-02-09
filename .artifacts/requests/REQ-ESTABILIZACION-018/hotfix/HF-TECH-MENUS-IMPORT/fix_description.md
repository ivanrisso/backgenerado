# Fix Description: HF-TECH-MENUS-IMPORT

## Problema
El componente `MenuItemTree.vue` intenta importar `MenuItem` usando `../../../domain/entities/MenuItem` (incorrecto).

## Impacto
Crash de la vista `/menus`.

## Criterio
Corregir import a `@domain/entities/MenuItem`.
