# Procedimiento Diario — SDLC con Antigravity

Este documento resume **el procedimiento estándar** para crear, ejecutar y cerrar requerimientos (REQ) en el proyecto usando Antigravity como **AI-First SDLC**.

> **Objetivo:** que cualquier nuevo cambio (feature, mejora, infra) se ejecute de forma **repetible, segura y auditable**, sin romper CI ni fiscalidad.

---

## 🧭 Principio Rector

> **Documentar → Planificar → Aprobar → Ejecutar → Evidenciar → Cerrar**

Nunca ejecutar código sin:

* REQ creado
* Plan aprobado
* Evidencia

---

## 0️⃣ Pregunta Inicial (obligatoria)

**¿El cambio toca código productivo o infraestructura versionada?**

* ❌ No → No corresponde ejecutar workflows (documentación pura).
* ✅ Sí → Continuar con el procedimiento.

---

## 1️⃣ Crear un nuevo REQ (siempre manual)

### 📍 Ubicación

```
.artifacts/requests/REQ-XXXX/
```

Usar el próximo identificador disponible.

---

### 📄 Archivo obligatorio — `input.md`

```md
# REQ-ID: REQ-XXXX — <Título corto>

## Contexto
Descripción breve del problema u oportunidad.

## Objetivo
Qué se quiere lograr.

## Alcance
Qué incluye el cambio.

## Fuera de alcance
Qué NO se va a tocar.

## Restricciones
- No romper CI.
- No usar credenciales reales.
- Cumplir normas AFIP si aplica.

## Criterios de aceptación
- Funcionalidad implementada.
- Tests pasan en CI.
```

---

### 📄 Archivo recomendado — `prd.md`

```md
# PRD — REQ-XXXX

## Resumen funcional
Qué cambia para el usuario o sistema.

## Impacto técnico
Backend / Frontend / AFIP / DB.

## Casos relevantes
Solo los casos importantes.
```

---

## 2️⃣ Elegir el workflow correcto

| Tipo de cambio                  | Workflow a ejecutar                                     |
| ------------------------------- | ------------------------------------------------------- |
| Feature / Mejora funcional      | `03_feature-evolution.md`                               |
| Cambio fiscal AFIP              | `03_feature-evolution.md` + `04_afip-reconciliation.md` |
| Infra / CI / tooling            | `03_feature-evolution.md`                               |
| Definición de estándares (raro) | `02_quality-bootstrap.md`                               |

📌 **Regla:** Todo lo que toca código → `03_feature-evolution.md`.

---

## 3️⃣ Ejecutar el workflow (Antigravity)

### 📍 Dónde

Antigravity → **Orchestrator (Planning)**

### 🧠 Prompt base

```txt
Ejecutá el workflow `03_feature-evolution.md` para `REQ-XXXX`.

Contexto:
- El proyecto cuenta con CI y testing activo.

Restricciones:
- No romper CI.
- No usar servicios externos reales.
- Agregar o ajustar tests si corresponde.

Objetivo:
- Implementar el REQ.
- Guardar evidencia en:
  `.artifacts/requests/REQ-XXXX/qa/evidencia.md`.

Al finalizar:
- Aplicar gate_delivery.
- Crear `status.md` y `closure_checklist.md`.
```

---

## 4️⃣ Aprobar el plan (paso obligatorio)

Antigravity **siempre** responde primero con un plan.

### ✅ Respuesta estándar de aprobación

```txt
Plan aprobado.

Procedé con la ejecución siguiendo el plan definido.
Respetar restricciones y estándares existentes.
```

⚠️ **Nunca** dejar ejecutar sin esta aprobación explícita.

---

## 5️⃣ Ejecución

Antigravity ejecuta automáticamente:

* Cambios de código
* Tests
* CI
* Evidencia

👉 El usuario **no interviene** durante esta fase.

---

## 6️⃣ Verificación de cierre

Al finalizar, verificar que existan:

```
REQ-XXXX/
  qa/
    evidencia.md
  status.md
  closure_checklist.md
```

Y que:

* CI esté verde
* Gate Delivery = PASS

---

## 7️⃣ Cerrar el REQ

### 📄 `status.md`

```md
# Status — REQ-XXXX

Estado: ✅ CERRADO
Fecha: YYYY-MM-DD
Cerrado por: Orchestrator (Antigravity)

## Gate aplicado
- Checklist: `.agent/checklists/gate_delivery.md`
- Resultado: ✅ PASS

## Evidencia
- `qa/evidencia.md`
```

### 📄 `closure_checklist.md`

```md
# Closure Checklist — REQ-XXXX

- [x] Código implementado
- [x] Tests ejecutados
- [x] CI verde
- [x] Evidencia registrada
- [x] Gate PASS
```

---

## 🔐 Reglas de Oro (no romper nunca)

1. Un REQ = una ejecución de workflow.
2. REQ cerrado **no se re-ejecuta**.
3. Sin `input.md` no hay ejecución.
4. Sin CI verde no se cierra.
5. AFIP real **jamás** en tests.

---

## 🧠 Resumen Ultra Corto (Post-it mental)

```
Crear REQ
↓
Elegir workflow
↓
Ejecutar (Orchestrator)
↓
Aprobar plan
↓
Ejecutar
↓
Evidencia + Gate
↓
Cerrar REQ
```

---

**Este procedimiento es la fuente de verdad para el trabajo diario del proyecto.**
