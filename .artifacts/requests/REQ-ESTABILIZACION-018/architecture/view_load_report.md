# View Load Report

| Route | Status | Lazy | Vite/JS Error | Notes |
|---|---|---|---|---|
| `/` | PASS | NO | NO | Dashboard OK |
| `/login` | PASS | NO | NO | Login OK |
| `/usuarios` | PASS | YES | NO | - |
| `/roles` | **FAIL** | YES | **YES** | Import Error: `Rol.ts` |
| `/menus` | **FAIL** | YES | **YES** | Import Error: `useMenuItems` |
| `/clientes` | PASS | YES | NO | - |
| `/clientes/deudores` | PASS | YES | NO | - |
| `/cuentacorriente` | PASS | YES | NO | - |
| `/comprobantes` | PASS | YES | NO | - |
| `/comprobantes/nuevo`| PASS | YES | NO | - |
| `/recibos` | PASS | YES | NO | - |
| `/recibos/nuevo` | PASS | YES | NO | Loads UI (API Error 401 confirmed) |
| `/monedas` | PASS | YES | NO | - |
| `/ivas` | PASS | YES | NO | - |
| `/conceptos` | PASS | YES | NO | - |
| `/puntos-venta` | PASS | YES | NO | - |
| `/tipos-comprobante` | PASS | YES | NO | - |
| `/tipos-impuesto` | PASS | YES | NO | - |
| `/paises` | PASS | YES | NO | - |
| `/provincias` | PASS | YES | NO | - |
| `/localidades` | PASS | YES | NO | - |
| `/tipodoms` | PASS | YES | NO | - |
| `/tipotels` | PASS | YES | NO | - |
| `/tipodocs` | PASS | YES | NO | - |
| `/operadores` | PASS | YES | NO | - |
| `/domicilios` | **FAIL** | YES | **YES** | Import Error: `useDomicilios` |
| `/telefonos` | PASS | YES | NO | - |
| `/condiciones-tributarias` | PASS | YES | NO | - |
| `/config/afip` | PASS | YES | NO | - |
