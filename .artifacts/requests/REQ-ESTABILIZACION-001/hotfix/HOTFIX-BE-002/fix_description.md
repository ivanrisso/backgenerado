# HOTFIX-BE-002: Integridad de Datos en Recibo Service

## Descripción
El servicio `ReciboService` genera recibos utilizando datos "hardcodeados" (placeholders) para los atributos del Cliente (ej: `doc_nro="00000000"`, `nombre_cliente="Cliente"`). Esto ocurre porque el servicio no recupera la entidad `Cliente` antes de crear el `Comprobante`.
El código indica explícitamente: `# Como ReciboCreate no tiene todo, esto fallaría en BD si son Not Null.`

## Impacto
- **Severidad**: Media (Integridad de Datos).
- **Componente**: Backend (`recibo_service.py`).
- **Riesgo**: Alto (Corrupción de datos en producción / Problemas de Compliance). Los recibos son documentos fiscales/legales y deben tener datos correctos.

## Contexto Técnico
- Ubicación: `app/services/recibo_service.py`
- Problema: Falta de inyección y uso de `ClienteRepository`.
