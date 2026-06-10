---
name: sports-data-deep
description: >
  Recopilación profunda y estructurada de datos deportivos para alimentar modelos de ML y PLN.
  Úsame SIEMPRE cuando necesites estadísticas detalladas de jugadores (en su club y selección),
  estadísticas de equipos por campaña, resultados históricos con marcadores, datos de eliminatorias
  mundialistas, o cuando el Agente Buscador necesite construir datasets ricos para predicciones.
  También actívame cuando se mencione: "estadísticas por jugador", "stats de liga", "eliminatorias",
  "marcadores históricos", "datos para ML", "features para entrenamiento", "dataset de partidos",
  "rendimiento en ligas", "selección y club". Cubre esquemas CSV, fuentes por tipo de dato y
  estrategias de extracción en capas para máxima cobertura de datos.
---

# Sports Data Deep — Recopilación Profunda para ML y PLN

Guía de esquemas, fuentes y estrategias para construir datasets ricos y completos orientados al entrenamiento de modelos de predicción del Mundial 2026.

## Operación recomendada (Copilot junio 2026)

- Revisa primero `/chronicle` para reutilizar decisiones y fuentes ya validadas en iteraciones previas.
- En análisis con muchos equipos/jugadores/partidos, usa modelos con ventana de contexto amplia para preservar consistencia entre capas.
- Ajusta reasoning level a alto para resolver conflictos entre fuentes o discrepancias de métricas históricas.

---

## Por qué importa recopilar en capas

Un modelo de ML de alta calidad necesita datos en **tres capas**:

| Capa | Tipo de dato | Impacto en el modelo |
|---|---|---|
| **Capa 1 — Jugador** | Stats individuales en club + selección | Mide forma actual, confianza, rendimiento colectivo |
| **Capa 2 — Equipo** | Stats agregadas de eliminatorias + partidos recientes | Captura identidad táctica, cohesión, presión grupal |
| **Capa 3 — Partido** | Marcadores históricos + xG + contexto | Aprende patrones de resultado por rival, sede, competición |

Y una **cuarta capa para PLN**:

| Capa | Tipo de dato | Impacto en PLN |
|---|---|---|
| **Capa 4 — Texto** | Declaraciones, conferencias de prensa, reportes de partidos | Detecta moral, confianza, presión mediática, narrativas |

---

## CAPA 1 — Estadísticas por Jugador

### 1A. Estadísticas en su Club (temporada actual + anterior)

Fuentes primarias: **FBref** → **Transfermarkt** → **SofaScore** → **WhoScored**

| Campo | Descripción | Fuente |
|---|---|---|
| `jugador_id` | Nombre normalizado + país | — |
| `club` | Equipo del jugador | Transfermarkt |
| `liga` | División y país de la liga | Transfermarkt |
| `temporada` | p.ej. `2025-26` | FBref |
| `partidos_jugados` | Apariciones totales | FBref |
| `minutos` | Minutos jugados | FBref |
| `goles` | Goles anotados | FBref |
| `asistencias` | Asistencias directas | FBref |
| `xG` | Expected Goals acumulados | FBref/Understat |
| `xA` | Expected Assists acumulados | FBref |
| `npxG` | xG sin penaltis | FBref |
| `tiros` | Total de tiros | FBref |
| `tiros_a_puerta` | Tiros entre los tres palos | FBref |
| `pases_clave` | Pases que generan tiro | FBref/WhoScored |
| `pases_progresivos` | Pases que avanzan >10m | FBref |
| `regates_completados` | Dribbles exitosos | SofaScore |
| `duelos_aereos_ganados` | Duelos de cabeza | WhoScored |
| `tackles_ganados` | Entradas exitosas | FBref |
| `intercepciones` | Balones interceptados | FBref |
| `tarjetas_amarillas` | Acumuladas en la temporada | Transfermarkt |
| `tarjetas_rojas` | Expulsiones | Transfermarkt |
| `rating_promedio` | Rating general de la temporada | SofaScore/WhoScored |
| `forma_5_partidos` | Rating promedio últimos 5 juegos | SofaScore |

**URL patrón FBref jugador:**
```
https://fbref.com/en/players/[ID]/[nombre]-Stats
https://fbref.com/en/players/[ID]/matchlogs/[temporada]/summary/[nombre]-Match-Logs
```

**Búsqueda Google:**
```
[Nombre jugador] 2025-26 season stats site:fbref.com
[Nombre jugador] statistics transfermarkt 2025-26
```

### 1B. Estadísticas en Selección Nacional

Fuentes primarias: **FBref (selecciones)** → **FIFA.com** → **Transfermarkt (carrera internacional)**

