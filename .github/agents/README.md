# Agents

Esta carpeta contiene los agentes especializados del ecosistema Quiniela Mundial 2026.

## Agentes actuales

- `buscador.md`: investigación deportiva y construcción de datasets/fichas.
- `ml.md`: entrenamiento, evaluación y predicción.
- `analitico.md`: diagnóstico, mejora y quiniela final.
- `arquitecto.md`: mantenimiento de skills/agentes/prompts y validación de capacidades Copilot.

## Convenciones

1. Cada agente debe tener frontmatter YAML (`name`, `description`).
2. La `description` debe indicar claramente cuándo invocar el agente.
3. Todo agente define: principios de operación, herramientas, entradas, salidas y criterios de validación.
4. Cada ejecución relevante deja trazabilidad en `Logs/prompts/[Agente]_YYYY-MM-DD.md`.
5. Si se crea un nuevo agente, también debe registrarse en `.github/copilot-instructions.md`.

## Política asíncrona

1. Los agentes deben poder trabajar en paralelo sin bloquearse.
2. El intercambio de trabajo se hace por artefactos en carpetas compartidas, no por espera sincrónica.
3. Las salidas críticas deben versionarse (`vNN` o fecha) para evitar colisiones.
4. Cada agente debe registrar qué versión consumió y qué versión publicó.
5. Cuando haya dudas de consistencia, prevalece la versión estable más reciente registrada en bitácora.

## Prácticas Copilot 2026

1. Usa `/chronicle` para consultar historial de sesiones antes de rehacer análisis o mantenimiento.
2. En tareas complejas, ajusta reasoning level desde el model picker para equilibrar calidad/costo.
3. Para auditorías largas y comparación de múltiples artefactos, prioriza modelos con ventana de contexto amplia.
