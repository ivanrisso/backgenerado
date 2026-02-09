# Menu Runtime Report (Skill: ui-runtime-menu-scan EXHAUSTIVE)

**Role:** Admin
**Date:** 2026-02-05
**Protocol:** Dashboard -> Expand -> Click -> Verify -> Dashboard

| Module | Item | Route | Status | Notes |
|---|---|---|---|---|
| **Facturación** | Comprobantes | `/comprobantes` | ✅ PASS | |
| **Tesorería** | Recibos | `/recibos` | ✅ PASS | |
| | Nuevo Recibo | `/recibos/nuevo` | ✅ PASS | |
| **Clientes** | Directorio | `/clientes` | ✅ PASS | |
| | Cuenta Corriente | `/cuentacorriente`| ✅ PASS | |
| | Saldos Deudores | `/clientes/deudores`| ✅ PASS | |
| **Maestros** | Monedas | `/monedas` | ✅ PASS | |
| | Tasas IVA | `/ivas` | ✅ PASS | |
| | Tipos Comprobante| `/tipos-comprobante`| ✅ PASS | |
| | Tipos Impuesto | `/tipos-impuesto` | ✅ PASS | |
| | Cond. Tributarias| `/condiciones-tribut`| ✅ PASS | |
| | Conceptos | `/conceptos` | ✅ PASS | |
| | Tipos Documento | `/tipodocs` | ✅ PASS | |
| | Países | `/paises` | ✅ PASS | |
| | Provincias | `/provincias` | ✅ PASS | |
| | Localidades | `/localidades` | ✅ PASS | |
| | Tipos Teléfono | `/tipotels` | ✅ PASS | |
| | Operadores | `/operadores` | ✅ PASS | |
| **Sistema** | Usuarios | `/usuarios` | ✅ PASS | |
| | Roles | `/roles` | ❌ FAIL | **Vite Import Error** |
| | Menús | `/menus` | ❌ FAIL | **Vite Import Error** |

## Conclusion
**Scan Failed.** 2 items in 'Sistema' are broken due to build/import errors.
Coverage: 19/21 Pass (90%).
Strict Completitud Rule: **FAIL**.
