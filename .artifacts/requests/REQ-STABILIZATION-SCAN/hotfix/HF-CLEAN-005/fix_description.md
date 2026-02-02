# 🔧 Fix Description — HF-CLEAN-005

## Contexto
Reporte de Deudores (`/clientes/deudores`).

## Problema Detectado
Crash JS: `repository.getDeudores is not a function`.

## Causa Raíz
Falta de implementación del método en `AxiosClienteRepository`, aunque estaba siendo llamado por el composable.

## Alcance de la Corrección
- Actualización de `IClienteRepository`.
- Implementación de `getDeudores()` en `AxiosClienteRepository`.
- Limpieza de tipos en `useClientes`.

## Validación
- Carga correcta de `/clientes/deudores`.
- Mensaje "No se encontraron clientes con deuda" o listado válido.
