# UI Menu Coverage & Map

## 1. Mapeo Menú -> Ruta -> Backend

| ID Menú | Etiqueta | Ruta Frontend | Endpoint Backend Principal | Cobertura |
|---------|----------|---------------|----------------------------|-----------|
| `comprobantes` | Comprobantes | `/comprobantes` | `GET /api/v1/comprobantes/` | ✅ |
| `nuevo-comprobante` | Nueva Factura | `/comprobantes/nuevo` | `POST /api/v1/comprobantes/` | ✅ |
| `lista-clientes` | Directorio (Clientes) | `/clientes` | `GET /api/v1/clientes/` | ✅ |
| `cuenta-corriente` | Cuenta Corriente | `/cuentacorriente` | `GET /api/v1/cuentacorrientes/` | ✅ |
| `deudores` | Saldos Deudores | `/clientes/deudores` | `GET /api/v1/clientes/deudores` | ✅ |
| `monedas` | Monedas | `/monedas` | `GET /api/v1/monedas/` | ✅ |
| `ivas` | Tasas IVA | `/ivas` | `GET /api/v1/ivas/` | ✅ |
| `conceptos` | Conceptos | `/conceptos` | `GET /api/v1/conceptos/` | ✅ |
| `paises` | Países | `/paises` | `GET /api/v1/paises/` | ✅ |
| `provincias` | Provincias | `/provincias` | `GET /api/v1/provincias/` | ✅ |
| `localidades` | Localidades | `/localidades` | `GET /api/v1/localidades/` | ✅ |
| `usuarios` | Usuarios | `/usuarios` | `GET /api/v1/usuarios/` | ✅ |
| `roles` | Roles | `/roles` | `GET /api/v1/rols/` | ✅ |
| `menus` | Menús | `/menus` | `GET /api/v1/menuitems/` | ✅ |

## 2. Rutas Maestras sin Menú Directo (Configurables)
*Estas rutas existen en router pero no en menú principal (se accede desde submenu Maestros o similar)*
- `/tipodoms` -> `TiposDom` (Posible huérfano de UI si no está en menú Maestros)
- `/tipotels` -> `TiposTel` (Posible huérfano)
- `/operadores` -> `Operadores` (Posible huérfano)
- `/domicilios` -> `Domicilio` (Generalmente sub-recurso de Cliente, OK)
- `/telefonos` -> `Telefono` (Sub-recurso de Cliente, OK)
- `/tipodocs` -> `TipoDoc` (Posible huérfano)
- `/condiciones-tributarias` -> `CondicionTributaria` (Posible huérfano)

> **Nota:** Se detectaron rutas de maestros (`tipodocs`, `condiciones-tributarias`, etc) que tienen vista Vue pero no están explícitamente en el array `children` de Maestros en `menu.ts` (solo están hasta localidades). Esto indica **UI Orphans**.

## 3. Discrepancias Detectadas
1. **Tipos de Datos Faltantes en Menú**: `TipoDoc`, `TipoDom`, `TipoTel`, `CondicionesTributarias`, `TipoImpuesto`, `TipoComprobante` tienen Vistas (`.vue`) y Rutas (`router`), pero **no aparecen** en `menuConfig` bajo "Maestros".
2. **Access Control**: Las rutas de menú están protegidas por roles (`admin`), y los endpoints también (`admin`). Consistente.
