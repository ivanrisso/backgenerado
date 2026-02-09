# Implementation Plan - HF-TECH-002

## Problem
1. **Broken Dashboard Link:** Sidebar points to `/dashboard`, but Router expects `/`.
2. **Orphan Items:** Items 26 ("Listado") and 27 ("Facturas") are orphans because their parent, Item 22 ("Comprobantes"), is not assigned to the active user's role (Admin).
3. **Broken Menús Link:** Reported as broken. DB shows `/menus`. Router has `/menus`. Will verify availability.

## Analysis
- **Dashboard:** DB Item 29 has `path='/dashboard'`. Router uses `/`. Fix: Update DB path to `/`.
- **Orphans:** Item 22 exists but is missing in `rolmenuitem` for Role 1 (Admin). Fix: Assign Item 22 to Role 1.

## Proposed Changes
### Database (Data Fix)
#### [MODIFY] [Script](file:///home/irisso/proyectos/facturacion/scripts/fix_hf_tech_002.py)
Create and run a python script to:
1. Update `menuitem` ID 29: set `path = '/'`.
2. Insert into `rolmenuitem`: `(rol_id=1, menu_item_id=22)`.

## Verification Plan
### Automated Tests
- `e2e_verification` in Stage D (Browser).

### Manual Verification
- Login as Admin.
- Verify "Dashboard" link works (goes to Home).
- Verify "Comprobantes" group appears.
- Verify "Listado" and "Facturas" appear under "Comprobantes".
- Verify "Menús" link works.
