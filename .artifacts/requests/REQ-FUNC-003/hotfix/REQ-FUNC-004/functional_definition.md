# Definición Funcional: REQ-FUNC-004 (Jerarquía de Menú)

## Contexto
El Sidebar debe renderizar una estructura jerárquica (Árbol) donde existen nodos padres (agrupadores) y nodos hijos (funcionalidades).
La estructura se define en la Base de Datos mediante `parent_id`.

## Problema
Actualmente, el Sidebar renderiza todos los items al mismo nivel (aplanados), ignorando la jerarquía.
Esto causa que "Puntos de Venta", que debería estar dentro de "Configuración", aparezca como un ítem principal.

## Requerimiento
El Frontend debe reconstruir correctamente el árbol de menú basándose en el `parent_id` retornado por el API.

### Criterios de Aceptación
1. **Visual:** Los ítems hijos NO deben ser visibles en el primer nivel del Sidebar.
2. **Interacción:** Los ítems hijos deben ser accesibles solo al expandir su nodo padre.
3. **Datos:** El algoritmo de construcción del árbol debe manejar correctamente los IDs (tipos de datos) y la ausencia de padres (nodos raíz).

## Hipótesis Técnica
El endpoint `/usuarios/me/menu` retorna una lista plana (Flat List).
El composable `useUserMenu.ts` intenta reconstruir el árbol, pero falla la coincidencia de `parent_id` vs `id`.
Posible causa: `parent_id` nulo o discrepancia de tipos (string vs number) en la respuesta JSON.
