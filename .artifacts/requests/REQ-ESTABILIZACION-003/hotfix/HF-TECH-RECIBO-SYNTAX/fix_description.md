# ReciboListView Syntax Error

## Problema
Error de compilación en `ReciboListView.vue`. Se duplicó la etiqueta de apertura `<td>` durante el refactor de acciones, dejando una etiqueta sin cerrar.

## Error Runtime
`Element is missing end tag` (Vue Compiler)

## Solución
Eliminar la línea duplicada (aprox línea 214).

```html
<!-- INCORRECTO -->
<td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
<td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">

<!-- CORRECTO -->
<td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
```
