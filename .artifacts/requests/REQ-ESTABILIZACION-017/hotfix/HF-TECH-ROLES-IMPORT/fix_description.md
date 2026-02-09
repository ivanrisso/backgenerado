# Fix Description: HF-TECH-ROLES-IMPORT

## Problema
El componente `RolForm.vue` intenta importar la entidad `Rol` usando una ruta relativa incorrecta:
`../../../domain/entities/Rol`
Esto resuelve a `src/modules/domain/entities/Rol`, ruta inexistente.

## Impacto
La vista `/roles` crashea inmediatamente al intentar cargar.
Bloquea la gestión de roles de seguridad.

## Criterio de Corrección
Reemplazar el import incorrecto por el path absoluto (alias) o la ruta relativa correcta.
- Incorrecto: `../../../domain/entities/Rol`
- Opción A (Alias): `@domain/entities/Rol`
- Opción B (Relativo): `../../../../domain/entities/Rol`

Se prefiere el uso de **Alias** si está configurado en `tsconfig`/`vite.config`, o relativo correcto si no.

## Verificación
- Navegar a `/roles`.
- La vista debe cargar el formulario sin error de Vite.
