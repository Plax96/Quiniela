# Bitácora Arquitecto — 2026-06-06

## Objetivo
Validar novedades recientes de GitHub Copilot y aplicar mejoras concretas a skills y agentes del repositorio.

## Fuentes consultadas
- https://github.blog/changelog/label/copilot/
- https://docs.github.com/en/copilot/customizing-copilot
- https://docs.github.com/en/copilot/about-github-copilot/github-copilot-features
- https://code.visualstudio.com/updates
- https://github.blog/tag/github-copilot/

## Novedades detectadas de mayor impacto
- `/chronicle` para insights y búsqueda de sesiones.
- Ventanas de contexto ampliadas (hasta 1M tokens en modelos compatibles).
- Reasoning levels configurables.
- Copilot SDK en estado GA.
- Agent Tasks REST API disponible en planes aplicables.
- Copilot Memory con soporte de preferencias.
- Deprecaciones recientes: GPT-4.1, GPT-5.2 y variantes; mantener migración fuera de líneas retiradas.

## Cambios aplicados
1. Actualizado `.github/arquitecto/validacion/copilot_changelog.md` a 2026-06-06.
2. Actualizado `.github/agents/arquitecto.md` con modelos/deprecaciones/capacidades nuevas.
3. Actualizado `.github/agents/buscador.md` con uso de `/chronicle`, contexto amplio y Research Agent (preview).
4. Actualizado `.github/agents/ml.md` con estrategia de contexto amplio y recuperación histórica vía `/chronicle`.
5. Actualizado `.github/agents/analitico.md` con contexto amplio, `/chronicle` y corrección de hito duplicado.
6. Actualizado `.github/agents/agent-template.md` y `.github/agents/README.md` con prácticas Copilot 2026.
7. Actualizadas skills:
   - `.github/skills/skill-creator/SKILL.md`
   - `.github/skills/doc-coauthoring/SKILL.md`
   - `.github/skills/web-research/SKILL.md`
   - `.github/skills/sports-data-deep/SKILL.md`
8. Actualizado `.github/skills/README.md` con inventario real y convenciones.
9. Registrada auditoría en `.github/arquitecto/validacion/audit_log.md`.

## Estado final
- Resultado: aplicado.
- Riesgos abiertos: hooks automatizados aún pendientes; falta definir política de costo para contexto 1M.
