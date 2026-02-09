# Plan de Implementación: HF-FUNC-001 (Puntos de Venta)

## Objetivo
Habilitar el acceso funcional al módulo de "Puntos de Venta" en el frontend.

## Cambios Propuestos

### 1. Frontend: Verificación y Activación de Ruta
**Archivo:** `frontend/src/router/index.ts`
- Verificar que la ruta `/puntos-venta` esté definida.
- Si está comentada o faltante, agregarla apuntando a `Maestros/ui/views/PuntoVentaList.vue`.

**Archivo:** `frontend/src/modules/Maestros/ui/views/PuntoVentaList.vue`
- Verificar existencia. Si es un archivo vacío o no existe, crear un scafold básico (Listado + Botón Nuevo).

### 2. Backend/DB: Inserción de Menú
**Script:** `scripts/insert_punto_venta_menu.py` (NUEVO)
- Buscar el `menu_item` padre "Maestros".
- Insertar nuevo `menu_item`:
  - Label: "Puntos de Venta"
  - Path: `/puntos-venta`
  - Orden: Al final de la lista de maestros.
- Asignar permisos al Rol `Admin`.

## Verificación
1. Ejecutar script de inserción.
2. Login como Admin.
3. Verificar aparición en Sidebar "Maestros".
4. Navegar y verificar carga de vista.

## Rollback
- Script reverso para eliminar el `menu_item` por Path `/puntos-venta`.
