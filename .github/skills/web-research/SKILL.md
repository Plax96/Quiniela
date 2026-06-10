---
name: web-research
description: >
  Catálogo de fuentes deportivas confiables y estrategias de extracción de datos para investigación
  del Mundial 2026. Incluye URLs directas a recursos clave, patrones de búsqueda optimizados por tipo
  de dato, validación cruzada y priorización de fuentes. Usa esta skill siempre que necesites buscar
  información deportiva en internet, acceder a estadísticas de fútbol, consultar noticias de equipos
  o jugadores, o cuando el Agente Buscador necesite guía sobre dónde y cómo obtener datos confiables.
  Activa también cuando se mencionen fuentes deportivas, web scraping de stats, o recopilación de
  datos del Mundial.
---

# Web Research — Fuentes y Estrategias de Investigación Deportiva

Guía de referencia para investigación deportiva orientada al Mundial 2026. Contiene el catálogo de fuentes confiables, estrategias de extracción por tipo de dato y protocolos de validación.

## Operación con Copilot 2026

1. Antes de iniciar un nuevo lote, revisar historial con `/chronicle search` para evitar duplicar investigaciones.
2. Para investigaciones amplias (múltiples confederaciones y ventanas temporales), priorizar sesiones con contexto amplio en modelos compatibles.
3. Si está disponible, usar Research Agent (preview) para producir reportes citados de alto volumen antes de estructurar datasets finales.

## Catálogo de fuentes

### Tier 1 — Fuentes primarias (máxima confiabilidad)

| Fuente | URL base | Qué obtener | Formato |
|---|---|---|---|
| **FIFA.com** | `https://www.fifa.com/` | Rankings oficiales, calendario, grupos, sedes, reglamento | HTML, PDF |
| **FBref** | `https://fbref.com/` | Estadísticas avanzadas: xG, xGA, posesión, pases progresivos, set pieces, PPDA | Tablas HTML |
| **Transfermarkt** | `https://www.transfermarkt.com/` | Valor de mercado, plantillas, fichajes, lesiones, historial de transferencias | HTML |
| **FIFA World Ranking** | `https://www.fifa.com/fifa-world-ranking` | Ranking actualizado con puntos y movimientos | HTML |

### Tier 2 — Fuentes especializadas (alta confiabilidad)

| Fuente | URL base | Qué obtener |
|---|---|---|
| **WhoScored** | `https://www.whoscored.com/` | Ratings de jugadores, formaciones, estadísticas de partido, heat maps |
| **SofaScore** | `https://www.sofascore.com/` | Stats en vivo, ratings, head-to-head, tendencias |
| **Understat** | `https://understat.com/` | xG detallado por partido y jugador, shot maps |
| **fotMob** | `https://www.fotmob.com/` | Estadísticas por partido, alineaciones, momentum |
| **Soccerway** | `https://int.soccerway.com/` | Resultados históricos, head-to-head, calendarios |

### Tier 3 — Fuentes de noticias y análisis (preferidas para contexto y noticias)

> ⚠️ **Importante**: estas fuentes son más confiables que Wikipedia para noticias y análisis deportivo. Úsalas siempre antes de recurrir a fuentes no especializadas.

| Fuente | URL base | URLs específicas Mundial 2026 | Qué obtener |
|---|---|---|---|
| **ESPN FC** | `https://www.espn.com/soccer/` | `/league/_/name/FIFA.WORLD` · `/team/_/id/[ID]/[equipo]` · `/story/_/id/[ID]` | Noticias, análisis tácticos, convocatorias, predicciones de expertos — **fuente prioritaria** |
| **BBC Sport Football** | `https://www.bbc.com/sport/football` | `/world-cup` · `/teams/[equipo]` | Noticias verificadas, reportes de partido, declaraciones oficiales |
| **The Athletic** | `https://theathletic.com/football/` | `/tag/world-cup-2026/` | Análisis táctico profundo, reportes de insiders, crónicas de vestuario |
| **Reuters Sports** | `https://www.reuters.com/sports/` | `/soccer/` · `/world-cup/` | Wire service, noticias de última hora verificadas, datos de agencia |
| **Marca** | `https://www.marca.com/` | `/futbol/mundial/` | Noticias de equipos hispanohablantes, convocatorias |
| **Goal.com** | `https://www.goal.com/` | `/en/news/` | Noticias globales — validar siempre cruzando con ESPN/BBC |

### Tier 4 — Datos contextuales y estructurales

| Fuente | URL base | Qué obtener |
|---|---|---|
| **Weather.com** | `https://weather.com/` | Pronóstico para sedes de partidos |
| **TimeandDate** | `https://www.timeanddate.com/` | Husos horarios, diferencias horarias por sede |

### Tier 5 — Último recurso (siempre validar con Tier 1-2)

> ⛔ **No usar como fuente primaria de datos deportivos.** Solo aceptable para información estática (capacidad de estadios, fechas históricas, altitud de sedes) y únicamente cuando no existe alternativa en Tiers 1-4. **Obligatorio cruzar con fuente de Tier 1 o Tier 2.**

| Fuente | URL base | Uso permitido | Restricción |
|---|---|---|---|
| **Wikipedia** | `https://en.wikipedia.org/wiki/2026_FIFA_World_Cup` | Capacidad de estadios, altitud, historia de torneos anteriores | Nunca como fuente única; nunca para estadísticas de jugadores o resultados recientes |

