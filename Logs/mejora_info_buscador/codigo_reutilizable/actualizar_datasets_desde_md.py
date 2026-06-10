#!/usr/bin/env python3
from __future__ import annotations

from datetime import date
from pathlib import Path
import csv
import re

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
INFO_DIR = ROOT / 'Informacion'
DATA_DIR = INFO_DIR / 'datasets'

TEAM_NAME_TO_CODE = {
    'Estados Unidos': 'USA',
    'Paraguay': 'PAR',
    'Turquía': 'TUR',
    'Australia': 'AUS',
    'Bélgica': 'BEL',
    'Belgica': 'BEL',
    'Portugal': 'POR',
    'Senegal': 'SEN',
    'Suiza': 'SUI',
    'Switzerland': 'SUI',
    'México': 'MEX',
    'Mexico': 'MEX',
    'Grecia': 'GRE',
    'Greece': 'GRE',
    'Marruecos': 'MAR',
    'Morocco': 'MAR',
    'Nicaragua': 'NCA',
    'Camerún': 'CMR',
    'Cameroon': 'CMR',
    'Curacao': 'CUW',
    'Curaçao': 'CUW',
    'Brasil': 'BRA',
    'Brazil': 'BRA',
    'Uruguay': 'URU',
    'España': 'ESP',
    'Spain': 'ESP',
    'Rumania': 'ROU',
    'Romania': 'ROU',
    'Kosovo': 'KOS',
    'Macedonia del Norte': 'MKD',
    'North Macedonia': 'MKD',
    'Venezuela': 'VEN',
    'Alemania': 'GER',
    'Germany': 'GER',
    'Bélgica': 'BEL',
    'Bélgca': 'BEL',
    'Marruecos': 'MAR',
    'Croacia': 'CRO',
    'Croatia': 'CRO',
    'Marruecos': 'MAR',
    'Italia': 'ITA',
    'Italy': 'ITA',
    'Inglaterra': 'ENG',
    'England': 'ENG',
    'Francia': 'FRA',
    'France': 'FRA',
    'Argelia': 'ALG',
    'Algeria': 'ALG',
    'Bosnia and Herzegovina': 'BIH',
    'Bosnia y Herzegovina': 'BIH',
    'Cote d\'Ivoire': 'CIV',
    'Côte d\'Ivoire': 'CIV',
    'Cote d’Ivoire': 'CIV',
    'Cabo Verde': 'CPV',
    'Cape Verde': 'CPV',
    'Canada': 'CAN',
    'Colombia': 'COL',
    'Congo DR': 'COD',
    'Czechia': 'CZE',
    'Ecuador': 'ECU',
    'Egypt': 'EGY',
    'Ghana': 'GHA',
    'Haiti': 'HAI',
    'IR Iran': 'IRN',
    'Iraq': 'IRQ',
    'Austria': 'AUT',
    'Argentina': 'ARG',
    'Albania': 'ALB',
    'Chile': 'CHI',
    'Chile': 'CHI',
    'Saudi Arabia': 'KSA',
    'Saudi Arabia': 'KSA',
    'Qatar': 'QAT',
    'Japan': 'JPN',
    'South Korea': 'KOR',
    'Korea Republic': 'KOR',
    'New Zealand': 'NZL',
    'Mali': 'MLI',
    'Nigeria': 'NGA',
    'Senegal': 'SEN',
    'Peru': 'PER',
    'Uruguay': 'URU',
    'Poland': 'POL',
    'Romania': 'ROU',
    'Serbia': 'SRB',
    'Sweden': 'SWE',
    'Norway': 'NOR',
    'Denmark': 'DEN',
    'Belgium': 'BEL',
    'Greece': 'GRE',
    'Morocco': 'MAR',
    'United States': 'USA',
}


def normalize_text(value: str) -> str:
    return re.sub(r'\s+', ' ', value.strip())


def code_from_name(value: str) -> str:
    value = normalize_text(value)
    if value in TEAM_NAME_TO_CODE:
        return TEAM_NAME_TO_CODE[value]
    return value[:3].upper()


