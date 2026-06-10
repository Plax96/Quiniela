# Handoff de informacion para el siguiente agente

Fecha: 2026-06-06
Origen: Auditoria tecnica de `Informacion/` y `Informacion/datasets/`
Destino sugerido: Agente ML (entrenamiento) y Agente Analitico (diagnostico)

## 1) Estado general del paquete recibido

- Cobertura de equipos mundialistas: 48/48 equipos en `equipos.csv` con grupos A-L completos (4 por grupo).
- Cobertura de jugadores: 251 registros en `jugadores.csv` (48 codigos de equipo).
- Cobertura de partidos historicos: 14 filas en `partidos_historicos.csv`.
- Cobertura H2H: 1 fila en `h2h.csv`.
- Cobertura de partidos objetivo: 3 filas en `contexto_partidos.csv`.

Diagnostico de readiness:
- Integridad de claves basicas: aceptable para unir `equipos` y `jugadores`.
- Densidad predictiva para modelado robusto: baja (faltan variables avanzadas y volumen historico).
- Uso recomendado inmediato: baseline probabilistico + reglas por ranking/forma/localia, con confianza mayormente baja-media.

## 2) Hallazgos criticos (bloqueantes de calidad alta)

### 2.1 Nulos mas relevantes en CSV

`equipos.csv` (48 filas):
- `xg`, `xga`, `ppda`, `pases_progresivos`, `efectividad_set_pieces`: 100% nulo.
- `goles_favor`, `goles_contra`: 95.8% nulo.
- `posesion_prom`: 93.8% nulo.
- `ranking_fifa`, `esquema_tactico`: 91.7% nulo.
- `dt`: 87.5% nulo.

`jugadores.csv` (251 filas):
- `minutos_jugados`, `xg_jugador`: 100% nulo.
- `asistencias`: 99.2% nulo.
- `club`: 74.9% nulo.

`partidos_historicos.csv` (14 filas):
- `fase`, `xg_1`, `xg_2`: 100% nulo.
- `ranking_2`: 78.6% nulo.

`contexto_partidos.csv` (3 filas):
- `altitud_m`, `temperatura_c`, `humedad_pct`, `distancia_viaje_1_km`, `distancia_viaje_2_km`: 100% nulo.

### 2.2 Cobertura historica insuficiente

- Solo 12/48 equipos aparecen en `partidos_historicos.csv`.
- 36/48 equipos no tienen historial de partidos en ese dataset.
- `h2h.csv` tiene solo 1 enfrentamiento.

### 2.3 Inconsistencias de catalogo FIFA

En `partidos_historicos.csv` aparecen codigos fuera del catalogo de 48 equipos cargados:
- `CMR`, `CUR`, `GRE`, `KOS`, `ROU`.

Nota: esto no siempre es error (pueden ser rivales externos), pero debe etiquetarse como `rival_fuera_mundial=true` para evitar mezclas al entrenar modelos de quiniela del Mundial.

## 3) Diagnostico de fichas Markdown para PLN

- Total de fichas de equipo: 48.
- Mediana de longitud: 21 lineas (min 20, max 94).
- Fichas con seccion `Noticias`: 4.
- Fichas con seccion `Jugadores`: 4.
- Fichas mas completas detectadas: `usa.md`, `paraguay.md`, `turquia.md`, `australia.md`.

Implicacion:
- El texto actual sirve para contexto descriptivo, pero no para PLN consistente multi-equipo.
- Evitar sobreponderar features textuales hasta homogeneizar estructura de fichas.

## 4) Instrucciones operativas para el siguiente agente (usar ya)

1. Base de entrenamiento actual:
- Usar `equipos.csv` + `jugadores.csv` como tablas principales.
- Usar `partidos_historicos.csv` y `h2h.csv` solo como senal auxiliar de baja cobertura.

2. Estrategia de modelado recomendada en esta iteracion:
- Construir baseline calibrado (logistic/multinomial) con features robustas disponibles:
  - ranking (cuando exista), puntos_forma, condicion sede/local, grupo, victorias/empates/derrotas.
- Aplicar imputacion conservadora y bandera de faltantes por feature clave.
- Marcar predicciones como `confianza=baja` cuando dependan de columnas 100% nulas.

3. Regla de uso de PLN:
- Activar PLN solo para los 4 equipos con fichas extendidas.
- Para el resto, setear features textuales neutrales (0) + bandera `texto_insuficiente=1`.

4. Riesgo metodologico:
- No comparar esta version contra objetivos de accuracy altos; tratarla como `baseline_v01` de arranque.

## 5) Solicitudes de mejora para Buscador (prioridad alta)

## Solicitud A (critica) - Enriquecer `partidos_historicos.csv`

Minimo esperado:
- Cobertura: ultimos 15 partidos por cada uno de los 48 equipos.
- Campos obligatorios completos: `fecha`, `equipo_1`, `equipo_2`, `goles_1`, `goles_2`, `resultado`, `competicion`, `fase`, `ranking_1`, `ranking_2`, `sede`, `neutral`.
- Campos avanzados deseables: `xg_1`, `xg_2`.

## Solicitud B (critica) - Completar metricas avanzadas en `equipos.csv`

Completar para los 48 equipos:
- `xg`, `xga`, `ppda`, `posesion_prom`, `pases_progresivos`, `efectividad_set_pieces`, `goles_favor`, `goles_contra`.

## Solicitud C (alta) - Mejorar `jugadores.csv`

Para al menos top 8 jugadores por equipo:
- `club`, `minutos_jugados`, `xg_jugador`, `asistencias`, `estado_fisico`, `titular_probable`.

## Solicitud D (media-alta) - Ampliar `h2h.csv`

