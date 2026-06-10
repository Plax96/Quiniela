# Codigo reutilizable para revision de calidad

Esta carpeta contiene scripts para evitar repetir analisis manual y ahorrar tokens.

## Scripts

- auditar_info_quiniela.py
  - Genera un reporte de estado general en Logs/mejora_info_buscador/auditoria_estado_info_YYYY-MM-DD.md
- generar_checklist_automatico.py
  - Genera checklist por equipo en formato md/csv
- ejecutar_revision_completa.sh
  - Ejecuta ambos scripts en secuencia

## Uso rapido

Desde la raiz del repo:

./Logs/mejora_info_buscador/codigo_reutilizable/ejecutar_revision_completa.sh

## Salidas

- Logs/mejora_info_buscador/auditoria_estado_info_YYYY-MM-DD.md
- Logs/mejora_info_buscador/checklist_automatico_por_equipo_YYYY-MM-DD.md
- Logs/mejora_info_buscador/checklist_automatico_por_equipo_YYYY-MM-DD.csv
