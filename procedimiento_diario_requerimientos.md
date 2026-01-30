# Procedimiento Diario — SDLC con Antigravity (Post-Bootstrap)

Este documento define **el procedimiento estándar y canónico** para crear, ejecutar y cerrar requerimientos (REQ) en el proyecto usando Antigravity como **AI-First SDLC**, **una vez finalizada la fase de bootstrap**.

> **Objetivo:** garantizar que cualquier cambio (feature, mejora o ajuste) se ejecute de forma **segura, repetible, auditable y con CI obligatorio**, sin romper calidad ni fiscalidad.

---

## 🧭 Principio Rector

> **Documentar → Planificar → Aprobar → Ejecutar → Validar (CI) → Evidenciar → Cerrar**

Nunca ejecutar código sin:

* REQ creado
* Plan aprobado
* Evidencia registrada
* CI verde

---

## 🧱 Nota clave sobre Bootstrap (MUY IMPORTANTE)

El **bootstrap del proyecto ya fue ejecutado y cerrado** (Baseline, Quality, CI).

Esto implica que:

* ❌ **NO** se vuelve a ejecutar `02_quality-bootstrap.md`.
* ❌ **NO** se recrea CI ni testing base.
* ❌ **NO** se ajusta infraestructura de forma recurrente.
* ✅ Todo nuevo requerimiento entra **directamente en fase de evolución funcional**.

> **El CI verde marca el fin del bootstrap y el inicio del desarrollo normal.**

---

## 0️⃣ Pregunta Inicial (obligatoria)

**¿El cambio toca código productivo o configuración versionada?**

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
Backend / Frontend / DB / AFIP.

## Casos relevantes
Casos funcionales importantes.
```

---

## 2️⃣ Elegir el workflow correcto

| Tipo de cambio                  | Workflow a ejecutar        |
| ------------------------------- | -------------------------- |
| Feature / Mejora funcional      | `03_feature-evolution.md`  |
| Cambio fiscal AFIP              | `03_feature-evolution.md`  |
| Cambio de infraestructura MAYOR | Bootstrap explícito (raro) |
| Documentación / PRD / ADR       | Ninguno                    |

📌 **Reglas:**

* Todo REQ funcional entra por `03_feature-evolution.md`.
* Infraestructura solo se toca con un **REQ explícito de tipo bootstrap**.
* CI y calidad base ya están congelados.

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
- Ajustar o agregar tests si corresponde.

Objetivo:
- Implementar el REQ.
- Generar evidencia en:
  `.artifacts/requests/REQ-XXXX/qa/evidencia.md`.

Al finalizar:
- Aplicar gate_delivery.
- Crear `status.md` y `closure_checklist.md`.
```

---

## 4️⃣ Aprobar el plan (paso obligatorio)

Antigravity **siempre responde primero con un plan**.

### ✅ Respuesta estándar de aprobación

```txt
Plan aprobado.

Procedé con la ejecución siguiendo el plan definido.
Respetar restricciones y estándares existentes.
```

⚠️ **Nunca ejecutar sin esta aprobación explícita.**

---

## 5️⃣ Ejecución e integración continua

Durante esta fase:

**Antigravity:**

* Implementa cambios de código.
* Actualiza o crea tests.
* Deja el repositorio listo para versionar.

**Usuario (humano):**

```bash
git add .
git commit -m "feat: REQ-XXXX <descripción>"
git push
```

**GitHub Actions:**

* Ejecuta CI automáticamente.
* Corre tests backend y frontend.
* Bloquea el cierre si CI falla.

---

## 6️⃣ Verificación de cierre

Confirmar que existen:

```
REQ-XXXX/
  qa/
    evidencia.md
  status.md
  closure_checklist.md
```

Y que:

* CI está **verde en runner remoto**.
* Gate Delivery = **PASS**.

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
6. Bootstrap **no se repite**.

---

## 🧠 Resumen Ultra Corto (Post-it mental)

```
Crear REQ
↓
03_feature-evolution.md
↓
Aprobar plan
↓
Implementar
↓
Commit / Push
↓
CI verde
↓
Gate PASS
↓
Cerrar REQ
```

---

**Este documento es la fuente de verdad para el trabajo diario del proyecto en fase post-bootstrap.**
