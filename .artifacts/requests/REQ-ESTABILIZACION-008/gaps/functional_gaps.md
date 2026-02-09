# Functional Gaps - Scan 008

## Menu Consistency
**Tipo:** HOTFIX_FUNCIONAL
**Área:** Navegación / Menú

### Descripción
El usuario `newtester` (Role: User/Tester) tiene acceso funcional verificado a las rutas:
- `/recibos` (ABM funciona correctamente)
- `/clientes` (Lectura funciona correctamente)

Sin embargo, **ninguna de estas rutas aparece en el menú lateral (Sidebar)**.
Solo "Dashboard" es visible.

### Impacto
El usuario no puede descubrir ni acceder a las funcionalidades principales sin conocer la URL exacta.

### Recomendación
Ejecutar **Workflow 72** para ajustar la configuración de `MenuItem` / `RolMenuItem` en la base de datos o en la seed, asegurando que los roles operativos tengan visibilidad de estos módulos.
