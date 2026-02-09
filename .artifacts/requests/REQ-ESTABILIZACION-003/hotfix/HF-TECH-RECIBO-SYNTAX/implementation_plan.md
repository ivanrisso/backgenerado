# Plan de Implementación - HF-TECH-RECIBO-SYNTAX

## Objetivo
Corregir error de sintaxis en `ReciboListView.vue` que impide la compilación del módulo de Tesorería.

## Archivos Afectados
- `frontend/src/modules/Tesoreria/ui/views/ReciboListView.vue`

## Cambios
1.  **[MODIFY]** `ReciboListView.vue`: Eliminar la etiqueta duplicada `<td ...>` en la línea 214 (aprox).

## Verificación
1.  **Compilación:** Verificar que no haya errores en la consola de `npm run dev` (Hot Module Replacement).
2.  **Runtime:** Navegar a `/recibos` y verificar que la carga de la vista sea exitosa.
