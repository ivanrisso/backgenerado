# UI Runtime Errors

**Status:** CRITICAL ISSUES FOUND

## Critical Errors
1. **Import Error (`/domicilios`)**
   - **Type:** Module Resolution / Vite
   - **Details:** Failed to resolve import `useDomicilios` from `src/modules/Maestros/ui/views/DomicilioView.vue`.
   - **Impact:** View crash. Navigation blocked.

2. **Route 404 (`/dashboard`)**
   - **Type:** Router Configuration
   - **Details:** Sidebar link points to `/dashboard` but router does not define it (likely defined as `/` alias but link uses name/path mismatch).
   - **Impact:** User lands on 404.

3. **Route 404 (`/menu-items`)**
   - **Type:** Router Configuration
   - **Details:** Sidebar link "Menús" points to `/menu-items` (or similar) which is not registered.
   - **Impact:** Feature inaccessible.

## Warnings
- **Orphan Menu Items:** IDs 26, 27 point to missing Parent ID 22.
