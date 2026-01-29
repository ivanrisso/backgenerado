# Análisis de Deuda Técnica

## Deuda Crítica
1. **Ausencia de Tests Automatizados**:
   - **Severidad**: ALTA
   - **Evidencia**: Carpeta `tests` vacía de código.
   - **Impacto**: Imposibilidad de refactorizar o agregar features con seguridad. Riesgo altísimo de regresiones, especialmente en cálculos fiscales y lógica de AFIP.

2. **Gestión de Secretos y Tokens**:
   - **Severidad**: ALTA
   - **Evidencia**: Archivos `afip_token_cache.json` en raíz del proyecto.
   - **Impacto**: Riesgo de seguridad si se comitean. Fragilidad si el sistema de archivos es efímero (ej. despliegue en contenedores sin volumen persistente).

3. **Scripts de Mantenimiento "Sueltos"**:
   - **Severidad**: MEDIA
   - **Evidencia**: Múltiples scripts `.py` en la raíz (`seed_*.py`, `fix_schema.py`, `reset_db.py`).
   - **Impacto**: Lógica de inicialización y migración dispersa fuera de herramientas estándar (Alembic) o pipelines CI/CD. Dificulta la replicabilidad de entornos.

## Deuda Arquitectónica
- **Falta de Documentación de API Viva**: Aunque existe `openapi.yaml`, debería generarse automáticamente desde el código (FastAPI lo hace, hay que verificar si está sincronizado o es un artefacto manual desactualizado).
- **Manejo de Errores SOAP**: La integración con Zeep suele requerir un manejo robusto de excepciones (time outs, XML malformados). No es evidente un wrapper resiliente (circuit breaker, retries) en la inspección superficial.

## Deuda Frontend
- **Estado Inicial**: Parece un proyecto nuevo ("version": "0.0.0").
- **Componentización**: Se debe validar si se están usando componentes reutilizables o HTML/Tailwind duro en las vistas.
