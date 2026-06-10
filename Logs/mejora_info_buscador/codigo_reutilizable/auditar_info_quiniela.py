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

FILES = [
    'equipos.csv',
    'jugadores.csv',
    'partidos_historicos.csv',
    'h2h.csv',
    'contexto_partidos.csv',
]


def pct(n: int, d: int) -> float:
    return 0.0 if d == 0 else (100.0 * n / d)


def load_data() -> dict[str, pd.DataFrame]:
    data: dict[str, pd.DataFrame] = {}
    for fname in FILES:
        data[fname] = pd.read_csv(DATA_DIR / fname)
    return data


def md_quality() -> dict[str, int]:
    files = sorted(INFO_DIR.glob('*.md'))
    with_noticias = 0
    with_jugadores = 0
    with_perfil = 0
    for p in files:
        txt = p.read_text(encoding='utf-8', errors='ignore')
        has_noticias = bool(re.search(r'^##\s+Noticias', txt, flags=re.M | re.I))
        has_jugadores = bool(re.search(r'^##\s+Jugadores', txt, flags=re.M | re.I))
        has_perfil = bool(re.search(r'^##\s+Perfil', txt, flags=re.M | re.I))
        with_noticias += int(has_noticias)
        with_jugadores += int(has_jugadores)
        with_perfil += int(has_perfil)
    return {
        'total': len(files),
        'with_noticias': with_noticias,
        'with_jugadores': with_jugadores,
        'with_perfil': with_perfil,
    }


def main() -> None:
    data = load_data()
    e = data['equipos.csv']
    j = data['jugadores.csv']
    p = data['partidos_historicos.csv']
    h = data['h2h.csv']
    c = data['contexto_partidos.csv']

    codes = set(e['codigo_fifa'].dropna().astype(str).str.upper())

    # Coverage
    teams_hist = set(p['equipo_1'].dropna().astype(str).str.upper()) | set(p['equipo_2'].dropna().astype(str).str.upper())
    teams_no_hist = sorted(codes - teams_hist)

    out_catalog = sorted((set(p['equipo_1'].dropna().astype(str).str.upper()) | set(p['equipo_2'].dropna().astype(str).str.upper())) - codes)

    # Null highlights
    eq_critical = ['xg', 'xga', 'ppda', 'pases_progresivos', 'efectividad_set_pieces', 'goles_favor', 'goles_contra', 'posesion_prom', 'ranking_fifa']
    pl_critical = ['club', 'goles', 'asistencias', 'minutos_jugados', 'xg_jugador']

    mdq = md_quality()

    # Critical criteria
    critical_issues = []
    if len(p) < 200:
        critical_issues.append(f'partidos_historicos muy bajo: {len(p)} filas (<200)')
    if len(h) < 20:
        critical_issues.append(f'h2h muy bajo: {len(h)} filas (<20)')
    if len(c) < 6:
        critical_issues.append(f'contexto_partidos muy bajo: {len(c)} filas (<6)')

    for col in eq_critical:
        if col in e.columns:
            n = int(e[col].isna().sum())
            if pct(n, len(e)) > 80:
                critical_issues.append(f'equipos.{col} nulo {pct(n, len(e)):.1f}%')

    for col in pl_critical:
        if col in j.columns:
            n = int(j[col].isna().sum())
            if pct(n, len(j)) > 80:
                critical_issues.append(f'jugadores.{col} nulo {pct(n, len(j)):.1f}%')

    if len(teams_no_hist) > 20:
        critical_issues.append(f'equipos sin historial en partidos_historicos: {len(teams_no_hist)}')

    if mdq['with_noticias'] < int(0.5 * mdq['total']):
        critical_issues.append(f'fichas con Noticias insuficientes: {mdq["with_noticias"]}/{mdq["total"]}')
    if mdq['with_jugadores'] < int(0.5 * mdq['total']):
        critical_issues.append(f'fichas con Jugadores insuficientes: {mdq["with_jugadores"]}/{mdq["total"]}')

    status = 'NO APTO - persisten problemas criticos' if critical_issues else 'APTO - sin problemas criticos detectados'

    out_md = OUT_DIR / f'auditoria_estado_info_{date.today().isoformat()}.md'
    lines = []
    lines.append('# Auditoria de estado de informacion para quiniela')
    lines.append('')
    lines.append(f'Fecha: {date.today().isoformat()}')
    lines.append(f'Estado: {status}')
    lines.append('')
    lines.append('## Volumen actual')
    for fname in FILES:
        df = data[fname]
        lines.append(f'- {fname}: {len(df)} filas, {len(df.columns)} columnas')
    lines.append('')
    lines.append('## Cobertura y consistencia')
    lines.append(f'- Equipos en catalogo: {len(codes)}')
    lines.append(f'- Equipos sin partidos historicos: {len(teams_no_hist)}')
    if teams_no_hist:
        lines.append(f"- Muestra equipos sin historico: {', '.join(teams_no_hist[:15])}")
    lines.append(f'- Codigos fuera de catalogo en partidos_historicos: {len(out_catalog)}')
    if out_catalog:
        lines.append(f"- Lista: {', '.join(out_catalog)}")
    lines.append('')
    lines.append('## Calidad de fichas md')
    lines.append(f"- Fichas totales: {mdq['total']}")
    lines.append(f"- Con seccion Perfil: {mdq['with_perfil']}")
    lines.append(f"- Con seccion Jugadores: {mdq['with_jugadores']}")
    lines.append(f"- Con seccion Noticias: {mdq['with_noticias']}")
    lines.append('')
    lines.append('## Problemas criticos detectados')
    if not critical_issues:
        lines.append('- Ninguno')
    else:
        for issue in critical_issues:
            lines.append(f'- {issue}')

    out_md.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(status)
    print(out_md)


if __name__ == '__main__':
    main()
