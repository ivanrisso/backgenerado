# Implementation Plan: HF-FUNC-MENU-FE-ORDER-COLLAPSE

## Goal
Implementar colapso de menús padres y edición de orden en el Frontend.

## Proposed Changes

### 1. Frontend: Domain Entity
- File: `src/domain/entities/MenuItem.ts` (or similar location)
- Action: Add `orden: number` property.

### 2. Frontend: Form Component
- File: `src/modules/Auth/ui/views/MenuItemForm.vue`
- Action:
  - Add `orden` to local `form` state.
  - Add `<input type="number">` for `orden`.
  - Propagate `orden` in submit event.

### 3. Frontend: Tree Component
- File: `src/modules/Auth/ui/views/MenuItemTree.vue`
- Action:
  - Add `expanded` state (Map<id, bool>).
  - Add Toggle Button (Chevron) for parents.
  - Show items sorted by `orden` in the list (visual feedback).

### 4. Frontend: Sidebar
- File: `src/shared/ui/components/Sidebar.vue`
- Action: Verify specific sorting logic (already implemented in previous step, confirm correctness).

## Verification Plan
1.  **Manual Test (CRUD)**:
    - Create Parent "A" (Orden 10), Parent "B" (Orden 5).
    - Verify "B" appears before "A".
    - Create Child "A.1" (Orden 2), "A.2" (Orden 1).
    - Verify "A.2" appears before "A.1".
    - Collapse "A". Verify Children hidden.
2.  **Manual Test (Sidebar)**:
    - Reload Page.
    - Verify Sidebar order matches CRUD configuration.
