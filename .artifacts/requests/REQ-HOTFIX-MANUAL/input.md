# REQ-HOTFIX-MANUAL-20260204-1500

## Contexto
Durante la ejecución del pipeline de CI se detectó un error técnico
en la creación de recibos que bloquea la correcta validación del backend.

## Objetivo
Preparar un hotfix técnico para restaurar la integridad del servicio
de Recibos sin introducir cambios funcionales.

## Alcance
- Servicio de Recibos
- Inicialización de dependencias
- Pruebas unitarias asociadas

## Fuera de alcance
- Cambios funcionales de negocio
- Cambios en UX
- Nuevas validaciones

## Tipo
Hotfix técnico

## Evidencia
Error en CI:
`ReciboService.__init__() missing cliente_repo`
