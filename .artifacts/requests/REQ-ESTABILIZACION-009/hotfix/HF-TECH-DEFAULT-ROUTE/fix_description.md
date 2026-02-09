# HF-TECH-DEFAULT-ROUTE: Fix Default Redirect 403

## Problema
La ruta raíz `/` redirige incondicionalmente a `/usuarios`.
La ruta `/usuarios` está protegida (requiere rol `admin`).
Usuarios con rol `Operador` reciben error 403 inmediatamente después de login.

## Impacto
Bloqueo de experiencia de usuario inicial. Sensación de sistema roto.

## Criterio de Corrección
Modificar el redirect default para que:
1. Apunte a una ruta común (ej: `/perfil` o `/recibos`).
2. O implemente lógica condicional.
3. O renderice un Dashboard vacío (`DashboardView`).
