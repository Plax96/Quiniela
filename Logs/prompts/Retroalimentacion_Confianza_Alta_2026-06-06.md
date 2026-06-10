# Retroalimentacion para mantener Confianza Alta
Fecha: 2026-06-06
Agente: Buscador

## Objetivo
Estandarizar como subir de Media a Alta en corridas de equipos por grupo con bajo costo de creditos.

## Regla practica (aplicable de inmediato)
1. Definir alcance: marcar explicitamente que la confianza Alta aplica a los campos actualizados (grupo, forma, convocatoria base), no a metricas no cargadas.
2. Validacion cruzada minima por dato critico:
- Grupo oficial: FIFA standings (Tier 1).
- Forma reciente (5 partidos): ESPN scoreboard/API.
- Convocatoria/disponibilidad base: ESPN roster endpoint.
3. Trazabilidad obligatoria en salida:
- Lista de URLs exactas por equipo.
- Bloque de confianza con criterio textual.
- Fecha de actualizacion alineada entre CSV y MD.

## Checklist rapido por equipo
- [ ] equipos.csv: confianza_dato = Alta
- [ ] equipos.csv: fecha_actualizacion actualizada
- [ ] jugadores.csv: jugadores criticos presentes y sin duplicados
- [ ] ficha MD: bloque "Confianza" explicito
- [ ] ficha MD: al menos 3 fuentes directas

## Plantilla recomendada para bloque de confianza
"Alta para los campos actualizados (grupo, forma y convocatoria base), validado con FIFA (grupo oficial) + ESPN API (forma y roster)."

## Errores comunes que bajan confianza
1. Usar solo una fuente para todos los datos.
2. No diferenciar alcance de la confianza.
3. Cambiar confianza en CSV sin explicar criterio en MD/bitacora.

## Siguiente mejora para sostener Alta
- Incorporar una segunda fuente de disponibilidad (ej. Transfermarkt lesiones) cuando exista noticia de duda/lesion para blindar estados fisicos sensibles.
