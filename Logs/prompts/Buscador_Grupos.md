# Aplicacion de Instrucciones #file:prompts — Grupos G y H
Fecha: 2026-06-06
Agente: Buscador
Modo: Bajo costo (entrada/salida/cache)

## Nota de reutilizacion
- Prompt maestro batch disponible en Logs/prompts/Buscador_Master_Batch.md para ejecutar cualquier bloque de grupos A-L cambiando solo parametros de entrada.

## Equipos Grupo G
- BEL | Belgium
- EGY | Egypt
- IRN | IR Iran
- NZL | New Zealand

## Equipos Grupo H
- ESP | Spain
- CPV | Cabo Verde
- KSA | Saudi Arabia
- URU | Uruguay

## Reglas operativas (aplicadas)
1. Maximo 2 fuentes por dato critico.
2. Prioridad de consulta: ESPN/BBC; tercera fuente solo por conflicto.
3. Solo URLs directas de alta senal (story/report/matchstats), no portadas.
4. Actualizar solo deltas en CSV/MD.
5. Salida compacta por equipo: cambios, fuentes, archivos, confianza.

## Prompt aplicado — BEL (Belgium)
Objetivo:
- Refrescar estado pre-Mundial de Belgium (lesiones, disponibilidad, forma reciente, titulares probables).

Entradas minimas:
- 2 URLs de alta senal (report/story) sobre Belgium.

Tareas:
1. Validar lesiones/sanciones confirmadas.
2. Extraer ultimo bloque de forma reciente (5-10 partidos oficiales).
3. Actualizar solo filas afectadas en jugadores.csv y equipos.csv.
4. Actualizar ficha de equipo en Informacion/belgium.md.

Salida requerida (compacta):
- Cambios: [lista corta]
- Fuentes: [2-3 URLs]
- Archivos: [csv/md tocados]
- Confianza: Alta/Media/Baja

## Prompt aplicado — EGY (Egypt)
Objetivo:
- Refrescar estado pre-Mundial de Egypt con foco en disponibilidad de titulares y tendencia competitiva.

Entradas minimas:
- 2 URLs directas de alta senal sobre Egypt.

Tareas:
1. Confirmar ausencias relevantes y estado fisico.
2. Consolidar forma reciente y rendimiento por contexto (local/visitante si aplica).
3. Aplicar deltas en jugadores.csv y equipos.csv.
4. Actualizar ficha de equipo en Informacion/egypt.md.

Salida requerida (compacta):
- Cambios: [lista corta]
- Fuentes: [2-3 URLs]
- Archivos: [csv/md tocados]
- Confianza: Alta/Media/Baja

## Prompt aplicado — IRN (IR Iran)
Objetivo:
- Refrescar IR Iran con foco en jugadores clave, disponibilidad y forma reciente oficial.

Entradas minimas:
- 2 URLs directas de alta senal sobre IR Iran.

Tareas:
1. Verificar bajas/dudas y condicion de figuras.
2. Consolidar forma reciente y notas tacticas minimas.
3. Actualizar solo filas afectadas en jugadores.csv y equipos.csv.
4. Actualizar ficha de equipo en Informacion/ir_iran.md.

Salida requerida (compacta):
- Cambios: [lista corta]
- Fuentes: [2-3 URLs]
- Archivos: [csv/md tocados]
- Confianza: Alta/Media/Baja

## Prompt aplicado — NZL (New Zealand)
Objetivo:
- Refrescar New Zealand con foco en estado fisico, titulares probables y forma reciente.

Entradas minimas:
- 2 URLs directas de alta senal sobre New Zealand.

Tareas:
1. Confirmar lesiones/sanciones y dudas.
2. Actualizar forma reciente y contexto competitivo.
3. Aplicar deltas en jugadores.csv y equipos.csv.
4. Actualizar ficha de equipo en Informacion/new_zealand.md.

Salida requerida (compacta):
- Cambios: [lista corta]
- Fuentes: [2-3 URLs]
- Archivos: [csv/md tocados]
- Confianza: Alta/Media/Baja

## Prompt aplicado — ESP (Spain)
Objetivo:
- Refrescar Spain (lesiones, disponibilidad, forma reciente y titulares probables).

Entradas minimas:
- 2 URLs directas de alta senal sobre Spain.

Tareas:
1. Validar lesiones/sanciones confirmadas.
2. Consolidar forma reciente oficial.
3. Actualizar solo filas afectadas en jugadores.csv y equipos.csv.
4. Actualizar ficha de equipo en Informacion/spain.md.

Salida requerida (compacta):
- Cambios: [lista corta]
- Fuentes: [2-3 URLs]
- Archivos: [csv/md tocados]
- Confianza: Alta/Media/Baja

## Prompt aplicado — CPV (Cabo Verde)
Objetivo:
- Refrescar Cabo Verde (lesiones, disponibilidad, forma reciente y titulares probables).

Entradas minimas:
- 2 URLs directas de alta senal sobre Cabo Verde.

Tareas:
1. Validar lesiones/sanciones confirmadas.
2. Consolidar forma reciente oficial.
3. Actualizar solo filas afectadas en jugadores.csv y equipos.csv.
4. Actualizar ficha de equipo en Informacion/cabo_verde.md.

Salida requerida (compacta):
- Cambios: [lista corta]
- Fuentes: [2-3 URLs]
- Archivos: [csv/md tocados]
- Confianza: Alta/Media/Baja

## Prompt aplicado — KSA (Saudi Arabia)
Objetivo:
- Refrescar Saudi Arabia (lesiones, disponibilidad, forma reciente y titulares probables).

Entradas minimas:
- 2 URLs directas de alta senal sobre Saudi Arabia.

Tareas:
1. Validar lesiones/sanciones confirmadas.
2. Consolidar forma reciente oficial.
3. Actualizar solo filas afectadas en jugadores.csv y equipos.csv.
4. Actualizar ficha de equipo en Informacion/saudi_arabia.md.

Salida requerida (compacta):
- Cambios: [lista corta]
- Fuentes: [2-3 URLs]
- Archivos: [csv/md tocados]
- Confianza: Alta/Media/Baja

## Prompt aplicado — URU (Uruguay)
Objetivo:
- Refrescar Uruguay (lesiones, disponibilidad, forma reciente y titulares probables).

Entradas minimas:
- 2 URLs directas de alta senal sobre Uruguay.

Tareas:
1. Validar lesiones/sanciones confirmadas.
2. Consolidar forma reciente oficial.
3. Actualizar solo filas afectadas en jugadores.csv y equipos.csv.
4. Actualizar ficha de equipo en Informacion/uruguay.md.

Salida requerida (compacta):
- Cambios: [lista corta]
- Fuentes: [2-3 URLs]
- Archivos: [csv/md tocados]
- Confianza: Alta/Media/Baja

## Validacion minima por corrida
- jugadores.csv: presencia de jugadores críticos por equipo (mínimo 4).
- jugadores.csv: sin duplicados por equipo+jugador.
- equipos.csv: fecha_actualizacion actualizada solo para BEL/EGY/IRN/NZL/ESP/CPV/KSA/URU.

## Entregable final esperado
- 1 bloque de salida por equipo (8 bloques totales).
- Datasets actualizados por deltas.
- Bitacora diaria con solo cambios nuevos.
