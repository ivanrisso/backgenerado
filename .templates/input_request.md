# REQ-ID: REQ-STABILIZATION-SCAN (Cambiar nombre de cada corrida)

# Workflow: 70 — Stabilization Scan

## Contexto
Sistema de facturación AR en desarrollo local.
Se detectan errores de navegación, carga de vistas y CRU(D).

## Objetivo
Detectar y documentar **errores técnicos** que impidan:
- Navegación completa
- Carga de vistas lazy-loaded
- Ejecución de CRU(D) sin crash

## Alcance
- Frontend Vue 3 + Vite
- Backend FastAPI
- Autenticación JWT
- Módulos Maestros, Clientes, Facturación

## Fuera de alcance
- Cambios funcionales
- Reglas de negocio
- Refactors
- UX

## Reglas de negocio
N/A (workflow técnico)

## AFIP / Fiscalidad
No aplicar cambios fiscales.
Solo validar estabilidad técnica.

## Criterios de aceptación
- Todas las rutas cargan o fallan de forma documentada
- Hotfixes técnicos identificados y clasificados
- ORDER.md generado

## Riesgos / Supuestos
- Navegador puede no estar disponible (degradar a static)
- CI puede no ejecutarse en local

## Notas técnicas
Base URL: http://localhost:5173
Backend: http://localhost:8000
