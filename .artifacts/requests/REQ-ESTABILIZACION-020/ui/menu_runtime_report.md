# Menu Runtime Report (REQ-020)

**Fecha:** 2026-02-05

## Resumen de Navegación
| Item | Ruta Objetivo | Estado | Observación |
| :--- | :--- | :--- | :--- |
| **Dashboard** | `/` | **PASS** | Link correcto. |
| **Facturación** | n/a | **PASS** | Colapsable Ok. |
| - Comprobantes | `/comprobantes` | **PASS** | Ok. |
| **Tesorería** | n/a | **PASS** | Colapsable Ok. |
| - Recibos | `/recibos` | **PASS** | Ok. |
| **Clientes** | n/a | **PASS** | Colapsable Ok. |
| - Directorio | `/clientes` | **PASS** | Ok. |
| - Cta. Corriente | `/cuentacorriente` | **PASS** | Ok. |
| - Saldos Deudores| `/clientes/deudores` | **PASS** | Ok. |
| **Maestros** | n/a | **PASS** | Colapsable Ok. |
| - Monedas | `/monedas` | **PASS** | Ok. |
| - Países/Prov/Loc | `/paises`... | **PASS** | Ok. |
| - Tipos Teléfono | `/tipotels` | **PASS** | Ok. |
| - **Tipos Domicilio**| `/tipodoms` | **FAIL** | **Falta en Sidebar**. Existe en DB (`/menus`). |
| - **Domicilios** | `/domicilios` | **FAIL** | **Falta en Sidebar**. Existe en DB (`/menus`). |
| - **Teléfonos** | `/telefonos` | **FAIL** | **Falta en Sidebar**. Existe en DB (`/menus`). |
| - **Puntos Venta** | n/a | **FAIL** | **GAP TOTAL**. No existe en DB ni Sidebar. |
| **Sistema** | n/a | **PASS** | Colapsable Ok. |
| - Usuarios | `/usuarios` | **PASS** | Ok. |
| - Roles | `/roles` | **PASS** | Ok. |
| - Menús | `/menus` | **PASS** | Ok. |

## Hallazgos Críticos
1. **Inconsistencia Sidebar vs DB:** `Domicilios` y otros están configurados como activos en `/menus` pero el componente `Sidebar` no los renderiza. Probable defecto en el loop de rendering o permisos.
2. **Módulo Faltante:** `Puntos de Venta` es un requerimiento funcional no implementado.
