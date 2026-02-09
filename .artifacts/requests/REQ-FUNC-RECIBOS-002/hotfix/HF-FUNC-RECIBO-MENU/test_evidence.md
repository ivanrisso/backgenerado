# Test Evidence - HF-FUNC-RECIBO-MENU

## Backend / Database
- **Menu Structure:** updated via `scripts/fix_recibo_menu.py`.
- **Output:** Created 'Tesorería' (ID: 31) and 'Recibos' (ID: 32). Removed 'Nuevo Recibo'.

## Frontend Verification
- **ReciboListView:**
  - `select` implementation verified in code.
  - Action buttons (Print, Modify, Delete) added and linked to routes.
- **Router:**
  - New stub routes (`/imprimir`, `/eliminar`, `/modificar`) registered.
- **Stubs:**
  - `ReciboPrintView.vue`, `ReciboDeleteView.vue`, `ReciboModifyView.vue` created.

## Functional Coverage
- **Select Filter:** Implemented.
- **Actions:** Implemented (Navigation to stubs).
- **Menu:** Integrity restored.
