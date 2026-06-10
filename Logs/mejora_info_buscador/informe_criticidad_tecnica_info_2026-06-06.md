# Informe de Criticidad Tecnica de Informacion

Fecha: 2026-06-06
Estado global: NO APTO para prediccion de quiniela de baja tasa de error
Objetivo de este informe: documentar de forma tecnica y trazable las brechas de informacion que impiden un rendimiento confiable del sistema de prediccion, y definir las mejoras necesarias para alcanzar calidad de datos apta para ML.

## 1. Resumen ejecutivo

El paquete de datos actual no cumple aun los minimos de calidad para producir predicciones robustas de quiniela con bajo error. Aunque existe cobertura de 48 equipos y una base inicial de jugadores, persisten brechas criticas en tres frentes:

1. Insuficiencia de volumen historico (partidos, h2h, contexto).
2. Alta incompletitud de variables predictivas clave (xG, xGA, PPDA, minutos, asistencias, etc.).
3. Baja estandarizacion de fichas de texto para PLN (secciones Jugadores y Noticias presentes solo en una minoria).

Implicacion tecnica: el modelo queda forzado a imputaciones masivas y features de baja señal, lo que eleva incertidumbre, reduce calibracion de probabilidades y aumenta riesgo de error sistematico en resultados 1X2.

## 2. Fuentes base utilizadas para este dictamen

### 2.1 Artefactos de auditoria y priorizacion
- `Logs/mejora_info_buscador/auditoria_estado_info_2026-06-06.md`
- `Logs/mejora_info_buscador/checklist_automatico_por_equipo_2026-06-06.md`
- `Logs/mejora_info_buscador/checklist_automatico_por_equipo_2026-06-06.csv`

### 2.2 Datasets evaluados
- `Informacion/datasets/equipos.csv`
- `Informacion/datasets/jugadores.csv`
- `Informacion/datasets/partidos_historicos.csv`
- `Informacion/datasets/h2h.csv`
- `Informacion/datasets/contexto_partidos.csv`

### 2.3 Fichas de texto evaluadas
- `Informacion/*.md` (48 fichas de equipos)

### 2.4 Codigo reutilizable de validacion ejecutado
- `Logs/mejora_info_buscador/codigo_reutilizable/auditar_info_quiniela.py`
- `Logs/mejora_info_buscador/codigo_reutilizable/generar_checklist_automatico.py`
- `Logs/mejora_info_buscador/codigo_reutilizable/ejecutar_revision_completa.sh`

## 3. Hallazgos tecnicos de criticidad

## 3.1 Criticidad alta: cobertura historica insuficiente

- `partidos_historicos.csv`: 14 filas.
- `h2h.csv`: 1 fila.
- `contexto_partidos.csv`: 3 filas.
- Equipos sin historial en `partidos_historicos.csv`: 36 de 48.

Impacto:
- Se degrada la capacidad de aprender patrones reales por rival, fase y contexto.
- Se limita seriamente la validacion temporal y por segmentos (fase/grupo).
- Se incrementa riesgo de sobreajuste a pocos casos y predicciones inestables.

## 3.2 Criticidad alta: incompletitud de features estructurales

En `equipos.csv`:
- `xg`, `xga`, `ppda`, `pases_progresivos`, `efectividad_set_pieces`: 100% nulo.
- `goles_favor`, `goles_contra`: 95.8% nulo.
- `posesion_prom`: 93.8% nulo.
- `ranking_fifa`: 91.7% nulo.

En `jugadores.csv`:
- `minutos_jugados`: 100% nulo.
- `xg_jugador`: 100% nulo.
- `asistencias`: 99.2% nulo.

En `partidos_historicos.csv`:
- `fase`: 100% nulo.
- `xg_1`, `xg_2`: 100% nulo.

Impacto:
- Disminuye la capacidad discriminativa del modelo.
- Afecta calibracion de probabilidades (prob_1/prob_x/prob_2).
- Obliga a depender de variables proxy y reglas heuristicas de baja robustez.

## 3.3 Criticidad media-alta: consistencia y trazabilidad de catalogo

