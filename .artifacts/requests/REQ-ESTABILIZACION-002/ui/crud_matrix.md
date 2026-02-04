# CRUD Matrix

## Modules

### Clientes
- **Entity**: Cliente
- **List View**: `ClienteList.vue`
- **Form View**: `ClienteForm.vue`
- **Operations**:
  - [x] Create (`handleNew` -> `saveCliente`)
  - [x] Read (`loadClientes`)
  - [x] Update (`handleEdit` -> `saveCliente`)
  - [x] Delete (`handleDelete` -> `deleteCliente`)
- **Dependencies**: `useClientes`, `useAuthStore`.

### Facturacion (Comprobantes)
- **Entity**: Comprobante
- **List View**: `InvoiceListView.vue`
- **Form View**: `InvoiceCreateView.vue`
- **Operations**:
  - [x] Create (Navigation to `InvoiceCreateView`)
  - [x] Read (`loadComprobantes`)
  - [ ] Update (Immutable - Expected)
  - [ ] Delete (Immutable - Expected)
- **Dependencies**: `useComprobantes`, `useTiposComprobante`, `useClientes`.

### Tesoreria (Recibos)
- **Entity**: Recibo
- **List View**: Not detected (Accessed via Client View?)
- **Form View**: `ReciboCreateView.vue`
- **Operations**:
  - [x] Create
  - [?] Read (Likely in Account View)
