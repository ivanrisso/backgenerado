# Routes Inventory (REQ-019)

| Route Path | View Component | Auth Required | Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `/login` | `LoginView.vue` | No | Active | |
| `/` | `DashboardView.vue` | Yes | Active | Dashboard is at root |
| `/dashboard` | - | - | **404** | Misconfigured link? |
| `/roles` | `RolListView.vue` | Yes | Active | |
| `/roles/nuevo` | `RolForm.vue` | Yes | **404** | Managed internally or modal? |
| `/roles/:id` | `RolForm.vue` | Yes | Active | |
| `/menus` | `MenuItemTree.vue` | Yes | Active | **Fixed via HF** |
| `/operadores` | `OperadorListView.vue` | Yes | Active | |
| `/clientes` | `ClienteListView.vue` | Yes | Active | |
| `/facturacion` | `ComprobanteListView.vue` | Yes | **404** | Group/Dropdown? |
| `/comprobantes` | `InvoiceListView.vue` | Yes | Active | Correct route for Invoices |
| `/recibos` | `ReciboListView.vue` | Yes | Active | |
