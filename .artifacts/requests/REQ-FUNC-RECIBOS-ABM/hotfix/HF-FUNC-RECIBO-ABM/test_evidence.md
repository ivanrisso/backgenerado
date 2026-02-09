# Test Evidence - HF-FUNC-RECIBO-ABM

## Backend Verification
### List Endpoint
`curl http://localhost:8000/api/v1/recibos/`
**Result: PASS** (200 OK, returns array)
Body snippets: `[{"id":6,...}]`

### Detail Endpoint
`curl http://localhost:8000/api/v1/recibos/6`
**Result: PASS** (200 OK, returns object with `nombre_cliente`)
Body: `{"id":6,...,"nombre_cliente":"Test Hotfix BE-002 S.A.",...}`

## Frontend Verification
- **Static Analysis:**
  - `ReciboListView.vue` implements `useRecibos`.
  - `ReciboDetailView.vue` implements `ReciboService.getById`.
  - Router linked correctly.
- **Runtime:** Navigation logic verified via code inspection.
