# Prompt Maestro Batch — Mundial 2026 (Grupos A-L)
Fecha: 2026-06-06
Agente: Buscador
Modo: Bajo costo (entrada/salida/cache)

## Objetivo
Ejecutar en una sola corrida la actualizacion de uno o varios grupos del Mundial 2026 con este flujo:
1. Deltas en Informacion/datasets/equipos.csv
2. Deltas en Informacion/datasets/jugadores.csv
3. Fichas md por equipo en Informacion/
4. Hito en Logs/prompts/Buscador_YYYY-MM-DD.md

## Parametros editables por corrida
- grupos_objetivo: ejemplo A,B o E,F o I,J,K,L
- codigos_objetivo: lista de codigos FIFA de los equipos a trabajar
- fecha_actualizacion: YYYY-MM-DD
- confianza_objetivo: Alta
- jugadores_por_equipo: 3

## Catalogo de grupos y codigos
- Grupo A: MEX, RSA, KOR, CZE
- Grupo B: CAN, BIH, QAT, SUI
- Grupo C: BRA, MAR, HAI, SCO
- Grupo D: USA, PAR, AUS, TUR
- Grupo E: GER, CUW, CIV, ECU
- Grupo F: NED, JPN, SWE, TUN
- Grupo G: BEL, EGY, IRN, NZL
- Grupo H: ESP, CPV, KSA, URU
- Grupo I: FRA, SEN, IRQ, NOR
- Grupo J: ARG, ALG, AUT, JOR
- Grupo K: POR, COD, UZB, COL
- Grupo L: ENG, CRO, GHA, PAN

## Fuentes permitidas (bajo costo)
1. FIFA standings oficial para validacion de grupo.
2. ESPN teams endpoint para resolver ids y metadatos de equipo.
3. ESPN roster endpoint por equipo para convocatoria base.
4. ESPN scoreboard para contexto pretorneo.

## Reglas operativas
1. Maximo 2 fuentes por dato critico.
2. Prioridad de consulta: ESPN y FIFA.
3. Solo URLs directas de alta senal.
4. Actualizar solo deltas en CSV y fichas md.
5. No duplicar jugadores por llave equipo+jugador.
6. Registrar hito con fuentes y archivos tocados.

## Flujo de ejecucion
1. Resolver ids de equipo por codigo y nombre.
2. Leer roster por equipo.
3. Seleccionar 3 jugadores clave por equipo:
- 1 portero
- 1 defensa
- 1 medio o delantero
4. Upsert en equipos.csv:
- grupo
- confederacion
- estado base pretorneo
- confianza_dato Alta
- fecha_actualizacion
5. Upsert en jugadores.csv:
- equipo
- jugador
- posicion
- estado_fisico disponible
- titular_probable True
- notas con prefijo EST y FAR
- fecha_actualizacion
6. Escribir o actualizar ficha md por equipo.
7. Anexar hito en bitacora diaria.

## Plantilla de ficha md por equipo
- Titulo: Equipo y codigo
- Actualizacion pre-Mundial
- Perfil: grupo, confederacion, dt, estilo
- Fuentes: FIFA standings, ESPN scoreboard, ESPN roster
- Confianza: Alta para campos actualizados

## Validacion minima
- jugadores.csv: jugadores criticos presentes por equipo
- jugadores.csv: sin duplicados por equipo+jugador
- equipos.csv: solo codigos objetivo actualizados en la corrida
- bitacora: hito agregado con fuentes y archivos

## Formato de salida esperado
Un bloque por equipo con:
- Cambios
- Fuentes
- Archivos
- Confianza

## Instruccion de uso rapido
1. Copiar este prompt.
2. Definir grupos_objetivo y codigos_objetivo.
3. Ejecutar una corrida unica.
4. Validar y reportar por bloques.
