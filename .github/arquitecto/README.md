# Arquitecto — Carpeta de Validación

Esta carpeta es el espacio de trabajo del **Agente Arquitecto**. Aquí mantiene su conocimiento actualizado sobre GitHub Copilot y el historial de todas las mejoras aplicadas al ecosistema del proyecto.

## Estructura

```
validacion/
├── copilot_changelog.md    ← Conocimiento actualizado de Copilot (refrescar cada 7 días)
├── audit_log.md            ← Historial de auditorías y cambios realizados
└── benchmarks/             ← Métricas de rendimiento por skill (se crea cuando se necesite)
```

## Uso

El Agente Arquitecto consulta esta carpeta **al inicio de cada sesión** para decidir si necesita actualizar su conocimiento antes de operar. Si `copilot_changelog.md` tiene más de 7 días de antigüedad, el agente lo actualiza antes de cualquier otra tarea.
