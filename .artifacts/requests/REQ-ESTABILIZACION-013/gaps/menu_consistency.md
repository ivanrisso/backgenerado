# Menu Consistency Report

## Methodology
Verified conformance between:
1.  **Backend Config (Observed/Referenced w/ Frontend)**
2.  **Frontend Routes (`router/index.ts`)**
3.  **Visual Menu (`menu.ts`)**
4.  **Strict Runtime check (`ui-runtime-menu-scan`)**

## Results (Admin Role)
| Module | Menu Item | Route | Backend Support | Status |
|---|---|---|---|---|
| **Tesorería** | Recibos | `/recibos` | `GET /api/v1/recibos` | **CONSISTENT** |
| **Tesorería** | Nuevo Recibo | `/recibos/nuevo` | `POST /api/v1/recibos` | **CONSISTENT** |
| **Facturación** | Comprobantes | `/comprobantes` | `GET /api/v1/comprobantes` | **CONSISTENT** |
| **Clientes** | Directorio | `/clientes` | `GET /api/v1/clientes` | **CONSISTENT** |
| **Maestros** | Monedas | `/monedas` | `GET /api/v1/monedas` | **CONSISTENT** |

## Gaps Detected
- None. All visible items lead to functional routes supported by endpoints.
