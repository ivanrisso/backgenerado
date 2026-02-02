# Evidencia de Estabilización - REQ-CLIENTES

## 1. Resumen Ejecutivo
Se han mitigado los errores bloqueantes que impedían la edición de clientes (Error 500 en maestras) y se han corregido errores visuales (SVG) y de robustez en el frontend. El sistema se encuentra estable operativo en desarrollo.

## 2. Diagnóstico del Error 500 (Backend)
**Síntoma:** `GET /api/v1/condiciones-tributarias/` y `/api/v1/tipoimpuestos/` retornaban 500 Internal Server Error.
**Causa Raíz:** Inconsistencia entre la definición del Schema de Base de Datos (ENUMs en Mayúsculas), los Datos almacenados (minúsculas) y la definición de Enums en Python.
- SQLAlchemy intentaba mapear el valor de la base de datos (`impuesto_directo`) contra los miembros del Enum en Python.
- Debido a una discrepancia en cómo SQLAlchemy 2.0+ maneja `Mapped[Enum]` en MySQL, se producía un `LookupError` al no encontrar correspondencia exacta.

**Mitigación Implementada:**
1. **Estandarización de Enums (Python):** Se actualizaron todos los valores en `app/domain/entities/enums.py` a MAYÚSCULAS para coincidir con la convención de Base de Datos.
2. **Corrección de Datos (Hard Fix):** Se ejecutó un script de migración (`fix_db_enums_hard.py`) que:
    - Convirtió temporalmente las columnas Enum a VARCHAR.
    - Actualizó el contenido a `UPPER()`.
    - Restauró la definición de columnas a ENUM con los valores correctos en mayúsculas.
    
**Resultado:**
- El endpoint ahora responde **200 OK**.
- `curl http://localhost:8000/api/v1/condiciones-tributarias/` devuelve la lista correcta de condiciones (6 items).

## 3. Corrección Frontend (SVG)
**Síntoma:** Warning en consola `Error: <path> attribute d: Expected arc flag ('0' or '1')`.
**Causa:** Sintaxis ambigua en un path SVG del componente `ClienteForm.vue` (ícono de "Sin domicilios"). La secuencia `1111.314` era interpretada incorrectamente por algunos parseadores estrictos.
**Mitigación:** Se agregaron espacios explícitos a los flags del arco: `a8 8 0 1 1 11.314 0z`.

## 4. Robustez Frontend
Adicionalmente, se implementaron mejoras defensivas:
- `Promise.allSettled` en `onMounted` de `ClienteForm.vue` para evitar que un fallo en una maestra bloquee toda la pantalla.
- Bloques `try/catch` en composables `useTiposImpuesto` y `useCondicionesTributarias`.
- Manejo de estado `error` y `loading`.

## 5. Pruebas de Desarrollo (Seeds)
Se ejecutó `seed_dev_fiscal.py` para asegurar la existencia de tipos de impuestos críticos (IVA, IIBB) y condiciones tributarias básicas, garantizando que el formulario de cliente se renderice con opciones válidas.
