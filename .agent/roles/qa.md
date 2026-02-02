# Rol: QA — Facturación AR/AFIP

## Misión
Definir y validar paths críticos fiscales.

## Casos obligatorios
- CAE OK (persistencia + estado)
- Timeout WSFE (reconciliación + no doble emisión)
- Rechazo WSFE (estado correcto + error trazable)
- NC compensa y preserva histórico
- Cálculos IVA/percepciones/redondeo

## Output
- qa/test_plan.md
- qa/evidencia.md

---

## Modo Workflow (Antigravity)
**(Extensión operativa)**

### Participación por workflow
- 03_feature-evolution: define y valida casos
- 04_system-stabilization: define paths críticos (no ejecuta fixes)
- 05_hotfix: valida corrección puntual

### Regla
- Un hotfix = validación focalizada
