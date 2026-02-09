# Functional Definition (PRD) - Dashboard

## Problema Actual
La URL `/` (Dashboard) actualmente redirige a una lista (`/usuarios` o `/recibos`). No existe una vista de "Tablero de Control" real.

## Comportamiento Esperado (Propuesta)
Implementar una vista **DashboardView.vue** simple que se muestre en `/`.

### Contenido Mínimo (MVP)
1. **Header:** "Dashboard / Resumen".
2. **Widgets (Simulados o Reales):**
   - Accesos directos a "Nuevo Comprobante", "Nuevo Recibo", "Nuevo Cliente".
   - (Opcional) Tarjetas simples: "Total Comprobantes", "Total Recibos".

### Reglas de Negocio
- Visible para todos los usuarios autenticados.
- El contenido de los widgets puede depender del rol.
- **NO** debe redirigir a `/recibos` ni `/usuarios`.

## Alcance
- Crear `DashboardView.vue`.
- Actualizar `router/index.ts` para usar esta vista en `/`.
