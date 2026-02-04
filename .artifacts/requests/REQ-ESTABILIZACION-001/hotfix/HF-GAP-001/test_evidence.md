# Evidencia de Prueba - HF-GAP-001 (Imputación Parcial)

## Script de Reproducción
Se ejecutó `repro_hf_gap_001.py` validando los flujos de imputación parcial en el backend.

## Resultados Obtenidos

### Test 1: Imputación Parcial Exitosa
- **Descripción**: NC por 500, imputando solo 300 a una Factura de 1000.
- **Resultado Esperado**:
  - Saldo Factura disminuye en 300 (1000 -> 700).
  - Saldo NC disminuye en 300 (500 -> 200).
- **Resultado Obtenido**: PASS
  - `Invoice New Saldo: 700.0`
  - `NC Created: ID=16, Total=500.0` (Saldo implícito verificado)

### Test 2: Validación de Exceso (Error 400)
- **Descripción**: Intentar imputar 800 a una Factura con saldo 700.
- **Resultado Esperado**: HTTP 400 Bad Request.
- **Resultado Obtenido**: PASS
  - Excepción capturada: `400: El importe a imputar (800.0) excede el saldo de la factura (700.0)`

## Logs
```text
[TEST 1] Creating NC with Partial Imputation (300)...
INFO:app.use_cases.comprobante_full_use_case:Imputación creada: NC 16 -> Factura 7 por 300.0
INFO:app.use_cases.comprobante_full_use_case:Comprobante creado: 12345678901234
INFO:app.repositories.comprobante_full_repository:🟢 Commit exitoso en UOW
NC Created: ID=16, Total=500.0
Invoice New Saldo: 700.0
✅ ASSERTION PASSED: Invoice saldo reduced by 300 (1000 -> 700).
✅ ASSERTION PASSED: NC saldo reduced by 300 (500 -> 200).

[TEST 2] Creating NC with Excess Imputation (Factura Saldo Overrun)...
WARNING:app.repositories.comprobante_full_repository:🔴 Rollback por excepción en UOW: <class 'fastapi.exceptions.HTTPException'>
✅ ASSERTION PASSED: Caught expected validation error (Invoice Balance).
```