def extract_code(text: str, fallback_name: str) -> str | None:
    first = text.splitlines()[0].strip() if text.splitlines() else ''
    m = re.match(r'^#\s+.*?—\s*([A-Z]{3})\s*$', first)
    if m:
        return m.group(1)
    m = re.match(r'^#\s+.*?[-—]\s*([A-Z]{3})\s*$', first)
    if m:
        return m.group(1)
    return TEAM_NAME_TO_CODE.get(fallback_name)


def parse_md_table(block: str) -> list[dict[str, str]]:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    table_lines = [line for line in lines if line.startswith('|')]
    if len(table_lines) < 2:
        return []
    headers = [cell.strip() for cell in table_lines[0].strip('|').split('|')]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def section_text(text: str, header_pattern: str) -> str:
    pattern = re.compile(rf'^{header_pattern}\s*\n(.*?)(?=^##\s+|\Z)', re.M | re.S)
    m = pattern.search(text)
    return m.group(1).strip() if m else ''


def parse_profile_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    profile = section_text(text, r'##\s+Perfil')
    for line in profile.splitlines():
        clean = line.strip()
        m = re.match(r'^-\s+(?:\*\*)?(.+?)(?:\*\*)?:\s*(.+)$', clean)
        if m:
            key = normalize_text(m.group(1)).lower()
            key = key.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
            fields[key] = m.group(2).strip()
    return fields


def parse_stats_fields(text: str) -> dict[str, str]:
    stats = section_text(text, r'##\s+Estadísticas.*?')
    values: dict[str, str] = {}
    for row in parse_md_table(stats):
        metric = normalize_text(next(iter(row.values()), ''))
        if metric:
            values[metric] = normalize_text(list(row.values())[1]) if len(row) > 1 else ''
    return values


def parse_player_rows(text: str) -> list[dict[str, str]]:
    block = section_text(text, r'##\s+Jugadores clave')
    return parse_md_table(block)


def parse_recent_matches(text: str) -> list[dict[str, str]]:
    match = re.search(r'^##\s+Forma reciente.*?\n(.*?)(?=^##\s+|\Z)', text, re.M | re.S)
    block = match.group(1).strip() if match else ''
    return parse_md_table(block)


def to_int(value: str) -> int | None:
    value = normalize_text(str(value))
    if not value or value in {'-', '—'}:
        return None
    m = re.search(r'(-?\d+)', value)
    return int(m.group(1)) if m else None


def to_float(value: str) -> float | None:
    value = normalize_text(str(value)).replace('%', '')
    if not value or value in {'-', '—'}:
        return None
    m = re.search(r'(-?\d+(?:\.\d+)?)', value)
    return float(m.group(1)) if m else None


def parse_result(code: str, cell: str) -> tuple[str | None, int | None, int | None]:
    cell = normalize_text(cell)
    m = re.match(r'^([WDL])\s+(\d+)-(\d+)', cell)
    if not m:
        return None, None, None
    letter, g1, g2 = m.group(1), int(m.group(2)), int(m.group(3))
    if letter == 'W':
        return '1', g1, g2
    if letter == 'D':
        return 'X', g1, g2
    return '2', g1, g2


