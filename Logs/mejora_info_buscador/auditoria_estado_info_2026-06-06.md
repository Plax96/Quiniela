# Auditoria de estado de informacion para quiniela

Fecha: 2026-06-06
Estado: NO APTO - persisten problemas criticos

## Volumen actual
- equipos.csv: 48 filas, 23 columnas
- jugadores.csv: 256 filas, 15 columnas
- partidos_historicos.csv: 22 filas, 15 columnas
- h2h.csv: 1 filas, 8 columnas
- contexto_partidos.csv: 3 filas, 13 columnas

## Cobertura y consistencia
- Equipos en catalogo: 48
- Equipos sin partidos historicos: 35
- Muestra equipos sin historico: ALG, ARG, AUT, BIH, CAN, CIV, COD, COL, CPV, CRO, CZE, ECU, EGY, ENG, FRA
- Codigos fuera de catalogo en partidos_historicos: 5
- Lista: CMR, CUR, GRE, KOS, ROU

## Calidad de fichas md
- Fichas totales: 48
- Con seccion Perfil: 48
- Con seccion Jugadores: 4
- Con seccion Noticias: 4

## Problemas criticos detectados
- partidos_historicos muy bajo: 22 filas (<200)
- h2h muy bajo: 1 filas (<20)
- contexto_partidos muy bajo: 3 filas (<6)
- equipos.xg nulo 100.0%
- equipos.xga nulo 100.0%
- equipos.ppda nulo 100.0%
- equipos.pases_progresivos nulo 100.0%
- equipos.efectividad_set_pieces nulo 100.0%
- equipos.goles_favor nulo 95.8%
- equipos.goles_contra nulo 95.8%
- equipos.posesion_prom nulo 93.8%
- jugadores.asistencias nulo 99.2%
- jugadores.minutos_jugados nulo 100.0%
- jugadores.xg_jugador nulo 100.0%
- equipos sin historial en partidos_historicos: 35
- fichas con Noticias insuficientes: 4/48
- fichas con Jugadores insuficientes: 4/48
