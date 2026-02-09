# Fix Prompt: HF-TECH-ROLES-IMPORT

## Contexto
El archivo `src/modules/Auth/ui/views/RolForm.vue` tiene un import roto que causa crash en tiempo de ejecución.

## Problema
Línea 3: `import { Rol } from '../../../domain/entities/Rol';`
Esta ruta relativa es incorrecta.

## Instrucción para Workflow 71
1. Editar `src/modules/Auth/ui/views/RolForm.vue`.
2. Cambiar el import de `Rol` para que apunte correctamente a `src/domain/entities/Rol`.
   - Preferencia: Usar alias `@domain/entities/Rol` si es posible.
   - Fallback: `../../../../domain/entities/Rol`.
3. Validar cargando la ruta `/roles`.

## Evidencia Requerida
- Screenshot de `/roles` cargando correctamente.
