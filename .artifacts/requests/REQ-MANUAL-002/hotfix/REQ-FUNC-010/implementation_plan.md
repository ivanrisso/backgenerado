# Implementation Plan - HF-FUNC-MENU-ORDER

## Problem
Menu items are displayed in arbitrary order (insertion ID or random), preventing logical organization of the sidebar. User requires configurable order.

## Analysis
- **Current State:** `MenuItem` model lacks an ordering field.
- **Requirement:** Add `orden` attribute to control display sequence.

## Proposed Changes

### Database
#### [MODIFY] `menuitem` Table
- Add column `orden` (INT, Default 0).
- Migration Strategy:
  - Add column.
  - Run update script to set initial `orden` based on current logical structure (e.g., Dashboard=1, Config=99).

### Backend
#### [MODIFY] [menuitem.py](file:///home/irisso/proyectos/facturacion/app/infrastructure/db/models/menuitem.py)
- Add `orden: Mapped[int] = mapped_column(default=0)`

#### [MODIFY] [schemas/menuitem.py](file:///home/irisso/proyectos/facturacion/app/schemas/menuitem.py)
- Add `orden: int` to schemas.

### Frontend
#### [MODIFY] [Sidebar.vue](file:///home/irisso/proyectos/facturacion/frontend/src/components/Sidebar.vue)
- Update logic to sort items by `orden` ascending before rendering.

### Data Migration
#### [NEW] [script](file:///home/irisso/proyectos/facturacion/scripts/migration_add_orden.py)
- Python loop to add column if missing.
- Set default values for known items (Dashboard=0, Comprobantes=10, Tesorería=20, Config=90, Security=100).

## Verification Plan
### Automated
- `inspect_db_menu.py` (updated to show order).

### Manual
- Verify Sidebar order matches defined integers.
- Change order in DB and verify Sidebar updates.
