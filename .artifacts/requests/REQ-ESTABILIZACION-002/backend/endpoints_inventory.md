# Inventario de Endpoints Backend

**Prefijo:** `/api/v1`

## Auth y RBAC
- `/auth/*` (Login, Me, Refresh)
- `/usuarios`, `/roles`, `/menus`

## Core de Negocio
- `/clientes` (CRUD)
- `/comprobantes` (CRUD, excepto Delete)
- `/comprobantes/full` (Lógica de creación)
- `/cuentacorriente` (Saldo)
- `/recibos` (Pagos)

## Maestros / Configuración
- `/monedas`, `/ivas`, `/conceptos`, `/tipos-comprobante`, `/paises`, etc. (CRUD)
- `/afip/config`
- `/puntos-venta`
