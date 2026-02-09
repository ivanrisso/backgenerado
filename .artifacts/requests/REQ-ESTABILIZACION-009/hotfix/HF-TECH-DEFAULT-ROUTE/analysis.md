# Analysis

## Causa Raíz
`frontend/src/router/index.ts`:
```typescript
{
    path: '',
    redirect: '/usuarios'
}
```

## Riesgos
Bajo. Cambio de configuración de ruteo.

## Alternativas
1. Redirect a `/recibos` (Parche rápido, pero asume permisos).
2. Redirect a `/dashboard` (Requiere crear `DashboardView.vue`).
3. Smart Redirect (Requiere lógica en `beforeEnter`).
