# Fix Prompt: HF-TECH-DOMICILIOS-IMPORT

## Contexto
Error de import en `DomicilioView.vue`.

## Instrucción
1. Localizar `src/modules/Maestros/ui/views/DomicilioView.vue`.
2. Verificar el import de `useDomicilios`.
3. Buscar el archivo real de `useDomicilios` (probablemente en `@modules/Maestros/composables/` o `@shared/composables/`).
4. Corregir la ruta.

## Evidencia
Screenshot de `/domicilios` cargando (aunque no esté en el menú, se puede acceder por URL).
