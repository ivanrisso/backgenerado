# QA Evidence - REQ-CI-BOOTSTRAP-001

## Simulación Local del Pipeline

Se han ejecutado manualmente los pasos definidos en `.github/workflows/ci.yml` para validar su funcionamiento.

### Job 1: Backend (Python 3.11)
**Paso: Install Dependencies**
`poetry install --no-interaction --no-root`
> Resultado: ✅ OK (No dependencies to install or update)

**Paso: Run Tests**
`poetry run pytest -v`
> Resultado: ✅ PASS
```text
tests/test_comprobante_draft.py::test_create_comprobante_draft_mocked PASSED [ 50%]
tests/test_healthcheck.py::test_healthcheck PASSED                               [100%]
======================== 2 passed, 45 warnings in 0.08s ========================
```

### Job 2: Frontend (Node 20)
**Paso: Install Dependencies**
`npm ci`
> Resultado: ✅ OK (added 554 packages in 6s)

**Paso: Run Tests**
`npm run test` (Simulado con `./node_modules/.bin/vitest run` por path local)
> Resultado: ✅ PASS
```text
 Test Files  1 passed (1)
      Tests  1 passed (1)
```

## Checklist de Calidad CI
- [x] **Backend Job**: Usa `setup-python`, `install-poetry` y `pytest`.
- [x] **Frontend Job**: Usa `setup-node`, `npm ci` (limpio) y `vitest`.
- [x] **Triggers**: Configurado para `push` y `pull_request` en branches principales.
- [x] **Aislamiento**: Jobs independientes corriendo en `ubuntu-latest`.

## Hotfix: CI Settings Validation (2026-01-29)
**Problema**: CI fallaba por falta de variables de entorno requeridas por `Settings` (Pydantic).
**Solución**: 
- Configurar `ENV: test` en el workflow.
- Generar `certs/` y `.env.test` dummy durante el build.
- Corregir formato de `BACKEND_CORS_ORIGINS` a JSON válido `[]` en `.env.test` (solucionando error de parsing por comillas simples).
- `app/core/config.py` ya soportaba carga condicional.

**Validación Local**:
Script `verify_ci_fix.py` con `ENV=test` cargó exitosamente la configuración simulando el entorno de CI.

## Hotfix: CI Logger (2026-01-29)
**Problema**: `ValueError: Unable to configure handler 'file'` en CI por falta de permisos/directorios de log.
**Solución**: 
- Se condicionó `app.core.logger.init_logger()` para no configurar `FileHandler` si `ENV=test`.
- Se usa `copy.deepcopy` para no alterar la configuración global en memoria.
**Validación**: Script `verify_logger.py` confirmó inicialización limpia con solo `StreamHandler`.