- Incluir ultimos 5-10 enfrentamientos por cada partido del Mundial proyectado (cuando existan).
- Si no existe historial directo, agregar un registro explicito con `sin_historial=true`.

## Solicitud E (media) - Homogeneizar fichas `.md`

Estructura minima por equipo:
- Perfil
- Jugadores clave
- Ultimos 5 partidos
- Fortalezas y debilidades
- Noticias relevantes (3-5 items con fecha y fuente)
- Confianza de informacion (Alta/Media/Baja + por que)

## 6) Criterios de aceptacion para cerrar mejora de datos

Se considera listo para pasar a entrenamiento robusto cuando:
- `partidos_historicos.csv` tenga >= 720 filas (48 equipos x 15 partidos, aproximado sin deduplicar).
- `h2h.csv` tenga cobertura para todos los cruces de `contexto_partidos.csv`.
- Nulos en columnas clave de `equipos.csv` bajen por debajo de 20%.
- Cada equipo tenga al menos 8 jugadores con metricas no nulas en `jugadores.csv`.
- Al menos 80% de fichas tenga seccion `Noticias` y `Jugadores` completas.

## 7) Conclusión ejecutiva

El paquete actual permite arrancar una primera iteracion de prediccion, pero no soporta aun un modelo de alta confianza. La prioridad inmediata debe ser aumentar cobertura historica y completar metricas avanzadas para evitar que el modelo dependa de imputaciones masivas.

## 8) Entregables automaticos para ejecucion del Buscador

Se genero un checklist detallado por equipo con scoring de prioridad para cerrar brechas con mayor impacto en precision de quiniela:

- `Logs/mejora_info_buscador/checklist_automatico_por_equipo_2026-06-06.md`
- `Logs/mejora_info_buscador/checklist_automatico_por_equipo_2026-06-06.csv`

Uso recomendado:
1. Ordenar por `priority_score` descendente.
2. Completar primero equipos `Critica` y `Alta`.
3. Recalcular el checklist tras cada lote de actualizacion para medir reduccion de brecha.

## 9) Complemento post-corridas A-L (estado consolidado)

Se confirma cobertura completa de grupos A-L en estructura base, pero persiste una brecha importante de densidad para modelado:

- `equipos.csv`: 48/48 equipos (estructura completa), pero con nulos masivos en variables de rendimiento.
- `jugadores.csv`: 251 filas para 48 equipos (promedio ~5.2 por equipo), aun por debajo del objetivo operativo de 8 jugadores por equipo.
- `partidos_historicos.csv`: 14 filas totales (muy por debajo del minimo recomendado de 720 para baseline robusto por ventana de 15 partidos por equipo).
- `h2h.csv`: 1 fila.
- `contexto_partidos.csv`: 3 filas.
- Fichas MD de equipo: 48/48 presentes, pero solo 4/48 incluyen secciones `Jugadores` y `Noticias`.

Interpretacion para ML:
- Hay cobertura horizontal (todos los equipos), pero no cobertura vertical suficiente (profundidad historica y metricas avanzadas).
- La siguiente iteracion debe enfocarse en cerrar densidad de datos antes de optimizar hiperparametros.

## 10) Plan de remediacion priorizado y medible (v02 y v03)

### Iteracion v02 (prioridad inmediata, 1-2 lotes)

Objetivo: habilitar un baseline mejorado con menos imputacion.

Umbrales de salida v02:
- `equipos.csv`: nulos en bloque avanzado (`xg`, `xga`, `ppda`, `posesion_prom`, `pases_progresivos`, `efectividad_set_pieces`) <= 60%.
- `jugadores.csv`: >= 8 jugadores por equipo para al menos 24/48 equipos; `club` no nulo <= 30% de faltantes globales.
- `partidos_historicos.csv`: >= 240 filas (meta intermedia), con cobertura de al menos 24 equipos y sin codigos vacios.
- MD: secciones `Jugadores` y `Noticias` presentes en al menos 24 fichas.

### Iteracion v03 (cierre de brecha para entrenamiento robusto)

Objetivo: dejar el paquete listo para entrenamiento principal y evaluacion analitica comparativa.

Umbrales de salida v03:
- `equipos.csv`: nulos en columnas clave < 20%.
- `jugadores.csv`: 48/48 equipos con >= 8 jugadores y campos clave (`club`, `minutos_jugados`, `xg_jugador`, `asistencias`) con completitud >= 80%.
- `partidos_historicos.csv`: >= 720 filas y presencia de los 48 codigos FIFA del mundial.
- `h2h.csv`: cobertura de todos los cruces activos en `contexto_partidos.csv`.
- MD: >= 80% de fichas con `Perfil`, `Jugadores`, `Noticias` y minimo de 3 items fechados en noticias.

## 11) Handoff incremental recomendado entre agentes

Para evitar bloqueos y acelerar ciclos:

1. Buscador publica entregable `v02` al cerrar cada 12 equipos o 2 grupos, lo que ocurra primero.
2. ML consume `v02` parcial para recalcular metricas de sensibilidad a faltantes y devuelve feedback en `Logs/mejoras/`.
3. Buscador ejecuta `v03` sobre los equipos con peor `priority_score` del checklist automatico.
4. Analitico valida mejora entre `baseline_v01` vs `baseline_v02` vs `modelo_v03` con trazabilidad de cobertura.

Formato sugerido de versionado en archivos de intercambio:
- `Resultados/predicciones_v02_YYYY-MM-DD.csv`
- `Resultados/metricas_v02_YYYY-MM-DD.csv`
- `Logs/mejoras/mejoras_para_buscador_v03_YYYY-MM-DD.md`

Condicion de pase a entrenamiento final:
- Solo avanzar a corrida final cuando los umbrales de v03 esten cumplidos o cuando se documente explicitamente que la brecha residual no cambia decisiones de quiniela.
