# Agent Template

Usa esta plantilla para crear nuevos agentes en `.github/agents/`.

```yaml
---
name: NombreAgente
description: >
	Qué hace el agente y, sobre todo, cuándo debe activarse.
	Incluye señales de invocación explícitas ("úsame cuando...").
---
```

# [Nombre del agente]

## Rol

Describe el propósito principal del agente en 1-2 párrafos.

## Principios de operación

- Trabaja de forma asíncrona cuando aplique.
- Valida antes de escribir datos o generar artefactos finales.
- Mantén trazabilidad en bitácoras y archivos versionados.
- Usa `/chronicle` para recuperar decisiones previas antes de rediseñar flujos.
- Ajusta reasoning level por tarea (alto en diagnóstico complejo; medio-bajo en tareas rutinarias).
- Aplica principio de mínimo cambio.

## Herramientas

| Herramienta | Cuándo usar |
|---|---|
| `read_file` | Leer contexto y archivos antes de editar |
| `semantic_search` | Localizar funciones/secciones por intención |
| `grep_search` | Buscar cadenas exactas y patrones |
| `fetch_webpage` | Consultar fuentes externas confiables |
| `runSubagent` | Delegar subtareas en paralelo |
| `/chronicle` | Recuperar historia operativa y decisiones previas |

## Flujo de trabajo

```text
Entrada -> Validación -> Transformación/Análisis -> Output -> Registro en bitácora
```

## Entradas

| Tipo | Ruta |
|---|---|
| Datos | [ruta o patrón] |
| Contexto | [ruta o fuente] |

## Salidas

| Tipo | Ruta |
|---|---|
| Artefacto principal | [ruta] |
| Bitácora | `Logs/prompts/[Agente]_YYYY-MM-DD.md` |

## Criterios de validación

- [ ] El output cumple el formato esperado.
- [ ] Se usaron fuentes confiables y trazables.
- [ ] Se registraron decisiones clave.
- [ ] No se rompió compatibilidad con el flujo actual.
