# Fix Description: HF-TECH-MENUS-IMPORT

## Problema
El componente `MenuItemTree.vue` intenta importar la entidad `MenuItem` usando una ruta relativa incorrecta:
`../../../domain/entities/MenuItem`
Esto resuelve a `src/modules/domain/entities/MenuItem`, ruta inexistente.

## Impacto
La vista `/menus` crashea inmediatamente.
Bloquea la configuración del menú del sistema.

## Criterio de Corrección
Corregir el import en `MenuItemTree.vue`.
- Incorrecto: `../../../domain/entities/MenuItem`
- Correcto: `@domain/entities/MenuItem` o `../../../../domain/entities/MenuItem`

## Verificación
- Navegar a `/menus`.
- La vista debe cargar el árbol de menú sin error.