def main() -> None:
    teams_path = DATA_DIR / 'equipos.csv'
    players_path = DATA_DIR / 'jugadores.csv'
    matches_path = DATA_DIR / 'partidos_historicos.csv'

    equipos = pd.read_csv(teams_path)
    jugadores = pd.read_csv(players_path)
    partidos = pd.read_csv(matches_path)

    existing_codes = set(equipos['codigo_fifa'].astype(str).str.upper())
    md_files = sorted(INFO_DIR.glob('*.md'))

    team_updates = 0
    player_updates = 0
    player_inserts = 0
    match_inserts = 0

    for md_path in md_files:
        text = md_path.read_text(encoding='utf-8', errors='ignore')
        title = text.splitlines()[0].strip() if text.splitlines() else ''
        name_match = re.match(r'^#\s+(.+?)(?:\s+[—-]\s+[A-Z]{3})?\s*$', title)
        name = name_match.group(1).strip() if name_match else md_path.stem.replace('_', ' ')
        code = extract_code(text, name)
        if not code:
            continue
        code = code.upper()

        profile = parse_profile_fields(text)
        stats = parse_stats_fields(text)

        mask = equipos['codigo_fifa'].astype(str).str.upper() == code
        if mask.any():
            idx = equipos.index[mask][0]
            row = equipos.loc[idx]

            mapping = {
                'grupo': profile.get('grupo'),
                'ranking_fifa': profile.get('ranking fifa') or profile.get('ranking') or profile.get('ranking fifa:'),
                'confederacion': profile.get('confederacion') or profile.get('confederación'),
                'dt': profile.get('dt'),
                'esquema_tactico': profile.get('esquema tactico') or profile.get('esquema táctico'),
                'estilo_juego': profile.get('estilo de juego') or profile.get('estilo juego') or profile.get('estilo'),
            }
            if mapping['grupo']:
                equipos.at[idx, 'grupo'] = mapping['grupo']
            if mapping['ranking_fifa']:
                equipos.at[idx, 'ranking_fifa'] = to_int(mapping['ranking_fifa']) or equipos.at[idx, 'ranking_fifa']
            if mapping['confederacion']:
                equipos.at[idx, 'confederacion'] = mapping['confederacion'].replace('Confederación', '').strip()
            if mapping['dt']:
                equipos.at[idx, 'dt'] = mapping['dt']
            if mapping['esquema_tactico']:
                equipos.at[idx, 'esquema_tactico'] = mapping['esquema_tactico']
            if mapping['estilo_juego']:
                style = mapping['estilo_juego'].split('—')[0].split('-')[0].strip().lower().replace(' ', '_')
                equipos.at[idx, 'estilo_juego'] = style

            # Populate recent stats when available
            for metric, column in [
                ('goles a favor', 'goles_favor'),
                ('goles en contra', 'goles_contra'),
                ('xg', 'xg'),
                ('xga', 'xga'),
                ('ppda promedio', 'ppda'),
                ('posesión promedio', 'posesion_prom'),
                ('posesion promedio', 'posesion_prom'),
                ('pases progresivos', 'pases_progresivos'),
                ('efectividad set pieces', 'efectividad_set_pieces'),
                ('partidos jugados', 'partidos_jugados'),
                ('victorias', 'victorias'),
                ('empates', 'empates'),
                ('derrotas', 'derrotas'),
            ]:
                for key, value in stats.items():
                    if metric in key.lower() and value and value != '-':
                        if column in {'ppda', 'posesion_prom', 'pases_progresivos', 'efectividad_set_pieces', 'puntos_forma', 'xg', 'xga'}:
                            num = to_float(value)
                            if num is not None:
                                equipos.at[idx, column] = num
                        else:
                            num = to_int(value)
                            if num is not None:
                                equipos.at[idx, column] = num
                        break

            if 'puntos forma' in stats:
                num = to_float(stats['puntos forma'])
                if num is not None:
                    equipos.at[idx, 'puntos_forma'] = num

            if 'confianza_dato' in equipos.columns and pd.isna(equipos.at[idx, 'confianza_dato']):
                equipos.at[idx, 'confianza_dato'] = 'Alta'

            team_updates += 1

        # Players upsert
        player_rows = parse_player_rows(text)
        for prow in player_rows:
            player_name = normalize_text(prow.get('Jugador', '') or prow.get('Jugador ') or '')
            if not player_name:
                continue
            pos = normalize_text(prow.get('Posición', '') or prow.get('Posicion', '') or '')
            club = normalize_text(prow.get('Club', '') or '')
            caps = to_int(prow.get('Caps', '') or '')
            goals = to_int(prow.get('Goles', '') or '')
            assists = to_int(prow.get('Asistencias', '') or '')
            status = normalize_text(prow.get('Estado físico', '') or prow.get('Estado fisico', '') or '')
            notes = normalize_text(prow.get('Notas', '') or '')

            mask_player = (jugadores['equipo'].astype(str).str.upper() == code) & (jugadores['jugador'].astype(str).str.lower() == player_name.lower())
            if mask_player.any():
                idxp = jugadores.index[mask_player][0]
                if pos:
                    jugadores.at[idxp, 'posicion'] = pos.split('/')[0].strip()
                if club:
                    jugadores.at[idxp, 'club'] = club
                if goals is not None:
                    jugadores.at[idxp, 'goles'] = goals
                if assists is not None:
                    jugadores.at[idxp, 'asistencias'] = assists
                if status:
                    jugadores.at[idxp, 'estado_fisico'] = status.lower().replace(' ', '_')
                if notes:
                    jugadores.at[idxp, 'notas'] = notes if notes else jugadores.at[idxp, 'notas']
                if caps is not None and 'caps' not in jugadores.columns:
                    pass
                if pd.isna(jugadores.at[idxp, 'titular_probable']):
                    jugadores.at[idxp, 'titular_probable'] = True
                player_updates += 1
            else:
                new_row = {col: '' for col in jugadores.columns}
                new_row['equipo'] = code
                new_row['jugador'] = player_name
                new_row['posicion'] = pos.split('/')[0].strip() if pos else ''
                new_row['club'] = club
                if goals is not None:
                    new_row['goles'] = goals
                if assists is not None:
                    new_row['asistencias'] = assists
                new_row['estado_fisico'] = status.lower().replace(' ', '_') if status else ''
                new_row['titular_probable'] = True
                new_row['notas'] = notes
                new_row['fecha_actualizacion'] = date.today().isoformat()
                jugadores = pd.concat([jugadores, pd.DataFrame([new_row])], ignore_index=True)
                player_inserts += 1

        # Historical matches from recent form tables
        recent_rows = parse_recent_matches(text)
        for r in recent_rows:
            fecha = normalize_text(r.get('Fecha', '') or r.get('fecha', '') or '')
            rival = normalize_text(r.get('Rival', '') or r.get('rival', '') or '')
            resultado = normalize_text(r.get('Resultado', '') or r.get('resultado', '') or '')
            competicion = normalize_text(r.get('Competición', '') or r.get('Competicion', '') or '')
            notas = normalize_text(r.get('Notas', '') or '')
            if not fecha or not rival or not resultado:
                continue
            rival_code = code_from_name(rival)
            out_res, g1, g2 = parse_result(code, resultado)
            if out_res is None:
                continue
            # If no explicit score is embedded, leave blank values.
            g1 = g1 if g1 is not None else ''
            g2 = g2 if g2 is not None else ''

            exists = (
                (partidos['fecha'].astype(str) == fecha)
                & (partidos['equipo_1'].astype(str).str.upper() == code)
                & (partidos['equipo_2'].astype(str).str.upper() == rival_code)
            )
            if exists.any():
                continue
            new_match = {col: '' for col in partidos.columns}
            new_match['fecha'] = fecha
            new_match['equipo_1'] = code
            new_match['equipo_2'] = rival_code
            new_match['goles_1'] = g1
            new_match['goles_2'] = g2
            new_match['resultado'] = out_res
            new_match['competicion'] = competicion
            new_match['fase'] = ''
            new_match['ranking_1'] = equipos.loc[mask, 'ranking_fifa'].iloc[0] if mask.any() else ''
            new_match['ranking_2'] = ''
            new_match['sede'] = ''
            new_match['neutral'] = 'True' if competicion.lower().find('amistoso') >= 0 else ''
            if 'fecha_actualizacion' in new_match:
                new_match['fecha_actualizacion'] = date.today().isoformat()
            if notas:
                # keep a trace in the competition field when useful and empty
                if not new_match['competicion']:
                    new_match['competicion'] = notas
            partidos = pd.concat([partidos, pd.DataFrame([new_match])], ignore_index=True)
            match_inserts += 1

    # Clean up dtypes and save
    equipos.to_csv(teams_path, index=False, quoting=csv.QUOTE_MINIMAL)
    jugadores.to_csv(players_path, index=False, quoting=csv.QUOTE_MINIMAL)
    partidos.to_csv(matches_path, index=False, quoting=csv.QUOTE_MINIMAL)

    print(f'team_updates={team_updates}')
    print(f'player_updates={player_updates}')
    print(f'player_inserts={player_inserts}')
    print(f'match_inserts={match_inserts}')
    print(f'teams_rows={len(equipos)} players_rows={len(jugadores)} matches_rows={len(partidos)}')


if __name__ == '__main__':
    main()