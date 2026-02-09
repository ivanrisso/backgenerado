# Analysis: HF-TECH-SIDEBAR-GAPS

## Problem
The Sidebar is missing links for existing modules:
- `Domicilios` (`/domicilios`)
- `Teléfonos` (`/telefonos`)
- `Tipos Domicilio` (`/tipodoms`)
Also, the `Dashboard` link points to `/dashboard` which 404s (should be `/`).

## Root Cause
Likely hardcoded list in `Sidebar.vue` or `useSidebar` composable that hasn't been updated to reflect all routes in `router/index.ts`.

## Solution
1. Modify `Sidebar.vue` (or equivalent).
2. Add missing items to the structure.
3. Correct `Dashboard` link.
