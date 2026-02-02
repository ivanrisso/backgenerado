## Skill: fix-description-generator

### Propósito
Transformar un issue técnico detectado en una **descripción de corrección clara, no ejecutable**, usable como input de un workflow correctivo posterior.

### Input esperado
- hotfix/HF-XXX/input.md
- hotfix/HF-XXX/analysis.md
- Contexto del workflow (frontend / backend / auth)

### Output
- hotfix/HF-XXX/fix_description.md

### Restricciones
- ❌ No generar código
- ❌ No generar prompts ejecutables
- ❌ No ejecutar workflows
- ✔️ Solo describir QUÉ corregir y POR QUÉ

### Formato obligatorio
Debe usar el template:
.agent/templates/fix_description.template.md
