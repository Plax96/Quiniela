#!/usr/bin/env python3
from __future__ import annotations

from datetime import date
from pathlib import Path
import re

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / 'Informacion' / 'datasets'
INFO_DIR = ROOT / 'Informacion'
OUT_DIR = ROOT / 'Logs' / 'mejora_info_buscador'


def md_map_by_code() -> dict[str, dict[str, int | str]]:
    out: dict[str, dict[str, int | str]] = {}
    for p in sorted(INFO_DIR.glob('*.md')):
        txt = p.read_text(encoding='utf-8', errors='ignore')
        first = txt.splitlines()[0] if txt.splitlines() else ''
        m = re.search(r'[-\u2014]\s*([A-Z]{3})\s*$', first)
        if not m:
            continue
        code = m.group(1)
        sections = re.findall(r'^##\s+(.+)$', txt, flags=re.M)
        out[code] = {
            'md_file': p.name,
            'md_sections_count': len(sections),
            'md_has_perfil': int(any(s.lower().startswith('perfil') for s in sections)),
            'md_has_jugadores': int(any(s.lower().startswith('jugadores') for s in sections)),
            'md_has_noticias': int(any(s.lower().startswith('noticias') for s in sections)),
        }
    return out


def main() -> None:
    e = pd.read_csv(DATA_DIR / 'equipos.csv')
    j = pd.read_csv(DATA_DIR / 'jugadores.csv')
    p = pd.read_csv(DATA_DIR / 'partidos_historicos.csv')
    md_meta = md_map_by_code()

    team_fields = [
        'ranking_fifa', 'dt', 'esquema_tactico', 'estilo_juego', 'goles_favor', 'goles_contra',
        'xg', 'xga', 'ppda', 'posesion_prom', 'pases_progresivos', 'efectividad_set_pieces',
    ]
    player_fields = ['club', 'goles', 'asistencias', 'minutos_jugados', 'xg_jugador']

    rows = []
    for _, t in e.iterrows():
        code = str(t['codigo_fifa']).upper()
        name = str(t['equipo'])
        group = str(t['grupo'])

        miss_team = [c for c in team_fields if pd.isna(t.get(c, None))]
        psub = j[j['equipo'].astype(str).str.upper() == code].copy()
        players_count = len(psub)
        gap_top8 = max(0, 8 - players_count)
        missing_player_cells = int(psub[player_fields].isna().sum().sum()) if players_count else 8 * len(player_fields)
        norm_player_missing = (missing_player_cells / max(1, players_count * len(player_fields))) if players_count else 1.0

        hist_count = int(((p['equipo_1'].astype(str).str.upper() == code) | (p['equipo_2'].astype(str).str.upper() == code)).sum())

        meta = md_meta.get(code, {
            'md_file': '',
            'md_sections_count': 0,
            'md_has_perfil': 0,
            'md_has_jugadores': 0,
            'md_has_noticias': 0,
        })

        miss_adv = len([c for c in ['xg', 'xga', 'ppda', 'pases_progresivos', 'efectividad_set_pieces'] if c in miss_team])
        score = (
            4 * miss_adv
            + 2 * gap_top8
            + int(10 * norm_player_missing)
            + (10 if hist_count == 0 else (6 if hist_count < 3 else (3 if hist_count < 6 else 0)))
            + (3 if meta['md_has_noticias'] == 0 else 0)
            + (2 if meta['md_has_jugadores'] == 0 else 0)
        )

        if score >= 30:
            priority = 'Critica'
        elif score >= 22:
            priority = 'Alta'
        elif score >= 15:
            priority = 'Media'
        else:
            priority = 'Baja'

        items = []
        if miss_team:
            items.append('team:' + ','.join(miss_team))
        if gap_top8 > 0:
            items.append(f'jugadores_faltan_slots_top8:{gap_top8}')
        if missing_player_cells > 0:
            items.append(f'jugadores_celdas_nulas:{missing_player_cells}')
        if hist_count == 0:
            items.append('historial_partidos:0')
        if meta['md_has_jugadores'] == 0:
            items.append('md_sin_jugadores')
        if meta['md_has_noticias'] == 0:
            items.append('md_sin_noticias')

        rows.append({
            'codigo_fifa': code,
            'equipo': name,
            'grupo': group,
            'prioridad': priority,
            'priority_score': score,
            'missing_team_fields_count': len(miss_team),
            'players_count': players_count,
            'slot_gap_to_top8': gap_top8,
            'missing_player_cells': missing_player_cells,
            'hist_matches_count': hist_count,
            'md_file': meta['md_file'],
            'md_sections_count': meta['md_sections_count'],
            'md_has_jugadores': meta['md_has_jugadores'],
            'md_has_noticias': meta['md_has_noticias'],
            'missing_items': ' | '.join(items),
        })

    report = pd.DataFrame(rows).sort_values(['priority_score', 'equipo'], ascending=[False, True])

    csv_path = OUT_DIR / f'checklist_automatico_por_equipo_{date.today().isoformat()}.csv'
    md_path = OUT_DIR / f'checklist_automatico_por_equipo_{date.today().isoformat()}.md'
    report.to_csv(csv_path, index=False)

    lines = []
    lines.append('# Checklist automatico por equipo')
    lines.append('')
    lines.append(f'Fecha: {date.today().isoformat()}')
    lines.append('')
    lines.append('## Resumen')
    lines.append(f"- Critica: {int((report['prioridad']=='Critica').sum())}")
    lines.append(f"- Alta: {int((report['prioridad']=='Alta').sum())}")
    lines.append(f"- Media: {int((report['prioridad']=='Media').sum())}")
    lines.append(f"- Baja: {int((report['prioridad']=='Baja').sum())}")
    lines.append('')
    lines.append('## Top 20')
    lines.append('')
    lines.append('| # | FIFA | Equipo | Prioridad | Score | Hist | Jug | Noticias |')
    lines.append('|---|---|---|---|---:|---:|---:|---:|')
    for i, (_, r) in enumerate(report.head(20).iterrows(), start=1):
        lines.append(f"| {i} | {r['codigo_fifa']} | {r['equipo']} | {r['prioridad']} | {int(r['priority_score'])} | {int(r['hist_matches_count'])} | {int(r['md_has_jugadores'])} | {int(r['md_has_noticias'])} |")

    lines.append('')
    lines.append('## Detalle')
    lines.append('')
    for _, r in report.iterrows():
        lines.append(f"### {r['equipo']} ({r['codigo_fifa']})")
        lines.append(f"- Prioridad: {r['prioridad']} (score {int(r['priority_score'])})")
        lines.append(f"- Faltantes: {r['missing_items']}")
        lines.append('')

    md_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(csv_path)
    print(md_path)


if __name__ == '__main__':
    main()