| Campo | Descripción |
|---|---|
| `seleccion` | Código FIFA del país |
| `partidos_seleccion` | Total caps internacionales |
| `goles_seleccion` | Goles con la selección |
| `asistencias_seleccion` | Asistencias con la selección |
| `minutos_seleccion` | Minutos en selección |
| `xG_seleccion` | xG acumulados con la selección |
| `partidos_eliminatorias` | Partidos en ruta al Mundial 2026 |
| `goles_eliminatorias` | Goles específicamente en eliminatorias |
| `minutos_eliminatorias` | Minutos en eliminatorias |
| `ultimo_partido_seleccion` | Fecha y rival del último partido |
| `convocado_mundial` | `sí/no/probable` |

**URL patrón FBref selección:**
```
https://fbref.com/en/squads/[ID]/[pais]-Stats
https://fbref.com/en/squads/[ID]/[temporada]/matchlogs/[pais]-Match-Logs
```

### Schema CSV: `jugadores.csv`

```
jugador,pais,posicion,club,liga,temporada,partidos_jugados,minutos,goles,asistencias,
xG,xA,npxG,tiros,tiros_puerta,pases_clave,pases_progresivos,regates,duelos_aereos,
tackles,intercepciones,amarillas,rojas,rating_promedio,forma_5p,
partidos_seleccion,goles_seleccion,asistencias_seleccion,xG_seleccion,
partidos_eliminatorias,goles_eliminatorias,convocado_mundial,confianza,fuente
```

---

## CAPA 2 — Estadísticas por Equipo

### 2A. Campaña de Eliminatorias (clasificación al Mundial 2026)

Esto es crítico para ML: cómo llegó el equipo al mundial define su nivel real.

Fuentes: **FBref (selecciones nacionales)** → **Soccerway** → **ESPN** → **FIFA.com**

| Campo | Descripción |
|---|---|
| `equipo` | Nombre del equipo |
| `confederacion` | UEFA / CONMEBOL / CONCACAF / CAF / AFC / OFC |
| `partidos_elim` | Total de partidos de eliminatorias |
| `ganados_elim` | Victorias |
| `empatados_elim` | Empates |
| `perdidos_elim` | Derrotas |
| `goles_favor_elim` | Goles anotados en eliminatorias |
| `goles_contra_elim` | Goles recibidos en eliminatorias |
| `diferencia_goles_elim` | GF - GC |
| `puntos_elim` | Puntos obtenidos |
| `xG_elim` | Expected Goals en eliminatorias |
| `xGA_elim` | Expected Goals contra en eliminatorias |
| `posesion_elim` | Posesión promedio % |
| `tiros_a_puerta_elim` | Tiros a puerta promedio |
| `goles_local_elim` | Goles como local |
| `goles_visitante_elim` | Goles como visitante |
| `limpias_elim` | Porterías a cero |

**Búsqueda Google:**
```
[País] World Cup 2026 qualification statistics site:fbref.com
[País] CONMEBOL/UEFA qualifying campaign 2026 results
[Confederación] World Cup qualifying table standings 2026
```

### 2B. Estadísticas Agregadas Recientes (últimos 15-20 partidos)

| Campo | Descripción |
|---|---|
| `posesion_promedio` | % posesión promedio |
| `xG_promedio` | xG por partido |
| `xGA_promedio` | xGA por partido |
| `goles_promedio_favor` | Goles/partido como atacante |
| `goles_promedio_contra` | Goles/partido en contra |
| `tiros_favor` | Tiros/partido a favor |
| `tiros_contra` | Tiros/partido en contra |
| `PPDA` | Pases permitidos por acción defensiva |
| `pases_progresivos` | Pases progresivos/partido |
| `set_pieces_conversion` | % de efectividad en set pieces |
| `rendimiento_local` | W/D/L como local (últimos 12 meses) |
| `rendimiento_visitante` | W/D/L como visitante |
| `racha_actual` | Últimos 5 resultados (ej. `W W D L W`) |

### Schema CSV: `equipos.csv`

```
equipo,codigo_fifa,grupo,ranking_fifa,confederacion,dt,formacion_principal,
partidos_elim,ganados_elim,empatados_elim,perdidos_elim,goles_favor_elim,goles_contra_elim,
xG_elim,xGA_elim,posesion_elim,
posesion_reciente,xG_reciente,xGA_reciente,PPDA,goles_promedio_favor,goles_promedio_contra,
rendimiento_local,rendimiento_visitante,racha_actual,
set_pieces_conversion,limpias_recientes,confianza,fuente
```

---

## CAPA 3 — Estadísticas por Partido (histórico completo)

