# Analysis: HF-TECH-ROLES-IMPORT

## Causa Raíz
Refactorización previa o movimiento de archivos que no actualizó los imports relativos profundos.
El nivel de anidamiento de `modules/Auth/ui/views` es más profundo de lo calculado en el import.

## Riesgos
Bajo. Solo afecta al import de tipado/clase.

## Componentes Afectados
- `src/modules/Auth/ui/views/RolForm.vue`
