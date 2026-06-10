# Skill: Prompt Optimizer

## Propósito

Capa de pre-procesamiento inteligente que recibe cualquier prompt dirigido a un agente, lo analiza, lo mejora y lo entrega optimizado antes de que el agente lo ejecute.

## Capacidades clave

| Capacidad | Descripción |
|---|---|
| **Análisis de calidad** | Detecta ambigüedades, falta de contexto, instrucciones vagas y detalles ausentes que afectan la calidad de respuesta del agente. |
| **Reestructuración** | Reformatea el prompt al formato más efectivo según el tipo de tarea: paso a paso, lista de requisitos, pregunta directa, etc. |
| **Traducción estratégica** | Cuando el dominio tiene mayor cobertura de datos en otro idioma (e.g., fútbol → inglés), traduce el prompt, ejecuta la petición y devuelve la respuesta en español. |
| **Solicitud de clarificación** | Si el prompt es demasiado ambiguo para mejorarlo de forma confiable, solicita información adicional al usuario antes de continuar. |
| **Adaptabilidad** | Maneja desde preguntas simples hasta instrucciones complejas multi-paso, ajustándose al contexto y al agente destino. |

## Flujo de procesamiento

```
Usuario → [Prompt original]
              │
              ▼
   ┌─────────────────────┐
   │  1. Recibir prompt   │
   └──────────┬──────────┘
              ▼
   ┌─────────────────────┐
   │  2. Análisis         │  → Detectar: ambigüedad, contexto faltante, formato inadecuado
   └──────────┬──────────┘
              ▼
        ¿Demasiado ambiguo?
         Sí → Pedir clarificación al usuario → volver a paso 2
         No ↓
   ┌─────────────────────┐
   │  3. Mejora           │  → Aplicar técnicas de prompt engineering
   └──────────┬──────────┘
              ▼
   ┌─────────────────────┐
   │  4. Traducción       │  → ¿El dominio se beneficia de otro idioma?
   │     estratégica      │     Sí → traducir, ejecutar, regresar a español
   └──────────┬──────────┘     No → continuar en español
              ▼
   ┌─────────────────────┐
   │  5. Entrega          │  → Prompt optimizado → Agente destino
   └─────────────────────┘
```

## Técnicas de prompt engineering aplicadas

- **Especificidad**: Transformar instrucciones vagas en directivas concretas con criterios de aceptación.
- **Contexto explícito**: Inyectar información relevante del proyecto (Mundial 2026, datos históricos, etc.).
- **Formato estructurado**: Elegir el formato óptimo (Chain-of-Thought, Few-Shot, Role-Playing, etc.) según la tarea.
- **Restricciones claras**: Definir límites, formato de salida esperado y criterios de éxito.

## Mejora continua

- Registrar las optimizaciones realizadas y la retroalimentación recibida.
- Incorporar nuevas técnicas de prompt engineering conforme evolucionen.
- Adaptar las estrategias de traducción según los resultados obtenidos por dominio.