# Análisis — HF-CLEAN-RECIBO-001

## Causa raíz
Desalineación entre la firma del constructor y las instancias
utilizadas en tests y configuración.

## Riesgos
- Bajo
- Cambio localizado

## Alternativas consideradas
1. Agregar valor por defecto → DESCARTADO
2. Ajustar inyección explícita → ELEGIDO
