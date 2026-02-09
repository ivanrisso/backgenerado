# Reporte de Carga de Vistas (Scan REQ-020)

**Fecha:** 2026-02-05

| Ruta | Estado | Observación |
| :--- | :--- | :--- |
| `/` (Dashboard) | **PASS** | Carga correctamente. |
| `/roles` | **PASS** | Carga lista de roles. |
| `/menus` | **PASS** | Carga árbol de menú. Hotfix verificado. |
| `/usuarios` | **PASS** | Carga lista de usuarios. |
| `/clientes` | **PASS** | Carga lista de clientes. |
| `/recibos` | **PASS** | Carga lista de recibos. |
| `/comprobantes` | **PASS** | Carga lista de facturas. |
| `/dashboard` | **FAIL** | 404 - Ruta inexistente (Dashboard es `/`). |
| `/roles/nuevo` | **FAIL** | 404 - Ruta no registrada explícitamente. |
| `/facturacion` | **FAIL** | 404 - Grupo de menú sin vista propia. |

## Hallazgos Técnicos
1. **Rutas fantasma**: El sistema intenta navegar a `/dashboard` en algunos contextos, pero la ruta base es `/`.
2. **Estabilidad**: Las vistas principales son estables.
