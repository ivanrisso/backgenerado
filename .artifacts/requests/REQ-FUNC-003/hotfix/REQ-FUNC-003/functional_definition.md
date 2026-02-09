# Definición Funcional: REQ-FUNC-003 (Menú Dinámico)

## Contexto
Actualmente, el FrontEnd utiliza un archivo de configuración estático (`config/menu.ts`) para renderizar el Sidebar.
Existe un módulo de Backend y FrontEnd ("Maestros -> Menús") que permite gestionar (Crear, Editar, Eliminar) items de menú en la base de datos.

## Problema
Cualquier cambio realizado en la Base de Datos (CRUD de Menús) es ignorado por el Sidebar, ya que este lee el archivo estático.
Esto provoca una desconexión total entre la configuración administrativa y la navegación real del usuario.

## Requerimiento
El Sidebar debe dejar de depender de `config/menu.ts` y debe consumir la estructura de menú provista por el Backend (vía API).

### Comportamiento Esperado
1. **Login:** Al autenticarse, la aplicación debe obtener la lista de menús permitidos para el usuario (o todos y filtrar localmente, aunque idealmente el backend ya filtra).
2. **Navegación:** El Sidebar debe renderizar los items basándose en la respuesta del API.
3. **Roles:** La visibilidad debe respetar los permisos asignados en el Backend (Tabla `RolMenuItem`).
4. **Fallback:** Si el API falla, se puede considerar un fallback estático (opcional, pero recomendado para estabilidad), o mostrar error.

## Alcance del Hotfix
- **Frontend:** Modificar `Sidebar.vue` o crear un Store (`useMenuStore`) para cargar items desde `/api/menus` (o endpoint equivalente).
- **Backend:** Asegurar que existe un endpoint que retorne el árbol de menú (o lista plana con parent_id) compatible.

## Criterios de Aceptación
- Un ítem agregado vía CRUD (ej: "Nuevo Modulo") debe aparecer en el Sidebar tras refrescar la página.
- Un ítem deshabilitado/eliminado no debe aparecer.
