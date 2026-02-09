# Routes Inventory (REQ-020)

| Route Path | View Component | Auth Required | Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `/login` | `LoginView.vue` | No | Active | |
| `/` | `DashboardView.vue` | Yes | Active | Dashboard Root |
| `/dashboard` | - | - | **404** | Link points here but route is `/` |
| `/roles` | `RolListView.vue` | Yes | Active | fixed via HF |
| `/roles/nuevo` | `RolForm.vue` | Yes | **404** | Not a direct route |
| `/roles/:id` | `RolForm.vue` | Yes | Active | |
| `/menus` | `MenuItemTree.vue` | Yes | Active | fixed via HF |
| `/operadores` | `OperadorListView.vue` | Yes | Active | |
| `/clientes` | `ClienteListView.vue` | Yes | Active | |
| `/facturacion` | `ComprobanteListView.vue` | Yes | **404** | Menu Group |
| `/comprobantes` | `InvoiceListView.vue` | Yes | Active | |
| `/recibos` | `ReciboListView.vue` | Yes | Active | |
