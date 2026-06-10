---
name: prompt-optimizer
description: >
  Pre-procesa y optimiza prompts antes de enviarlos a cualquier agente.
  Analiza claridad, contexto, formato y ambigüedad; aplica técnicas de prompt engineering;
  traduce estratégicamente al idioma con mayor cobertura del dominio y devuelve la respuesta en español.
  SIEMPRE ACTIVA: esta skill se ejecuta automáticamente en CADA consulta del chat como capa de
  pre-procesamiento. No requiere activación explícita del usuario. Toda respuesta final se entrega
  en español, incluso si internamente se procesó en otro idioma.
---

# Prompt Optimizer

Capa inteligente de pre-procesamiento que se ejecuta **siempre** en cada consulta del chat. Analiza, mejora y optimiza el prompt antes de procesarlo, y garantiza que la respuesta final se entregue en español.

## Activación

**Siempre activa.** Esta skill se ejecuta automáticamente como primera capa en cada interacción del chat, sin necesidad de que el usuario lo solicite. Opera de forma transparente:

1. Recibe el prompt del usuario.
2. Lo analiza y optimiza internamente.
3. Procesa la petición (traduciendo a otro idioma si el dominio lo requiere).
4. Entrega la respuesta **siempre en español**.

## Flujo de procesamiento

Sigue estos pasos en orden estricto:

### Paso 1 — Recepción
Recibe el prompt original del usuario tal como fue escrito.

### Paso 2 — Análisis de calidad
Evalúa el prompt en estas dimensiones:

| Dimensión | Qué buscar |
|---|---|
| **Claridad** | ¿Las instrucciones son entendibles sin ambigüedad? |
| **Contexto** | ¿Tiene suficiente información de fondo para que el agente actúe? |
| **Especificidad** | ¿Define criterios de aceptación, formato de salida, restricciones? |
| **Estructura** | ¿El formato es adecuado para el tipo de tarea? |
| **Alcance** | ¿El scope está definido o es abierto de forma no intencional? |

Si el prompt es **demasiado ambiguo** para mejorarlo con confianza (falla en 3+ dimensiones sin forma de inferir la intención), solicita clarificación al usuario antes de continuar. Sé específico sobre qué información falta.

### Paso 3 — Mejora
Aplica las técnicas de prompt engineering relevantes:

- **Especificidad**: Transforma instrucciones vagas en directivas concretas con criterios medibles.
- **Contexto explícito**: Inyecta información relevante del proyecto (Mundial 2026, datos históricos, equipos, etc.).
- **Formato estructurado**: Elige el patrón óptimo según la tarea:
  - *Chain-of-Thought* → razonamiento paso a paso para análisis complejos
  - *Few-Shot* → ejemplos concretos para tareas con formato esperado definido
  - *Role-Playing* → asignación de rol experto cuando el dominio lo requiere
  - *Paso a paso* → instrucciones secuenciales para workflows
- **Restricciones claras**: Define límites, formato de salida y criterios de éxito.
- **Descomposición**: Si el prompt pide múltiples cosas, sepáralo en sub-tareas ordenadas.

### Paso 4 — Traducción estratégica
Evalúa si el dominio del prompt tiene mayor cobertura de información en otro idioma:

- **Fútbol, deportes internacionales, estadísticas FIFA** → traducir a inglés.
- **Contexto local o cultural específico** → mantener en español.
- **Dominio técnico (ML, código)** → evaluar caso a caso.

Si traduce:
1. Convierte el prompt optimizado al idioma objetivo.
2. Procesa la petición en ese idioma.
3. **Siempre traduce la respuesta de vuelta a español** antes de entregarla al usuario, manteniendo terminología técnica cuando sea apropiado.

### Paso 5 — Entrega
Entrega la respuesta **siempre en español**, independientemente del idioma en que se haya procesado internamente. Si se aplicó traducción estratégica, añade una nota breve al final indicando el idioma utilizado.

## Formato de salida del análisis

Cuando el usuario pida explícitamente ver el análisis (no solo el prompt mejorado), usa este formato:

```
## Análisis del prompt original
- **Claridad**: [Alta/Media/Baja] — [observación]
- **Contexto**: [Suficiente/Parcial/Insuficiente] — [observación]
- **Especificidad**: [Alta/Media/Baja] — [observación]
- **Estructura**: [Adecuada/Mejorable] — [observación]
- **Alcance**: [Definido/Ambiguo] — [observación]

## Mejoras aplicadas
1. [Mejora 1]
2. [Mejora 2]
...

## Prompt optimizado
[El prompt mejorado listo para usar]

## Traducción
- **Aplicada**: [Sí/No]
- **Idioma**: [Si aplica]
- **Razón**: [Si aplica]
```

## Ejemplo

**Prompt original:**
> "Dame predicciones para el grupo A"

**Análisis:**
- Claridad: Baja — no especifica qué tipo de predicción (resultado, goles, clasificación).
- Contexto: Insuficiente — no indica qué modelo usar ni qué datos considerar.
- Especificidad: Baja — sin formato de salida ni criterios.

**Prompt optimizado:**
> "Genera predicciones de resultado (victoria/empate/derrota) para los 6 partidos de la fase de grupos del Grupo A del Mundial 2026. Usa el modelo de clasificación entrenado con datos históricos de FIFA (2010-2026). Para cada partido incluye: equipos, resultado predicho, probabilidad de cada desenlace (1X2) y confianza del modelo. Formato: tabla con columnas [Partido, Predicción, P(1), P(X), P(2), Confianza]."

## Mejora continua

Esta skill evoluciona con el uso:
- Registra las optimizaciones aplicadas y los resultados obtenidos.
- Incorpora nuevas técnicas de prompt engineering conforme aparezcan.
- Ajusta las reglas de traducción estratégica según efectividad medida por dominio.
