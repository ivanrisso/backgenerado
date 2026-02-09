# Definición Funcional: Puntos de Venta (HF-FUNC-001)

## 1. Comportamiento Actual (Incorrecto)
- No existe acceso funcional a la administración de Puntos de Venta.
- El ítem de menú no aparece en "Maestros".
- No hay rutas registradas para `/puntos-venta` (o similar).

## 2. Comportamiento Esperado (Correcto)

### A. Navegación
- **Menú:** Agregar ítem "Puntos de Venta" dentro del grupo "Maestros".
- **Ruta:** `/puntos-venta` debe cargar el listado de puntos de venta.

### B. Funcionalidad (CRUD Básico)
**Listado:**
- Mostrar tabla con:
  - Número de Punto de Venta (ej. 0001)
  - Tipo de Emisión (Factura Electrónica, etc.)
  - Sucursal o Domicilio asociado
  - Estado (Activo/Inactivo)

**Alta/Edición:**
- Campos requeridos:
  - Número (Numérico, 4-5 dígitos)
  - Descripción / Fantasía
  - Sistema Asociado (FE, Impresora Fiscal, etc.)
  - Domicilio (Dropdown de domicilios)

### C. Reglas de Negocio
- El número de punto de venta debe ser único.
- No se puede eliminar un Punto de Venta si tiene comprobantes asociados (Soft Delete preferido).

## 3. Alcance del Hotfix
- **SÍ:** Agregar ruta, vista de listado y formulario básico (o modal).
- **SÍ:** Integrar al menú lateral.
- **NO:** Integración real con AFIP (eso es configuración técnica, aquí gestionamos la entidad lógica).