- Codigos fuera de catalogo mundial en `partidos_historicos.csv`: `CMR`, `CUR`, `GRE`, `KOS`, `ROU`.

Impacto:
- No es necesariamente error, pero requiere etiquetado explicito de rival externo al mundial para no contaminar features de rivalidad directa.

## 3.4 Criticidad media: bajo readiness de texto para PLN

- Fichas totales: 48.
- Con seccion `Perfil`: 48.
- Con seccion `Jugadores`: 4.
- Con seccion `Noticias`: 4.

Impacto:
- Señal textual no homogénea entre equipos.
- Riesgo de sesgo hacia pocos equipos con texto rico.

## 3.5 Criticidad global por equipo

Resultado del checklist automatico:
- Prioridad Critica: 47 equipos.
- Prioridad Alta: 1 equipo.

Interpretacion:
- El problema no es puntual; es sistemico en casi todo el universo de selecciones.

## 4. Causa raiz tecnica (resumen)

1. Carga inicial orientada a estructura, no a completitud estadistica profunda.
2. Integracion de fuentes sin cierre por umbrales minimos por columna/tabla.
3. Falta de gating de calidad antes de considerar dataset apto para entrenamiento robusto.

## 5. Mejoras requeridas para alcanzar calidad deseada

## 5.1 Umbrales objetivo (obligatorios)

1. `partidos_historicos.csv` >= 720 filas (aprox. 48 equipos x 15 partidos, sin deduplicacion estricta).
2. `h2h.csv` con cobertura para todos los cruces relevantes de `contexto_partidos.csv`.
3. Nulos en columnas clave de `equipos.csv` por debajo de 20%.
4. Minimo 8 jugadores por equipo con datos no nulos en campos criticos (`club`, `minutos_jugados`, `xg_jugador`, `asistencias`, `estado_fisico`).
5. Al menos 80% de fichas MD con secciones `Jugadores` y `Noticias` completas.

## 5.2 Acciones prioritarias (orden de ejecucion)

1. Enriquecer `partidos_historicos.csv` por lote de equipos Critica/Alta.
2. Completar variables avanzadas de `equipos.csv` (xG/xGA/PPDA/pases progresivos/set pieces).
3. Robustecer `jugadores.csv` (minutos, xG jugador, asistencias, estado fisico).
4. Normalizar fichas MD con plantilla unica minima para PLN.
5. Etiquetar explicitamente rivales externos al mundial en historicos.

## 5.3 Controles de calidad recomendados

1. Ejecutar tras cada lote:
   - `./Logs/mejora_info_buscador/codigo_reutilizable/ejecutar_revision_completa.sh`
2. Rechazar lote si rompe schema o deja columnas clave >20% nulo sin justificacion.
3. Mantener `fecha_actualizacion` consistente (YYYY-MM-DD) en todas las tablas.

## 6. Riesgo residual si no se corrige

Si se entrena y predice con el estado actual:
- Mayor varianza en resultados.
- Menor capacidad de generalizacion a cruces no vistos.
- Probabilidades menos calibradas.
- Mayor probabilidad de error en picks de quiniela cerrados.

## 7. Criterio de salida del estado critico

El estado dejara de ser critico cuando:
- Los umbrales del punto 5.1 esten cumplidos y validados por script.
- El checklist reduzca equipos Critica a <= 10 y sin bloqueos estructurales (historicos y variables avanzadas).

## 8. Conclusion tecnica

A la fecha del corte, la calidad de informacion sigue en estado critico para objetivo de quiniela con bajo error. No se recomienda avanzar a una corrida final de prediccion de alta confianza hasta cerrar las brechas estructurales descritas. El pipeline de validacion reutilizable ya esta disponible para monitorear avances y reducir consumo de tokens en futuras revisiones.

## 9. Mapa operativo de cierre de brechas

### 9.1 Prioridad por impacto en ML

Orden de cierre recomendado para maximizar mejora por unidad de esfuerzo:

1. `partidos_historicos.csv`
2. `equipos.csv`
3. `jugadores.csv`
4. `h2h.csv`
5. `Informacion/*.md`

### 9.2 Objetivo minimo por artefacto

