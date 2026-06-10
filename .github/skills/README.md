# Skills

Esta carpeta contiene skills reutilizables para Copilot en el proyecto Quiniela Mundial 2026.

## Skills activas

- prompt-optimizer: optimización de prompts y respuesta final en español.
- doc-coauthoring: coautoría estructurada de documentación técnica.
- web-research: catálogo de fuentes deportivas y validación cruzada.
- sports-data-deep: recopilación profunda por capas para ML/PLN.
- skill-creator: creación y mejora iterativa de skills.
- xlsx: operaciones sobre archivos tabulares y hojas de cálculo.

## Convenciones

1. Cada skill debe tener frontmatter YAML con name y description de activación "pushy".
2. El cuerpo debe seguir flujo claro: contexto -> instrucciones -> ejemplos -> criterios.
3. Mantener compatibilidad con el estándar agentskills.io.
4. Registrar cambios relevantes en auditorías del Agente Arquitecto.
