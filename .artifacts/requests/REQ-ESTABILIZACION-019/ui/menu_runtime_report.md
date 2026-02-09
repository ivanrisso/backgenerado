# Menu Runtime Report (REQ-019)

**Fecha:** 2026-02-05

## Resumen de Navegación
| Item | Ruta Objetivo | Estado | Observación |
| :--- | :--- | :--- | :--- |
| **Dashboard** | `/` | **PASS** | Ok. |
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
| - Ivas | `/ivas` | **PASS** | Ok. |
| - Conceptos | `/conceptos` | **PASS** | Ok. |
| - Países | `/paises` | **PASS** | Ok. |
| - Provincias | `/provincias` | **PASS** | Ok. |
| - Localidades | `/localidades` | **PASS** | Ok. |
| - Tipos Teléfono | `/tipotelef` | **PASS** | Ok. |
| - Tipos Documento| `/tipodocs` | **PASS** | Ok. |
| - Cond. Tributaria| `/condtributaria` | **PASS** | Ok. |
| - **Tipos Domicilio**| `/tipodomis` | **FAIL** | **Falta en Sidebar**. Existe en DB/Gestión. |
| - **Domicilios** | `/domicilios` | **FAIL** | **Falta en Sidebar**. Existe en DB/Gestión. |
| - **Teléfonos** | `/telefonos` | **FAIL** | **Falta en Sidebar**. Existe en DB/Gestión. |
| - **Puntos Venta** | n/a | **FAIL** | **Inexistente**. No está en Sidebar ni en Gestión de Menú. |
| **Sistema** | n/a | **PASS** | Colapsable Ok. |
| - Usuarios | `/usuarios` | **PASS** | Ok. |
| - Roles | `/roles` | **PASS** | Ok. |
| - Menús | `/menus` | **PASS** | Ok. |

## Hallazgos Críticos (Gaps)
1. **Items Ocultos:** `Domicilios`, `Teléfonos` y `Tipos Domicilio` están configurados en el sistema pero no se renderizan en el Sidebar (posible falta de rol asignado o hardcoding en Sidebar).
2. **Módulo Faltante:** `Puntos de Venta` parece no estar implementado o registrado en el menú.
