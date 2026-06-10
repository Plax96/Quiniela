# Contexto del proyecto: Quiniela Mundial 2026

Este repositorio se enfoca en construir un sistema para predicciones del Mundial 2026 (quiniela).

## Objetivo inicial
- Definir estructura base para trabajo con Copilot.
- Preparar el entorno para Machine Learning y PLN.
- Evolucionar gradualmente skills y agentes.

## Guías
- Priorizar código claro y modular.
- Mantener trazabilidad de experimentos y datasets.
- Separar prototipos de código de producción.

## Protocolo asíncrono entre agentes

Todos los agentes deben operar en paralelo sin bloquearse entre sí.

1. Cada agente trabaja sobre su propio output y publica entregables incrementales.
2. Ningún agente debe esperar respuesta sincrónica de otro para continuar una tarea que pueda avanzar con datos disponibles.
3. Los handoffs se hacen por archivos en carpetas compartidas (no por conversación):
    - Buscador -> `Informacion/` y `Informacion/datasets/`
    - ML -> `Resultados/`
    - Analítico -> `Logs/mejoras/`
    - Arquitecto -> `.github/` y `.github/arquitecto/validacion/`
4. Si dos agentes pueden tocar un mismo artefacto, usar versionado (`vNN` o fecha) en lugar de sobrescribir.
5. Antes de consumir un output de otro agente, tomar la versión estable más reciente y registrarla en la bitácora del día.

## Política global de hitos (anti-caché)

Para evitar sesiones demasiado largas que degraden calidad o agoten contexto:

1. Todo agente debe operar por hitos cortos con entregable incremental.
2. Tiempo máximo por hito: 25-30 minutos según agente.
3. Al cerrar cada hito, publicar artefacto o estado (`estable`, `pendiente`, `bloqueado`).
4. Si un hito no puede cerrarse, registrar bloqueo y continuar con el siguiente hito útil.
5. Ningún agente debe permanecer trabajando sin checkpoint publicable.

## Skills disponibles

Las siguientes skills están registradas y pueden ser utilizadas por Copilot y los agentes del proyecto.

### prompt-optimizer
- **Ruta**: `.github/skills/prompt-optimizer/SKILL.md`
- **Descripción**: Pre-procesa y optimiza prompts antes de enviarlos a cualquier agente. Analiza claridad, contexto, formato y ambigüedad; aplica técnicas de prompt engineering; traduce estratégicamente al idioma con mayor cobertura del dominio y devuelve la respuesta en español.
- **Activación**: **Siempre activa.** Se ejecuta automáticamente como capa de pre-procesamiento en cada consulta del chat. Toda respuesta final se entrega en español.

### skill-creator
- **Ruta**: `.github/skills/skill-creator/SKILL.md`
- **Descripción**: Crea nuevas skills, modifica y mejora skills existentes, y mide su rendimiento. Incluye flujo de evaluación con benchmarks y análisis de varianza.
- **Activación**: Cuando el usuario quiera crear una skill desde cero, editar o mejorar una existente, ejecutar evaluaciones o optimizar la descripción de una skill para mejor activación.

### xlsx
- **Ruta**: `.github/skills/xlsx/SKILL.md`
- **Descripción**: Manejo integral de archivos de hojas de cálculo (.xlsx, .xlsm, .csv, .tsv). Lectura, edición, creación, limpieza de datos tabulares, fórmulas y gráficos. Esencial para trabajar con datasets deportivos, estadísticas FIFA y datos de partidos.
- **Activación**: Cuando se trabaje con archivos de datos tabulares (CSV, XLSX) de resultados, rankings, estadísticas de equipos o cualquier dataset del proyecto.

### doc-coauthoring
- **Ruta**: `.github/skills/doc-coauthoring/SKILL.md`
- **Descripción**: Flujo estructurado para co-autoría de documentación: specs técnicas, propuestas, documentos de decisión y reportes de experimentos. Guía al usuario por etapas de captura de contexto, refinamiento y verificación.
- **Activación**: Cuando se necesite escribir documentación del proyecto, specs de modelos, reportes de experimentos o documentos de decisión técnica.

### web-research
- **Ruta**: `.github/skills/web-research/SKILL.md`
- **Descripción**: Catálogo de fuentes deportivas confiables (ESPN, FBref, Transfermarkt, FIFA, WhoScored, SofaScore, Understat) con estrategias de extracción por tipo de dato, patrones de búsqueda optimizados y protocolo de validación cruzada. Wikipedia solo como último recurso.
- **Activación**: Cuando se necesite buscar información deportiva en internet, acceder a estadísticas de fútbol, consultar fuentes para el Agente Buscador o recopilar datos del Mundial.

