# Fix Prompt — HF-TECH-001

## Contexto
Broken Import in `DomicilioView.vue`.

## Instrucción
1. Verify if `useDomicilios.ts` exists.
2. If it exists, correct the import path in `DomicilioView.vue`.
3. If it does not exist, check if it was renamed or moved (e.g. to `@shared`).
4. Verify the view loads without error.
