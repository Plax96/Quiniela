# GitHub Copilot — Changelog y Conocimiento Actualizado

> **Última actualización**: 2026-06-06
> **Fuentes consultadas**: github.blog/changelog/label/copilot/ · docs.github.com/copilot/features · VS Code 1.123 (2026-06-03)
> **Próxima actualización**: 2026-06-13 (7 días)

---

## Última versión conocida

- **Fecha de changelog más reciente validada**: 2026-06-05
- **Modelos y capacidad de razonamiento**:
  - `GPT-5.5` y `Claude Opus 4.7` con soporte de ventanas de contexto ampliadas en VS Code.
  - **Ventana de contexto 1M tokens** disponible para modelos compatibles (OpenAI/Anthropic) en VS Code 1.123.
  - **Reasoning level configurable** en Copilot para modelos compatibles (latencia vs profundidad).
- **Nuevos modelos/plataforma**:
  - `MAI-Code-1-Flash` disponible en Copilot (2026-06-02).
  - Modelos Gemini añadidos para Copilot CLI, cloud agent y Copilot app (2026-06-02).

---

## Novedades clave (mayo-junio 2026)

### Alto impacto para este repositorio

| Feature | Fecha | Descripción | Aplicación recomendada |
|---|---|---|---|
| **`/chronicle`** | 2026-06-02 | Insights y búsqueda de sesiones de agentes | Usarlo en auditorías para recuperar decisiones históricas antes de tocar skills/agentes |
| **Contexto 1M tokens** | 2026-06-03/04 | Ventana ampliada para modelos compatibles | Consolidar análisis largos (Buscador/ML) en menos sesiones fragmentadas |
| **Reasoning levels configurables** | 2026-06-04 | Ajuste de profundidad de razonamiento por tarea | Subir reasoning en ML/Analítico; bajar en tareas rutinarias para costo/latencia |
| **Copilot SDK GA** | 2026-06-02 | SDK estable para integrar capacidades agentic | Evaluar integración del pipeline Quiniela para tareas repetitivas de validación |
| **Agent Tasks REST API** | 2026-06-04 | API para crear/gestionar tareas de agentes | Preparar automatización futura de corridas por grupo (A-H) |
| **Copilot Memory (preferencias)** | 2026-06-02 | Memoria con preferencias en planes business/enterprise | Estandarizar estilo de outputs de agentes en el equipo |

### Impacto medio

| Feature | Fecha | Descripción | Nota |
|---|---|---|---|
| **Copilot app (agent-native desktop)** | 2026-06-02 | Nueva superficie de trabajo agentic | No bloqueante para este repo, pero útil para operación multi-superficie |
| **Schedule and automate tasks (cloud agent)** | 2026-06-02 | Programación de tareas agentic | Podría calendarizar refresh de datasets y auditorías |
| **Richer PR context in Copilot Chat** | 2026-06-04 | Mejor contexto en pull requests | Mejor revisión de cambios de skills/agentes |
| **Fix with Copilot for failing Actions** | 2026-06-04 | Disponible en Pro/Pro+/Max | Útil para CI/CD de notebooks y validación de esquemas |
| **Research agent (VS Code preview)** | 2026-06-03 | Investigación profunda con reporte citado | Ideal para exploración de fuentes en Buscador sin edición de código |

---

## Deprecaciones y migraciones

| Deprecado | Fecha | Acción recomendada |
|---|---|---|
| **GPT-4.1** | 2026-06-02 | Migrar prompts/model selection a GPT-5.4/5.5 o Claude Opus 4.7 |
| **GPT-5.2 / GPT-5.2-Codex** | 2026-06-05 | No fijar dependencias a esta familia; usar líneas activas |
| **GPT-5.1 y variantes** | 2026-04-03 | Mantener reemplazo por GPT-5.4+ |

---

## Cambios recomendados para skills/agentes del repo

1. **Añadir uso operativo de `/chronicle`** en Arquitecto para auditoría de decisiones pasadas.
2. **Actualizar tablas de modelos y deprecaciones** en Arquitecto (eliminar referencias a líneas retiradas).
3. **Incorporar estrategia de contexto 1M** en ML/Analítico para análisis largos.
4. **Agregar guía de Research Agent (preview)** en Buscador para investigación profunda sin editar artefactos.
5. **Mantener enfoque agentskills.io + gh skill**, ahora complementado con automatización futura por Agent Tasks API.

---

_Mantenido exclusivamente por el Agente Arquitecto. Actualizar cada 7 días consultando las fuentes del Protocolo de Validación._