### sports-data-deep
- **Ruta**: `.github/skills/sports-data-deep/SKILL.md`
- **Descripción**: Recopilación profunda y estructurada de datos deportivos en 4 capas: (1) estadísticas de jugadores en su club y selección, (2) estadísticas de equipos por campaña de eliminatorias, (3) marcadores y stats históricas de partidos, (4) textos para PLN. Incluye esquemas CSV completos, fuentes por tipo de dato, patrones de búsqueda profunda y checklist de completitud para ML/PLN.
- **Activación**: Cuando el Agente Buscador construya datasets de jugadores, equipos o partidos. Cuando se necesiten stats de eliminatorias, rendimiento en ligas de club, marcadores históricos, head-to-head completo o textos para procesamiento de lenguaje natural.

> A medida que se creen nuevas skills, se deben registrar en esta sección siguiendo el mismo formato.

## Agentes disponibles

Los agentes del proyecto se encuentran en `.github/agents/`. Operan de forma asíncrona y colaboran entre sí mediante carpetas compartidas.

### Buscador (Search Agent)
- **Ruta**: `.github/agents/buscador.md`
- **Rol**: Investigador deportivo con acceso a internet. Recopila, valida, cruza y estructura información sobre equipos, jugadores, estadísticas avanzadas (xG, PPDA), lesiones, cambios técnicos, factores contextuales y noticias del Mundial 2026. Genera fichas `.md` por equipo y fichas pre-partido, además de datasets CSV estructurados listos para ML.
- **Output**: `Informacion/` (fichas MD) + `Informacion/partidos/` (fichas pre-partido) + `Informacion/datasets/` (CSVs: equipos, jugadores, partidos_historicos, h2h, contexto_partidos).
- **Bitácora**: `Logs/prompts/Buscador_YYYY-MM-DD.md`

### ML (Machine Learning Agent)
- **Ruta**: `.github/agents/ml.md`
- **Rol**: Motor de predicción. Consume datasets CSV de `Informacion/datasets/` (fuente primaria) y fichas `.md` para PLN (fuente complementaria). Crea Jupyter Notebooks en `Notebooks/` para cada etapa del pipeline. Entrena modelos de ML (scikit-learn, XGBoost, LightGBM) y PLN (NLTK, spaCy), genera predicciones 1X2 con probabilidades.
- **Input**: `Informacion/datasets/` (CSVs) + `Informacion/` (fichas MD para PLN) + `Logs/mejoras/`
- **Output**: `Resultados/` — predicciones en `.csv` o `.xlsx`.
- **Notebooks**: `Notebooks/` — pipeline completo (ingesta, features, entrenamiento, evaluación, predicciones, explicabilidad, PLN).
- **Bitácora**: `Logs/prompts/ML_YYYY-MM-DD.md`

### Analítico (Analytics Agent)
- **Ruta**: `.github/agents/analitico.md`
- **Rol**: Evaluador y estratega. Analiza las predicciones del Agente ML, identifica debilidades, genera puntos de mejora y produce la quiniela final. Sabe cuándo detener el ciclo de optimización. Genera visualizaciones y reportes comprensibles para el usuario.
- **Input**: `Resultados/` (predicciones versionadas `predicciones_vNN_*.csv` + métricas `metricas_vNN_*.csv`).
- **Output**: `Logs/mejoras/` (puntos de mejora) + `Resultados/` (quiniela final y visualizaciones).
- **Notebooks**: `Notebooks/analitico/` — evaluación, diagnóstico, generación de quiniela final.
- **Bitácora**: `Logs/prompts/Analitico_YYYY-MM-DD.md`

### Arquitecto (AI Systems Engineer Agent)
- **Ruta**: `.github/agents/arquitecto.md`
- **Rol**: Ingeniero de sistemas de IA. Crea, mejora y da mantenimiento a skills, agentes y prompts. Valida continuamente las últimas capacidades de GitHub Copilot para maximizar la potencia de todo el ecosistema. **En su primera ejecución (o si el changelog tiene más de 7 días) ejecuta el Protocolo de Validación** antes de cualquier tarea.
- **Input**: `.github/skills/*/SKILL.md` + `.github/agents/*.md` + `.github/copilot-instructions.md` + Web (changelog oficial de Copilot).
- **Output**: Skills/agentes mejorados + `.github/arquitecto/validacion/` (audit_log, copilot_changelog) + `Logs/prompts/Arquitecto_YYYY-MM-DD.md`.
- **Carpeta de validación**: `.github/arquitecto/validacion/` — mantiene el conocimiento actualizado de Copilot y el historial de auditorías.
- **Bitácora**: `Logs/prompts/Arquitecto_YYYY-MM-DD.md`

### Flujo de colaboración entre agentes

```
Buscador ──▶ Informacion/           ──▶ ML ──▶ Resultados/ ──▶ Analítico
              ├── *.md (fichas)              ▲              ▼
              ├── partidos/*.md         Notebooks/    Logs/mejoras/
              └── datasets/*.csv              ◀──────────┘

Arquitecto ──▶ .github/skills/      (mantiene y mejora skills)
           ──▶ .github/agents/      (mantiene y mejora agentes)
           ──▶ .github/arquitecto/validacion/  (conocimiento Copilot actualizado)
```

> A medida que se creen nuevos agentes, se deben registrar en esta sección siguiendo el mismo formato.
