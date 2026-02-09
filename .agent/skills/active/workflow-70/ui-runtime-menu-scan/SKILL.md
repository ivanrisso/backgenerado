# SKILL — UI Runtime Menu Scan

## Rol autorizado
- **QA**

⚠️ Ningún otro rol está autorizado a ejecutar este skill.

---

## Objetivo

Ejecutar una **verificación runtime específica del sistema de navegación (menú)**,
con el fin de **observar y evidenciar** errores **técnicos y funcionales observables**
relacionados con la navegación de la UI.

Este skill permite detectar:

- ítems de menú no visibles para el rol ADMIN,
- submenús que no expanden,
- submenús visibles pero con navegación fallida,
- ítems de menú que apuntan a rutas inexistentes,
- abortos de navegación iniciados desde el menú.

Este skill:
- ❌ NO valida reglas de negocio
- ❌ NO corrige código
- ❌ NO clasifica hotfix vs gap
- ❌ NO toma decisiones de priorización

👉 Su **única responsabilidad** es **OBSERVAR y EVIDENCIAR**.

---

## Contexto de ejecución

- Workflow: **70 — Stabilization Scan**
- Stage: **E — Runtime Scan**
- Modo requerido: `execution_mode = hybrid`
- Navegador: Chromium
- Protocolo: CDP
- Base URL: `http://localhost:5173`

### Usuario obligatorio
- Usuario: `admin@facturacion.local`
- Password: `admin.password.dev`

⚠️ Este skill **SIEMPRE se ejecuta con rol ADMIN**,  
independientemente del rol donde se haya detectado el issue.

---

## Precondiciones obligatorias

Deben existir previamente:

- `architecture/routes_inventory.md`
- `run_log.md` con `execution_mode = hybrid`
- Credenciales ADMIN válidas

Si **alguna** de estas precondiciones no se cumple  
→ **NO ejecutar el skill**.

---

## Alcance del scan

Este skill verifica **exclusivamente**:

- ❌ Ítems de menú no visibles para ADMIN
- ❌ Submenús que no expanden
- ❌ Submenús visibles pero con navegación fallida
- ❌ Clicks de menú que:
  - no navegan,
  - navegan a rutas inexistentes,
  - producen error JS,
  - cancelan la navegación

Este skill **NO evalúa**:

- permisos por roles no-admin
- textos, labels o UX fina
- reglas de negocio
- comportamiento funcional esperado

---

## Acciones del Skill

### 1️⃣ Inicialización de sesión ADMIN

1. Abrir la aplicación en la URL base.
2. Autenticarse como:
   - `admin@facturacion.local`
   - `admin.password.dev`
3. Verificar:
   - Login exitoso
   - Render correcto del layout
   - Menú lateral visible

Registrar cualquier error inmediato observado.

---

### 2️⃣ Inventario visual del menú

1. Enumerar todos los ítems de primer nivel del menú.
2. Para cada ítem, registrar si es:
   - simple
   - contenedor (posee submenús)
3. Registrar evidencia textual del árbol de menú observado.

---

### 3️⃣ Expansión de submenús (OBLIGATORIO)

Para cada ítem contenedor:

1. Intentar expandir el submenú.
2. Verificar:
   - que el submenú se despliega visualmente,
   - que no se produzcan errores JS,
   - que no exista navegación abortada.

Si un submenú **NO se expande correctamente**  
→ registrar **FAIL técnico observable**.

---

### 4️⃣ Navegación desde menú  
(iterativa, completa y anti-stale)

**Regla CRÍTICA:**  
Nunca reutilizar referencias del DOM.  
En cada navegación se debe **re-descubrir** el menú y sus subítems.

Para cada menú padre:

1. Expandir el menú padre.
2. Descubrir la lista completa de subítems visibles.
3. Para cada subítem:
   1. Expandir nuevamente el menú padre (aunque esté abierto).
   2. Clickear el subítem.
   3. Validar:
      - navegación efectiva,
      - carga de vista,
      - ausencia de errores JS.
   4. Volver a una ruta base **solo si el menú colapsó**.
4. El menú padre se considera **COMPLETO** únicamente cuando
   **todos** sus subítems tengan resultado registrado.

---

### Regla de completitud por menú padre (CRÍTICA)

Un menú padre **NO puede considerarse validado** hasta que:

- TODOS sus subítems visibles
- hayan sido navegados individualmente
- y cada uno tenga resultado **PASS o FAIL** registrado

Mientras exista al menos un subítem sin registro:

- ❌ NO cambiar de menú padre
- ❌ NO concluir el menú
- ❌ NO avanzar al siguiente módulo

---

### 5️⃣ Correlación menú ↔ rutas

1. Comparar:
   - rutas visibles en el menú
   - rutas existentes en `architecture/routes_inventory.md`
2. Detectar:
   - rutas existentes que **NO aparecen** en el menú
   - ítems de menú que apuntan a rutas inexistentes

Registrar diferencias **sin interpretarlas**.

---

## Reglas estrictas (NO negociables)

- ❌ No modificar estado del sistema
- ❌ No crear, editar ni borrar entidades
- ❌ No forzar navegación manual por URL
- ❌ No ocultar errores
- ❌ No interpretar intención funcional

Si algo falla → **se registra exactamente como ocurre**.

---

## Outputs obligatorios

Este skill **DEBE generar** los siguientes artefactos
dentro del REQ activo.

---

### 📄 `qa/stabilization_evidence.md`  
(extensión del existente)

Debe incluir una sección:

  - Runtime Menu Scan (ADMIN)
  - Menús visibles
  - Submenús detectados
  - Submenús que no expanden
  - Ítems que no navegan
  - Rutas existentes no visibles en menú


---

### 📄 `ui/menu_runtime_report.md`  **(OBLIGATORIO)**

Debe contener, por cada menú padre:

- Nombre del menú
- Tipo (simple / contenedor)
- Cantidad de subítems detectados
- Cantidad de subítems navegados
- Resultado final del menú: PASS | FAIL
- Detalle de errores observados (si aplica)

📌 **La ausencia de este archivo implica que el runtime menu scan  
NO fue ejecutado correctamente y DEBE provocar FAIL del Stage E.**

---

### 📄 `ui/ui_runtime_errors.md` (si aplica)

Solo si existen errores visibles.
Debe incluir:
- Menú
- Acción ejecutada
- Error observado

---

## Clasificación (NO incluida)

Este skill:
- ❌ NO decide Hotfix vs Gap
- ❌ NO genera carpetas
- ❌ NO prioriza issues

La clasificación ocurre **exclusivamente** en:

> **Stage F — Clasificación Hotfix vs Gap (Workflow 70)**

---

## Criterio de finalización del Skill

- El skill **siempre finaliza**
- No bloquea por sí mismo
- El **Gate del Workflow 70** decide PASS / FAIL

---

## Regla de cierre del reporte (OBLIGATORIA)

Un menú padre se considera:

- **PASS** si:
  - Todos los subítems detectados fueron navegados
  - Ninguno produjo error de navegación o error JS

- **FAIL** si:
  - Existe al menos un subítem no navegado
  - Existe al menos un subítem con error
  - El submenú no expandió correctamente

Si existe **al menos un menú con estado FAIL**  
→ el **Stage E del Workflow 70 DEBE considerarse FALLIDO**.

---

## Regla final del Skill

> **Si un menú no se puede expandir o navegar,  
> el sistema NO es estable, aunque las rutas existan.**  
>
> **Este skill observa.  
> No corrige.  
> No interpreta.  
> No decide.**
