# Test Cases: HF-FUNC-DASHBOARD-CONTENT

## Case 1: Landing on Dashboard
- **Actor:** `newtester@gmail.com` (Operador)
- **Action:** Login -> Auto-navigate to `/`.
- **Expected:** View "Bienvenido al Sistema de Facturación". No redirect to `/recibos`.

## Case 2: Navigation Links
- **Actor:** `newtester@gmail.com`
- **Action:** Click "Nuevo Recibo" card.
- **Expected:** Navigate to `/recibos/nuevo`.

## Case 3: Admin User
- **Actor:** `admin@facturacion.local` (Admin) - *Note: Using newtester for simplicity if admin creds unavailable, assuming shared logic.*
- **Action:** Visit `/`.
- **Expected:** See same Dashboard (universal access).