### 3A. Partidos de Eliminatorias (todos los partidos, no solo el resumen)

Fuentes: **Soccerway** → **FBref** → **ESPN** → **FIFA.com**

| Campo | Descripción |
|---|---|
| `fecha` | YYYY-MM-DD |
| `equipo_local` | Nombre equipo local |
| `equipo_visitante` | Nombre equipo visitante |
| `goles_local` | Goles del local |
| `goles_visitante` | Goles del visitante |
| `resultado` | `L` (local gana) / `V` (visitante gana) / `E` (empate) |
| `competicion` | Nombre de la fase de eliminatorias |
| `sede` | Ciudad/país del partido |
| `es_local_en_casa` | Si el "local" jugó en su país (`sí/no`) |
| `xG_local` | xG del equipo local (si disponible) |
| `xG_visitante` | xG del visitante |
| `posesion_local` | % posesión local |
| `tiros_local` | Tiros totales del local |
| `tiros_visitante` | Tiros totales del visitante |
| `amarillas_local` | Tarjetas amarillas local |
| `amarillas_visitante` | Tarjetas amarillas visitante |
| `publico` | Asistencia al estadio |

### 3B. Head-to-Head histórico entre dos selecciones

| Campo | Descripción |
|---|---|
| `fecha` | YYYY-MM-DD |
| `rival_a` | Equipo A |
| `rival_b` | Equipo B |
| `goles_a` / `goles_b` | Marcador final |
| `ganador` | Código FIFA del ganador o `empate` |
| `competicion` | Amistoso / Copa del Mundo / Confederaciones / etc. |
| `fase` | Grupos / Octavos / Cuartos / etc. |
| `sede_neutral` | Si fue en terreno neutral (`sí/no`) |
| `notas` | Penales, prórroga, goles en el 90+ |

**Búsqueda Google:**
```
[País A] vs [País B] all time head to head complete history site:soccerway.com
[País A] [País B] historical results site:fbref.com
```

### Schema CSV: `partidos_historicos.csv`

```
fecha,equipo_local,equipo_visitante,goles_local,goles_visitante,resultado,
competicion,fase,sede,es_local_en_casa,xG_local,xG_visitante,
posesion_local,tiros_local,tiros_visitante,amarillas_local,amarillas_visitante,
publico,penales,prorroga,confianza,fuente
```

---

## CAPA 4 — Datos para PLN (Procesamiento de Lenguaje Natural)

Estos datos son texto libre que el Agente ML convertirá en features de PLN.

### 4A. Qué recopilar

| Tipo | Fuente | Dónde guardar |
|---|---|---|
| Conferencias de prensa | ESPN, BBC, Reuters, Goal.com | `Informacion/pln/prensa/[equipo]/` |
| Declaraciones del DT | ESPN, The Athletic | `Informacion/pln/prensa/[equipo]/` |
| Análisis tácticos de expertos | The Athletic, ESPN FC | `Informacion/pln/analisis/` |
| Reportes post-partido | BBC, Reuters | `Informacion/pln/reportes/[equipo]/` |
| Tweets/posts verificados de jugadores | X (verificar cuenta oficial) | `Informacion/pln/social/` |
| Narrativa mediática previa al partido | ESPN, BBC, Marca | `Informacion/pln/pre_partido/` |

### 4B. Etiquetas de sentimiento para PLN

Cada fragmento de texto debe guardarse con metadatos mínimos:

```
fecha: YYYY-MM-DD
equipo: [código FIFA]
tipo: prensa|declaracion|analisis|reporte|social
fuente: espn|bbc|theathletic|reuters|marca
confianza: Alta|Media|Baja
sentimiento_sugerido: positivo|negativo|neutro|tenso  ← etiqueta humana si es obvia
contenido: "..." (texto literal, máx 500 palabras por fragmento)
```

### Schema archivo: `Informacion/pln/[tipo]/[equipo]/YYYY-MM-DD_[fuente].md`

---

## Patrones de búsqueda optimizados para datos profundos

| Dato buscado | Patrón de búsqueda |
|---|---|
| Stats de jugador en liga | `[Jugador] 2025-26 season statistics goals assists site:fbref.com` |
| Stats de jugador en selección | `[Jugador] international career stats goals caps site:fbref.com` |
| Stats de equipo en eliminatorias | `[País] World Cup 2026 qualifying statistics xG site:fbref.com` |
| Todos los partidos de eliminatorias | `[País] qualification results 2026 complete schedule site:soccerway.com` |
| H2H completo | `[País A] [País B] all time results head to head site:soccerway.com OR site:transfermarkt.com` |
| Forma reciente del equipo | `[País] national team last 10 results 2025 2026 site:soccerway.com` |
| Conferencia de prensa DT | `[DT nombre] press conference World Cup 2026 site:espn.com OR site:bbc.com` |
| Lesiones del equipo | `[País] injuries World Cup 2026 squad site:transfermarkt.com OR site:espn.com` |
| Marcador partido específico | `[País A] vs [País B] [año] [competición] result score` |

