# Fix Description: HF-TECH-DOMICILIOS-IMPORT

## Problema
`DomicilioView.vue` falla al importar `useDomicilios`.
Error: `Failed to resolve import "@modules/Maestros/composables/useDomicilios"`.

## Impacto
Crash de vista `/domicilios`.

## Criterio
Corregir el import en `src/modules/Maestros/ui/views/DomicilioView.vue`.
Verificar si `useDomicilios` existe o si el path es incorrecto.
