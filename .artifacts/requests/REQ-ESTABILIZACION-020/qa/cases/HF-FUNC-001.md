# Casos de Prueba: HF-FUNC-001 (Puntos de Venta)

## Precondiciones
- Usuario logueado como Admin.

## Casos

### TC-01: Visibilidad en Menú
**Pasos:**
1. Login.
2. Expandir "Maestros".
3. Verificar existencia de "Puntos de Venta".
**Resultado Esperado:** Ítem visible con icono de impresora.

### TC-02: Navegación
**Pasos:**
1. Clic en "Puntos de Venta".
**Resultado Esperado:** Carga vista `/puntos-venta` con título "Puntos de Venta" y tabla vacía (o con datos).

### TC-03: Alta de Punto de Venta (UI Check)
**Pasos:**
1. Clic en "+ Nuevo".
2. Verificar apertura de Modal.
3. Verificar campos: Número, Tipo, Estado.
**Resultado Esperado:** Modal abre correctamente. (No se probará la persistencia backend en profundidad si no es crítico, focalizamos en acceso).
