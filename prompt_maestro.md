Actuá como Orchestrator (Planning). Objetivo: instalar el Agent Operating System (AOS) en este repo.

1) Crear/actualizar SOLO estos paths:
- `.agent/**`
- `.templates/**`
- `RUNBOOK.md`

2) NO tocar código del backend/frontend ni configuración existente fuera de esos paths.

3) Verificar que existen artifacts del baseline:
- `.artifacts/requests/REQ-BASELINE/current_state.md`
- `.artifacts/requests/REQ-BASELINE/architecture/domain_map.md`
- `.artifacts/requests/REQ-BASELINE/architecture/tech_debt.md`
- `.artifacts/requests/REQ-BASELINE/architecture/risks.md`
Si falta alguno, crear:
- `.artifacts/requests/REQ-BASELINE/blocking_issues.md` listando faltantes.

4) Al finalizar, listar archivos creados y sugerir un commit/PR.

Restricciones:
- No comandos destructivos.
- Si necesitás terminal (ls/tree/find/grep/cat), pedí aprobación antes.
- No inventar contenido fuera de lo que está en este chat y el baseline.