`partidos_historicos.csv`
- Llevar la cobertura a >= 720 filas.
- Completar `fecha`, `equipo_1`, `equipo_2`, `goles_1`, `goles_2`, `resultado`, `competicion`, `fase`, `ranking_1`, `ranking_2`, `sede`, `neutral`.
- Agregar `xg_1` y `xg_2` cuando exista fuente valida.

`equipos.csv`
- Reducir nulos en columnas clave por debajo de 20%.
- Completar `xg`, `xga`, `ppda`, `posesion_prom`, `pases_progresivos`, `efectividad_set_pieces`, `goles_favor`, `goles_contra`.

`jugadores.csv`
- Alcanzar al menos 8 jugadores por equipo.
- Completar `club`, `minutos_jugados`, `xg_jugador`, `asistencias`, `estado_fisico`, `titular_probable`.

`h2h.csv`
- Cubrir los cruces relevantes de los partidos objetivo del Mundial.
- Registrar `sin_historial=true` cuando no exista antecedente directo.

`Informacion/*.md`
- Estandarizar `Perfil`, `Jugadores`, `Ultimos 5 partidos`, `Fortalezas y debilidades`, `Noticias relevantes` y `Confianza`.
- Lograr al menos 80% de fichas con `Jugadores` y `Noticias` completas.

### 9.3 Fuentes recomendadas por tipo de dato

- `equipos.csv`: FIFA, FBref, Soccerway, ESPN.
- `jugadores.csv`: FBref, Transfermarkt, SofaScore, WhoScored.
- `partidos_historicos.csv`: Soccerway, FBref, ESPN, FIFA.
- `h2h.csv`: Soccerway y SofaScore, con validacion cruzada.
- `Informacion/*.md`: ESPN, BBC Sport, Reuters, The Athletic.

## 10. Plan de ejecucion para cerrar el paquete completo

### Lote 1

- Completar historial de partidos para los equipos con peor `priority_score`.
- Subir la cobertura de jugadores a 8 por equipo en los mismos equipos.
- Homogeneizar las fichas MD de esos equipos.

### Lote 2

- Completar metricas avanzadas de equipos.
- Rellenar H2H de los cruces que ya existan en calendario o contexto.
- Recalcular el checklist y reordenar por score.

### Lote 3

- Expandir cobertura al resto del universo.
- Revisar consistencia de codigos FIFA y fuentes.
- Revalidar umbrales globales de salida.

## 11. Criterio de salida operativo

Se puede considerar que la informacion ya cerro brechas criticas cuando se cumplan simultaneamente estos tres puntos:

1. El checklist automatico deja de marcar a casi todos los equipos como `Critica`.
2. Las columnas avanzadas ya no dependen de imputacion masiva.
3. ML puede entrenar una version nueva sin marcar `confianza=baja` por falta de cobertura estructural.

## 12. Avance parcial posterior a la sincronizacion local

Tras reutilizar las fichas MD existentes para sincronizar `equipos.csv`, `jugadores.csv` y `partidos_historicos.csv`, el estado actual mejoro de forma puntual pero sigue lejos del umbral de salida:

- `equipos.csv`: 48 filas; `ranking_fifa` reducido a 34 nulos y `dt` casi completo, pero `xg/xga/ppda/pases_progresivos/set pieces` siguen sin cobertura.
- `jugadores.csv`: 256 filas; se incorporaron o refrescaron jugadores desde las fichas MD, pero `minutos_jugados`, `xg_jugador` y `asistencias` siguen casi vacios.
- `partidos_historicos.csv`: 22 filas; subio respecto al corte inicial, aunque aun muy por debajo del minimo funcional.
- Checklist automatico: 45 equipos en Critica y 3 en Alta, lo que confirma una mejora marginal pero no suficiente para entrenamiento robusto.

Interpretacion:
- El repositorio ya no esta en el mismo estado inicial de vacio parcial, pero la señal predictiva sigue siendo insuficiente para una corrida final.
- El siguiente salto real requiere fuentes externas para historia, metricas avanzadas y H2H, no solo reutilizacion de MD local.