---

## Estrategia de extracción por confederación (eliminatorias)

Cada confederación tiene su propia estructura de eliminatorias para el Mundial 2026:

| Confederación | Plazas | Fuente de stats | URL directa |
|---|---|---|---|
| **UEFA** | 16 | FBref + UEFA.com | `https://fbref.com/en/comps/UEFA` |
| **CONMEBOL** | 6 (+1 repechaje) | FBref + CONMEBOL | `https://fbref.com/en/comps/CONMEBOL-WC-Qualifying` |
| **CONCACAF** | 6 (+1 repechaje) | FBref + Soccerway | `https://fbref.com/en/comps/CONCACAF` |
| **CAF (África)** | 9 (+1 repechaje) | FBref + CAFonline | Buscar por `CAF World Cup qualifier 2026 stats` |
| **AFC (Asia)** | 8 (+1 repechaje) | FBref + AFC.com | Buscar por `AFC World Cup qualifier 2026 stats` |
| **OFC** | 1 (+1 repechaje) | Soccerway + OFC | Buscar por `OFC World Cup qualifier 2026 results` |

---

## Checklist de completitud de datos por equipo

Usa esta checklist antes de marcar un equipo como "estable":

### Capa 1 — Jugadores (top 15 por equipo)
- [ ] Stats de temporada actual en el club (goles, asistencias, xG, minutos)
- [ ] Stats de la temporada anterior en el club (comparación de forma)
- [ ] Stats con la selección en eliminatorias
- [ ] Rating y forma reciente (últimos 5 partidos del club)
- [ ] Estado físico (lesiones, sanciones)

### Capa 2 — Equipo
- [ ] Tabla completa de eliminatorias (todos los partidos G/E/P + xG si disponible)
- [ ] Stats agregadas de los últimos 15-20 partidos de la selección
- [ ] Rendimiento local vs visitante diferenciado
- [ ] PPDA y métricas defensivas avanzadas

### Capa 3 — Partidos
- [ ] Todos los partidos de eliminatorias con marcadores y stats (no solo el resumen)
- [ ] Head-to-head con los 3 rivales del grupo (mínimo últimos 10 enfrentamientos cada uno)
- [ ] Al menos 1 partido completo del Mundial anterior si participó

### Capa 4 — PLN
- [ ] Al menos 2 reportes/declaraciones recientes del DT
- [ ] Al menos 1 análisis táctico de fuente confiable
- [ ] Noticias clave de los últimos 30 días

---

## Ejemplo de extracción completa: un jugador

**Objetivo**: obtener datos de Kylian Mbappé para el modelo

1. **Stats de club (Real Madrid, 2025-26)**:
   - `https://fbref.com/en/players/42fd9c7f/Kylian-Mbappe-Stats`
   - Extraer: goles, asistencias, xG, npxG, minutos, rating promedio

2. **Stats con selección francesa**:
   - `https://fbref.com/en/squads/76483902/France-Stats`
   - Buscar su fila en la tabla de la selección

3. **Stats en eliminatorias UEFA**:
   - Buscar: `France UEFA World Cup 2026 qualifier stats site:fbref.com`

4. **Forma reciente**:
   - `https://fbref.com/en/players/42fd9c7f/matchlogs/2025-2026/summary/Mbappe-Match-Logs`

5. **Estado físico**:
   - `https://www.transfermarkt.com/kylian-mbappe/verletzungen/spieler/[ID]`

6. **Narrativa mediática**:
   - Buscar: `Mbappé World Cup 2026 fitness form site:espn.com OR site:theathletic.com`

---

## Criterios de calidad del dataset para ML/PLN

| Criterio | Mínimo aceptable | Óptimo |
|---|---|---|
| Jugadores cubiertos por equipo | 11 titulares | 23 (convocatoria completa) |
| Partidos de eliminatorias cubiertos | Todos los partidos del equipo | + H2H completo |
| Temporadas de estadísticas de club | Temporada actual | Actual + 2 anteriores |
| Fragmentos PLN por equipo | 3 textos | 10+ textos etiquetados |
| Nivel de confianza mínimo | Media | Alta en datos cuantitativos |
| Cobertura de partidos históricos H2H | Últimos 10 | Últimos 20 o todos |
