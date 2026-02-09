# Analysis: HF-TECH-AUTH-SESSION

## Causa Raíz
Posible mala gestión del token JWT en el cliente HTTP (`axios`) o en el store de Pinia (`auth.ts`).
Si el interceptor de respuesta recibe un 401, redirige agresivamente sin intentar refresh o validar si es un falso positivo.

## Riesgos
Medio. Tocar lógica de auth puede afectar todo el sistema. Se requiere cautela en la condición de logout.

## Componentes Afectados
- `src/modules/Auth/store/auth.ts`
- `src/core/api/httpClient.ts` (estimado)
