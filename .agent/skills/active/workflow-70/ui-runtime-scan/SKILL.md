# SKILL — UI Runtime Scan

## Rol autorizado
- **QA**

⚠️ Ningún otro rol puede ejecutar este skill.

---

## Objetivo

Ejecutar una **verificación runtime técnica** de la aplicación frontend
para detectar **errores técnicos observables en ejecución**
que impidan la estabilidad operativa del sistema.

Este skill:
- ✔️ Navega la UI en ejecución
- ✔️ Ejecuta acciones mínimas de uso real
- ✔️ Detecta crashes, errores JS y abortos de navegación
- ❌ NO valida reglas de negocio
- ❌ NO evalúa comportamiento funcional esperado
- ❌ NO clasifica hotfix vs gap
- ❌ NO corrige código

👉 Su **única responsabilidad** es **OBSERVAR y EVIDENCIAR** errores técnicos runtime.

---

## Contexto de ejecución

- Workflow: **70 — Stabilization Scan**
- Stage: **E — Runtime Scan**
- Modo requerido: `execution_mode = hybrid`
- Navegador: Chromium
- Protocolo: CDP
- Base URL: `http://localhost:5173`

⚠️ Si `execution_mode = static`  
→ **NO ejecutar este skill**.

---

## Precondiciones obligatorias

Deben existir previamente:

- `architecture/routes_inventory.md`
- `ui/crud_matrix.md`
- `run_log.md` con `execution_mode = hybrid`

Si **alguna** de estas precondiciones no se cumple  
→ **NO ejecutar el skill**  
→ **Stage E debe considerarse FAIL**.

---

## Alcance técnico del scan

Este skill **solo verifica síntomas técnicos observables**, tales como:

- ❌ Pantalla en blanco
- ❌ Error JS bloqueante en consola
- ❌ Navegación abortada
- ❌ Vista lazy-loaded que no carga
- ❌ Acción CRU(D) que rompe la UI
- ❌ Error HTTP técnico visible (401 inesperado, 500)

⚠️ Si la UI “funciona” pero el comportamiento no es el esperado  
→ **NO es responsabilidad de este skill**.

---

## Acciones del Skill

### 1️⃣ Inicialización de sesión

1. Abrir la aplicación en la URL base.
2. Verificar que:
   - la aplicación renderiza,
   - no hay crash inmediato,
   - no existe overlay de error inicial.
3. Registrar cualquier error técnico inicial observado.

---

### 2️⃣ Navegación de rutas

Para **cada ruta** listada en:
architecture/routes_inventory.md


Ejecutar:

1. Navegar explícitamente a la ruta.
2. Esperar render completo de la vista.
3. Verificar:
   - la vista renderiza completamente,
   - no hay error JS bloqueante,
   - no hay redirección infinita,
   - no aparece overlay de error.
4. Registrar resultado **PASS o FAIL** por ruta.

⚠️ No interactuar con flujos secundarios.

---

### 3️⃣ Verificación de vistas lazy-loaded

Para cada vista marcada como lazy-loaded:

1. Forzar resolución completa del módulo:
   - esperar hooks de montaje (`onMounted`),
   - ejecutar scroll o foco si aplica.
2. Verificar:
   - que el módulo carga correctamente,
   - que no existe error de import dinámico,
   - que no se produce crash de UI.
3. Registrar resultado por vista.

---

### 4️⃣ Ejecución mínima de CRU(D)

Para **cada CRUD** identificado en:
ui/crud_matrix.md


Ejecutar mínimamente:

- **List**
  - abrir la pantalla,
  - verificar que no crashea.

- **Create**
  - abrir formulario,
  - ejecutar acción mínima,
  - verificar que la UI no se rompe.

- **Update**
  - abrir formulario existente,
  - verificar render correcto.

- **Delete** (si existe)
  - ejecutar acción,
  - ❌ NO confirmar modales manualmente,
  - ❌ NO cancelar flujos.

🎯 El objetivo es **detectar roturas técnicas**,  
no validar resultados funcionales.

---

## Reglas estrictas (NO negociables)

- ❌ No cancelar modales manualmente
- ❌ No simular datos complejos
- ❌ No validar mensajes de negocio
- ❌ No modificar estado funcional deliberadamente
- ❌ No evitar acciones que rompen

Si algo rompe → **se registra exactamente como ocurre**.

---

## Outputs obligatorios

Este skill **DEBE generar** los siguientes artefactos
dentro del REQ activo.

---

### 📄 `architecture/view_load_report.md` **(OBLIGATORIO)**

Debe contener, por cada ruta evaluada:

- Ruta
- Lazy-loaded: SI | NO
- Resultado de carga: PASS | FAIL
- Errores JS bloqueantes: SI | NO
- Errores de import dinámico: SI | NO

Formato mínimo por ruta:

Ruta: /usuarios
Lazy-loaded: SI
Resultado carga: PASS
Errores JS: NO
Errores import: NO


📌 **La ausencia de este archivo implica FAIL automático del Stage E.**

---

### 📄 `ui/ui_runtime_errors.md` (si aplica)

Solo si existen errores runtime visibles.
Debe incluir:
- Ruta
- Acción ejecutada
- Error observado

---

### 📄 `qa/stabilization_evidence.md`  
(extensión del existente)

Debe incluir una sección:
  - Runtime UI Scan
  - Rutas navegadas
  - CRUD ejecutados
  - Errores técnicos observados


---

## Criterio de finalización del Skill

- El skill **siempre finaliza**
- No decide PASS / FAIL del workflow
- La decisión final pertenece al **Gate del Workflow 70**

---

## Regla de cierre del scan (OBLIGATORIA)

Una ruta o vista se considera:

- **PASS** si:
  - renderiza completamente,
  - no presenta errores JS bloqueantes,
  - no presenta errores de import dinámico.

- **FAIL** si:
  - no renderiza,
  - aparece overlay de error,
  - existe error JS bloqueante,
  - falla la carga de un módulo lazy.

Si existe **al menos una ruta o vista con estado FAIL**  
→ el **Stage E del Workflow 70 DEBE considerarse FALLIDO**.

---

## Regla final del Skill

> **Una vista que no renderiza completamente  
> implica que el sistema NO es estable.**  
>
> **Este skill observa.  
> No corrige.  
> No interpreta.  
> No decide.**