## Estrategias de extracción por tipo de dato

### Estadísticas de equipo
1. Buscar primero en **FBref** → datos más completos y con métricas avanzadas.
2. Complementar con **WhoScored** para ratings y formaciones.
3. Usar `fetch_webpage` con la URL directa del equipo en FBref.
4. Patrón de URL FBref: `https://fbref.com/en/squads/[ID]/[Equipo]-Stats`

### Estadísticas de jugador
1. **FBref** para stats de temporada (goles, asistencias, xG, minutos).
2. **Transfermarkt** para valor de mercado, historial de lesiones, trayectoria.
3. **SofaScore** para ratings promedio y tendencia reciente.

### Head-to-head
1. **Soccerway** → historial completo de enfrentamientos.
2. **SofaScore** → h2h con stats comparadas.
3. Buscar: `[Equipo A] vs [Equipo B] head to head history`

### Lesiones y disponibilidad
1. **Transfermarkt** → sección de lesiones del equipo: `https://www.transfermarkt.com/[equipo]/ausfaelle/verein/[ID]`
2. **FotMob** → lista de ausentes por partido.
3. Cruzar con noticias recientes de ESPN/BBC para confirmar.

### Noticias de última hora
1. **ESPN primero**: `https://www.espn.com/soccer/league/_/name/FIFA.WORLD` — cobertura amplia y actualizada.
2. **BBC como segundo canal**: `https://www.bbc.com/sport/football/world-cup` — noticias verificadas.
3. Buscar en Google: `[Equipo] World Cup 2026 news site:espn.com OR site:bbc.com OR site:reuters.com OR site:theathletic.com`
4. Filtrar por última semana para relevancia.
5. Validar cruzando entre al menos 2 fuentes de Tier 3.
6. **No usar Wikipedia para noticias** — sus artículos de noticias pueden estar desactualizados o carecer de verificación editorial.

### Ranking FIFA
1. Fuente única oficial: `https://www.fifa.com/fifa-world-ranking`
2. Frecuencia de actualización: mensual (tras ventanas FIFA).

### Factores contextuales (sede/clima)
1. Identificar sede del partido desde calendario FIFA.
2. **Weather.com** para pronóstico de la fecha.
3. **FIFA.com** o **ESPN** para datos del estadio (capacidad, altitud). Wikipedia solo si no está disponible en estas fuentes y marcando confianza Media.
4. **TimeandDate** para diferencia horaria respecto al país del equipo.

## Patrones de búsqueda optimizados

Usar estos patrones al buscar en la web — están diseñados para maximizar relevancia:

| Tipo de dato | Patrón de búsqueda (inglés) |
|---|---|
| Stats de equipo | `[Country] national football team 2025-2026 statistics site:fbref.com` |
| Lesiones | `[Country] World Cup 2026 injury news latest` |
| Forma reciente | `[Country] national team results 2025 2026` |
| Táctica | `[Country] [Manager name] tactics formation analysis` |
| H2H | `[Country A] vs [Country B] all time record head to head` |
| Convocatoria | `[Country] World Cup 2026 squad list confirmed` |
| xG y avanzadas | `[Country] expected goals xG 2025-26 site:fbref.com OR site:understat.com` |

## Protocolo de validación cruzada

Antes de almacenar un dato en `Informacion/`, valida así:

| Nivel de confianza | Criterio |
|---|---|
| **Alta** | Dato presente en fuente Tier 1, o confirmado por 2+ fuentes Tier 2. |
| **Media** | Dato de una sola fuente Tier 2, o de Tier 3 sin contradecir Tier 1-2. |
| **Baja** | Solo una fuente Tier 3, o dato de redes sociales/rumores. Marcar como provisional. |

Siempre incluye el nivel de confianza en la ficha del equipo junto al dato.

## Manejo de bloqueo de fuentes (HTTP 403/429)

Algunas fuentes deportivas pueden bloquear extracción automática en determinados momentos.
Si ocurre, aplica esta secuencia:

1. Marcar la fuente como temporalmente bloqueada en tus notas de trabajo.
2. Buscar la misma métrica en otra fuente del mismo Tier (o del siguiente si no hay alternativa).
3. Confirmar con una segunda fuente cuando sea posible.
4. Registrar explícitamente en el output final:
  - Fuente primaria intentada (bloqueada)
  - Fuente de reemplazo usada
  - Nivel de confianza final del dato

Nunca inventes ni extrapoles estadísticas cuando una fuente esté bloqueada.

## Registro mínimo de fuentes por entrega

Cada entrega (ficha o dataset) debe cerrar con:

- Fecha de consulta (YYYY-MM-DD)
- URL exacta de cada fuente usada
- Nivel de confianza por bloque de datos (Alta/Media/Baja)

## Reglas de priorización

Cuando tengas múltiples tareas pendientes, prioriza en este orden:
1. **Actualizaciones críticas**: lesiones de titulares, cambios de DT, sanciones.
2. **Fichas pre-partido**: enfrentamientos próximos en los siguientes 3 días.
3. **Fichas de equipo incompletas**: equipos sin ficha o con ficha desactualizada.
4. **Enriquecimiento**: agregar métricas avanzadas a fichas que solo tienen datos básicos.
5. **Monitoreo general**: noticias y tendencias del panorama mundialista.
