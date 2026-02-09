# Functional Definition: HF-FUNC-MENU-FE-ORDER-COLLAPSE

## 1. Comportamiento Actual (Incorrecto)
El sistema de menús en el frontend presenta deficiencias funcionales que afectan la usabilidad y la administración:

1.  **Gestión (CRUD)**:
    - Los menús padres **no son colapsables**. Se muestran siempre expandidos o no permiten distinguir claramente su jerarquía visual agrupada.
    - El orden de los ítems en el listado es arbitrario (o por inserción), no configurable por el usuario.

2.  **Navegación (Sidebar)**:
    - Los ítems hijos pueden renderizarse como niveles superiores si la jerarquía no se respeta estrictamente.
    - El orden visual de los elementos no sigue una lógica de negocio definida.

## 2. Comportamiento Esperado (Correcto)
El frontend debe comportarse de la siguiente manera:

1.  **Gestión (CRUD) - Página `/menus`**:
    - **Jerarquía Visual**: Los menús padres deben permitir **colapsar y expandir** sus hijos para facilitar la gestión.
    - **Ordenamiento Configurable**: El usuario debe poder modificar el campo `orden` (ya existente en backend) directamente desde la interfaz.
        - Ordenar padres entre sí.
        - Ordenar hijos dentro de su padre.
    
2.  **Navegación (Sidebar)**:
    - **Respeto de Jerarquía**: El Sidebar debe renderizar estrictamente la estructura árbol. Un hijo nunca debe aparecer fuera de su padre.
    - **Respeto de Orden**: Los elementos deben aparecer ordenados ascendentemente por el campo `orden`.

## 3. Casos Borde y Validaciones
- **Menú sin Hijos**: Debe comportarse como un ítem simple (sin flecha de colapso).
- **Menú Huérfano**: Si un ítem tiene `parent_id` pero el padre no existe, debe manejarse con un fallback visual (ej. al final de la lista raíz) para no perder acceso, o filtrarse según regla de negocio (actualmente se muestra).
- **Orden Duplicado**: Si dos ítems tienen el mismo `orden`, se desempatará por `ID` o alfabéticamente para mantener consistencia visual.

## 4. Alcance
- **Incluye**: Modificación de `Menus.vue` (o componente equivalente de administración) y verificación de `Sidebar.vue`.
- **Excluye**: Cambios en API Backend (la API ya provee `orden`).
