# CRUD Matrix (UI)

| Entity | List View | Create View | Detail/Edit View | Delete View | Notes |
|Str|Str|Str|Str|Str|Str|
|---|---|---|---|---|---|
| **Recibos** | `ReciboListView` | `ReciboCreateView` | `ReciboDetailView`, `ReciboModifyView` | `ReciboDeleteView` | Full CRUD visible + Print |
| **Comprobantes** | `InvoiceListView` | `InvoiceCreateView` | - | - | Create + List only |
| **Clientes** | `ClienteList` | - | `ClienteTelefonosView` (nested) | - | Appears limited to List/Partial Edit |
| **Usuarios** | `UsuarioList` | - | - | - | List only detected |
| **Roles** | `RolList` | - | - | - | List only detected |
| **Menus** | `MenuItemTree` | - | - | - | Tree View |
| **Maestros** | Multiple Views | - | - | - | Various master tables (Monedas, Paises, etc) |
