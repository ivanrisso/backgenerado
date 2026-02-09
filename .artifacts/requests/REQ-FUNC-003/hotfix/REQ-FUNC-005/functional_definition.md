# Definición Funcional: REQ-FUNC-005 (Agrupación Seguridad)

## Contexto
El módulo de Seguridad contiene las opciones: Usuarios, Roles y Menús.
Estas opciones deben estar agrupadas bajo un ítem padre "Seguridad" para mantener el orden en el sidebar.

## Problema
Actualmente, "Usuarios", "Roles" y "Menús" aparecen en el primer nivel del sidebar.
"Seguridad" no aparece o no actúa como agrupador.

## Requerimiento
1. Existencia del ítem padre "Seguridad" (sin ruta de navegación, solo desplegable).
2. Los ítems "Usuarios", "Roles" y "Menús" deben tener `parent_id` apuntando a "Seguridad".
3. El frontend debe renderizar "Seguridad" como un grupo colapsable.

## Criterios de Aceptación
- Visual: "Seguridad" aparece en el sidebar.
- Visual: "Usuarios", "Roles", "Menús" están ocultos por defecto.
- Interacción: Al hacer clic en "Seguridad", se despliegan las opciones hijas.
