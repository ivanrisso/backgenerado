# Análisis de Riesgos

## Riesgos Funcionales y Fiscales
1. **Pérdida de Sincronía con AFIP**:
   - Riesgo de que el sistema local marque una factura como "Emitida" pero AFIP la haya rechazado, o viceversa (timeou durante la respuesta).
   - *Mitigación necesaria*: Mecanismos de re-consulta y reconciliación de estado (GetComprobante).

2. **Cambios Normativos**:
   - AFIP cambia frecuentemente URLs, certificados raíz, o protocolos de seguridad.
   - *Mitigación necesaria*: Configuración flexible, no hardcodeada. Pruebas de integración continuas contra entorno de Homologación.

3. **Vencimiento de Certificados Digitales**:
   - El sistema requiere certificados (`.crt`, `.key`) para firmar. Si vencen, la facturación se detiene TOTALMENTE.
   - *Mitigación necesaria*: Monitoreo de expiración y alertas preventivas.

## Riesgos Técnicos
1. **Escalabilidad de Base de Datos**:
   - Uso de MySQL simple. Si el volumen de comprobantes crece masivamente, consultas de reportaría podrían degradar el rendimiento transaccional.
   - *Mitigación*: Índices apropiados, particionamiento futuro, réplicas de lectura.

2. **Seguridad de Datos Sensibles**:
   - Manejo de datos fiscales y personales de clientes.
   - Riesgo de exposición de APIs sin autenticación robusta (se detectó JWT pero se debe auditar su implementación en todos los endpoints).

3. **Deploy y CI/CD**:
   - No se evidencian pipelines de despliegue automatizado (GitHub Actions, GitLab CI).
   - Riesgo de despliegues manuales propensos a error humano "funciona en mi máquina".
