# 📘 README de Gobierno de Workflows

## Propósito del Documento

Este README define el **modelo de gobierno operativo y técnico** del sistema
mediante workflows encadenados, con reglas claras de:

- cuándo se ejecuta cada workflow
- qué tipo de problemas aborda
- qué puede y qué NO puede hacer
- cómo se relacionan entre sí

Este documento es la **fuente de verdad** para:
- Arquitectura
- Estabilización
- Corrección técnica
- Corrección funcional
- Evolución del sistema

---

## Principios de Gobierno (NO negociables)

1. **Nada se corrige sin haber sido detectado y clasificado.**
2. **La arquitectura manda sobre la implementación.**
3. **Un workflow no hace el trabajo de otro.**
4. **Todo cambio deja evidencia persistente.**
5. **Sin Gate PASS, no hay avance.**

---

## Mapa General de Workflows

```text
Workflow 10 — System Architecture Definition (SAD)
                ↓
Workflow 70 — Stabilization Scan
                ↓
        +---------------------+
        |                     |
        v                     v
Workflow 71              Workflow 72
Hotfix Técnico        Hotfix Funcional

