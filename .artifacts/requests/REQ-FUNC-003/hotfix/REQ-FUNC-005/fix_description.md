# Fix Description — HF-FUNC-005

## Origen

Gap funcional detectado manualmente durante revisión visual de la navegación,
posterior a una corrección funcional previa.

Este gap **NO fue detectado por Workflow 70**.

---

## Síntoma observable

En el sidebar de la aplicación:

- Los ítems **Usuarios**, **Roles** y **Menús** aparecen como
  **ítems de primer nivel**.
- Sin embargo, en la configuración de menús:
  - Estos ítems dependen del menú contenedor **Seguridad**.
  - **Seguridad** actúa como agrupador lógico sin ruta propia.

Existe una **inconsistencia entre la jerarquía configurada y la jerarquía visible**.

---

## Evidencia

- Vista de sidebar con ítems sueltos:
  - Usuarios
  - Roles
  - Menús
- Vista de configuración de menú:
  - Seguridad (sin ruta)
    - Usuarios
    - Roles
    - Menús

---

## Impacto funcional

- La navegación no refleja la estructura funcional definida.
- El usuario percibe el sistema como desordenado.
- Se pierde la agrupación semántica de seguridad.
- Aumenta la confusión en usuarios administrativos.

---

## Alcance

- Afecta únicamente la **presentación del menú lateral**.
- No implica cambios de permisos.
- No implica cambios técnicos ni de backend.

---

## Restricciones

- ❌ No agregar nuevas funcionalidades
- ❌ No modificar reglas de negocio
- ❌ No refactor técnico
- ✔️ Solo corregir jerarquía de navegación
