# Backend Inventory (REQ-019)

Derived from Frontend usage.

| Endpoint | Method | Frontend Module | Usage |
| :--- | :--- | :--- | :--- |
| `/auth/login` | POST | Auth | Login |
| `/auth/me` | GET | Auth | Session Rehydration |
| `/roles` | CRUD | Auth | Role Management |
| `/menuitems` | CRUD | Auth | Menu Management |
| `/comprobantes` | CRUD | Facturacion | Invoices |
| `/recibos` | CRUD | Tesoreria | Receipts |
| `/clientes` | CRUD | Clientes | Clients |
| `/maestros/*` | GET | Maestros | Dropdowns (Paises, Provincias, etc) |
