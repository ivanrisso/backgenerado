# Backend Endpoints Inventory

## Core
- `auth_routes.py`: Login, Refresh
- `usuario_routes.py`: CRUD Users, `/me/menu` (New)
- `rol_routes.py`: Roles
- `menuitem_routes.py`: Menu Items

## Facturación
- `comprobante_routes.py`: Invoices
- `comprobante_full_routes.py`: Full Invoice Flow
- `recibo_routes.py`: Receipts (Tesoreria)
- `punto_venta_routes.py`
- `tipocomprobante_routes.py`
- `concepto_routes.py`
- `moneda_routes.py`
- `iva_routes.py`

## Clientes
- `cliente_routes.py`: Clients
- `domicilio_routes.py`
- `telefono_routes.py`
- `cuentacorriente_routes.py`

## Maestros / Geo
- `pais_routes.py`
- `provincia_routes.py`
- `localidad_routes.py`

## Configuration
- `afip_config_routes.py`

## Protection
Most routes use `require_roles` dependency for RBAC.
`usuario_routes.py` recently patched to expose public `/me/menu`.
