#!/usr/bin/env python3
"""Enriquece datasets del Mundial 2026 usando endpoints de resumen de ESPN.

Este script prioriza campos alcanzables y consistentes:
- equipos.csv: goles, resultados, posesion promedio, forma
- jugadores.csv: goles/asistencias/tarjetas y altas de roster por equipo

No inventa xG/xGA/PPDA cuando la fuente no los publica de forma estable.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[3]
DATASETS_DIR = ROOT / "Informacion" / "datasets"
EQUIPOS_CSV = DATASETS_DIR / "equipos.csv"
JUGADORES_CSV = DATASETS_DIR / "jugadores.csv"

BASE = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.friendly"
SCOREBOARD_URL = f"{BASE}/scoreboard"
SUMMARY_URL = f"{BASE}/summary?event={{event_id}}"

USER_AGENT = "Mozilla/5.0 (compatible; QuinielaBot/1.0)"


def _fetch_json(url: str) -> dict:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def _safe_float(value: str) -> Optional[float]:
    if value is None:
        return None
    value = str(value).strip().replace("%", "")
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _safe_int(value: str) -> Optional[int]:
    if value is None:
        return None
    value = str(value).strip()
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def _norm_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def _read_csv(path: Path) -> Tuple[List[dict], List[str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        return rows, reader.fieldnames or []


def _write_csv(path: Path, rows: List[dict], fieldnames: List[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _event_completed(event: dict) -> bool:
    try:
        comp = event.get("competitions", [{}])[0]
        status = comp.get("status", {}).get("type", {})
        return bool(status.get("completed"))
    except Exception:
        return False


def _extract_competitors(event: dict) -> List[dict]:
    comp = event.get("competitions", [{}])[0]
    return comp.get("competitors", [])


def _collect_relevant_events(scoreboard: dict, team_ids: set[str]) -> List[str]:
    event_ids: List[str] = []
    for event in scoreboard.get("events", []):
        if not _event_completed(event):
            continue
        competitors = _extract_competitors(event)
        ids = {str(c.get("team", {}).get("id", "")) for c in competitors}
        if ids & team_ids:
            eid = str(event.get("id", "")).strip()
            if eid:
                event_ids.append(eid)
    return event_ids


def _team_stat_map(summary: dict) -> Dict[str, dict]:
    out: Dict[str, dict] = {}
    for team_block in summary.get("boxscore", {}).get("teams", []):
        tid = str(team_block.get("team", {}).get("id", "")).strip()
        if not tid:
            continue
        stat_values = {}
        for stat in team_block.get("statistics", []):
            stat_values[stat.get("name", "")] = stat.get("displayValue")
        out[tid] = stat_values
    return out


def _iter_player_rows(summary: dict) -> Iterable[Tuple[str, dict, List[dict]]]:
    for team_roster in summary.get("boxscore", {}).get("rosters", []):
        team = team_roster.get("team", {})
        tid = str(team.get("id", "")).strip()
        for player in team_roster.get("roster", []):
            athlete = player.get("athlete", {})
            stats = player.get("stats", [])
            yield tid, athlete, stats


def _aggregate_players_from_details(summary: dict, espn_id_to_code: Dict[str, str], player_aggr: dict) -> None:
    details = summary.get("header", {}).get("details", [])
    for d in details:
        team_id = str(d.get("team", {}).get("id", "")).strip()
        code = espn_id_to_code.get(team_id)
        if not code:
            continue

        etype = (d.get("type", {}).get("text") or "").lower()
        participants = d.get("participants", []) or []
        if not participants:
            continue

        p1 = participants[0].get("athlete", {})
        name1 = (p1.get("displayName") or "").strip()
        if not name1:
            continue
        key1 = (code, _norm_text(name1))

        # Goles y asistencias: en ESPN details suelen venir en scoringPlay con 1-2 participantes.
        if d.get("scoringPlay"):
            player_aggr[key1]["g"] += 1
            player_aggr[key1]["app"] += 1
            if len(participants) > 1:
                p2 = participants[1].get("athlete", {})
                name2 = (p2.get("displayName") or "").strip()
                if name2:
                    key2 = (code, _norm_text(name2))
                    player_aggr[key2]["a"] += 1
                    player_aggr[key2]["app"] += 1

        # Tarjetas por tipo de evento.
        if "yellow" in etype:
            player_aggr[key1]["yc"] += 1
            player_aggr[key1]["app"] += 1
        elif "red" in etype:
            player_aggr[key1]["rc"] += 1
            player_aggr[key1]["app"] += 1


def _expand_event_ids(initial_ids: List[str], limit: int = 180) -> List[str]:
    """Expande gameIds explorando boxscore.form en cada summary."""
    seen = set(initial_ids)
    queue = list(initial_ids)

    while queue and len(seen) < limit:
        event_id = queue.pop(0)
        try:
            summary = _fetch_json(SUMMARY_URL.format(event_id=event_id))
        except (HTTPError, URLError, TimeoutError):
            continue

        forms = summary.get("boxscore", {}).get("form", [])
        for team_form in forms:
            for ev in team_form.get("events", []):
                new_id = str(ev.get("id", "")).strip()
                if not new_id or new_id in seen:
                    continue
                seen.add(new_id)
                queue.append(new_id)
                if len(seen) >= limit:
                    break
            if len(seen) >= limit:
                break

    return list(seen)


def _pos_from_abbr(raw: str) -> str:
    raw = (raw or "").upper()
    if raw in {"G", "GK", "POR"}:
        return "POR"
    if raw.startswith("D") or raw in {"RB", "LB", "CB", "DEF"}:
        return "DEF"
    if raw.startswith("M") or raw in {"DM", "CM", "AM", "LM", "RM", "MED"}:
        return "MED"
    if raw.startswith("F") or raw in {"FW", "ST", "DEL"}:
        return "DEL"
    return "MED"


def main() -> int:
    equipos_rows, equipos_fields = _read_csv(EQUIPOS_CSV)
    jugadores_rows, jugadores_fields = _read_csv(JUGADORES_CSV)

    # Mapa codigo_fifa -> fila equipos y nombre canonico.
    code_to_team: Dict[str, dict] = {}
    name_to_code: Dict[str, str] = {}
    for row in equipos_rows:
        code = (row.get("codigo_fifa") or "").strip().upper()
        name = (row.get("equipo") or "").strip()
        if not code or not name:
            continue
        code_to_team[code] = row
        name_to_code[_norm_text(name)] = code

    # Vincula ESPN team id -> codigo FIFA a partir de scoreboard (competitors).
    try:
        scoreboard = _fetch_json(SCOREBOARD_URL)
    except (HTTPError, URLError, TimeoutError) as exc:
        print(f"ERROR: no se pudo leer scoreboard ESPN: {exc}")
        return 1

    espn_id_to_code: Dict[str, str] = {}
    for event in scoreboard.get("events", []):
        for comp in _extract_competitors(event):
            team = comp.get("team", {})
            tid = str(team.get("id", "")).strip()
            abbr = (team.get("abbreviation") or "").strip().upper()
            display = (team.get("displayName") or "").strip()
            if not tid:
                continue
            if abbr in code_to_team:
                espn_id_to_code[tid] = abbr
                continue
            nkey = _norm_text(display)
            if nkey in name_to_code:
                espn_id_to_code[tid] = name_to_code[nkey]

    tracked_team_ids = set(espn_id_to_code.keys())
    event_ids = _collect_relevant_events(scoreboard, tracked_team_ids)
    event_ids = list(dict.fromkeys(event_ids))
    event_ids = _expand_event_ids(event_ids, limit=100)

    if not event_ids:
        print("WARN: no se encontraron eventos cerrados para equipos del dataset.")
        return 0

    team_match_stats = defaultdict(list)
    team_results = defaultdict(list)
    player_aggr = defaultdict(lambda: {"g": 0, "a": 0, "yc": 0, "rc": 0, "app": 0})

    for idx, event_id in enumerate(event_ids, start=1):
        try:
            summary = _fetch_json(SUMMARY_URL.format(event_id=event_id))
        except (HTTPError, URLError, TimeoutError):
            continue

        comp = summary.get("header", {}).get("competitions", [{}])[0]
        competitors = comp.get("competitors", [])
        if len(competitors) != 2:
            continue

        c1, c2 = competitors
        t1 = str(c1.get("team", {}).get("id", "")).strip()
        t2 = str(c2.get("team", {}).get("id", "")).strip()
        code1 = espn_id_to_code.get(t1)
        code2 = espn_id_to_code.get(t2)
        if not code1 and not code2:
            continue

        s1 = _safe_int(c1.get("score")) or 0
        s2 = _safe_int(c2.get("score")) or 0

        # Guarda resultado por equipo para forma y GF/GC.
        if code1:
            team_results[code1].append({"gf": s1, "gc": s2, "date": comp.get("date", "")})
        if code2:
            team_results[code2].append({"gf": s2, "gc": s1, "date": comp.get("date", "")})

        tstats = _team_stat_map(summary)
        if code1 and t1 in tstats:
            team_match_stats[code1].append(tstats[t1])
        if code2 and t2 in tstats:
            team_match_stats[code2].append(tstats[t2])

        # Estadisticas de jugador por partido.
        for tid, athlete, stats in _iter_player_rows(summary):
            code = espn_id_to_code.get(tid)
            if not code:
                continue
            aid = str(athlete.get("id", "")).strip()
            name = (athlete.get("fullName") or athlete.get("displayName") or "").strip()
            if not aid or not name:
                continue
            key = (code, _norm_text(name))
            by_name = {s.get("name"): _safe_int(s.get("value")) for s in stats}
            player_aggr[key]["g"] += by_name.get("totalGoals") or 0
            player_aggr[key]["a"] += by_name.get("goalAssists") or 0
            player_aggr[key]["yc"] += by_name.get("yellowCards") or 0
            player_aggr[key]["rc"] += by_name.get("redCards") or 0
            player_aggr[key]["app"] += by_name.get("appearances") or 0

        # Fallback robusto cuando rosters no trae stats completas.
        _aggregate_players_from_details(summary, espn_id_to_code, player_aggr)

        if idx % 25 == 0:
            print(f"Procesados {idx}/{len(event_ids)} eventos...")

    today = dt.date.today().isoformat()

    # Actualiza equipos.csv con campos alcanzables.
    for row in equipos_rows:
        code = (row.get("codigo_fifa") or "").strip().upper()
        results = team_results.get(code, [])
        if not results:
            continue
        results = sorted(results, key=lambda x: x.get("date", ""), reverse=True)
        sample = results[:15]
        last5 = results[:5]

        gf = sum(r["gf"] for r in sample)
        gc = sum(r["gc"] for r in sample)
        w = sum(1 for r in sample if r["gf"] > r["gc"])
        d = sum(1 for r in sample if r["gf"] == r["gc"])
        l = sum(1 for r in sample if r["gf"] < r["gc"])
        points_last5 = sum(3 if r["gf"] > r["gc"] else 1 if r["gf"] == r["gc"] else 0 for r in last5)

        row["goles_favor"] = str(gf)
        row["goles_contra"] = str(gc)
        row["partidos_jugados"] = str(len(sample))
        row["victorias"] = str(w)
        row["empates"] = str(d)
        row["derrotas"] = str(l)
        row["puntos_forma"] = f"{float(points_last5):.1f}"

        stats = team_match_stats.get(code, [])
        poss_vals = []
        for st in stats:
            v = _safe_float(st.get("possessionPct"))
            if v is not None:
                poss_vals.append(v)
        if poss_vals:
            row["posesion_prom"] = f"{sum(poss_vals) / len(poss_vals):.1f}"

        row["confianza_dato"] = "Alta"
        row["fecha_actualizacion"] = today

    # Index de jugadores existentes por (equipo, nombre normalizado).
    players_idx: Dict[Tuple[str, str], dict] = {}
    for row in jugadores_rows:
        code = (row.get("equipo") or "").strip().upper()
        name = _norm_text(row.get("jugador") or "")
        if code and name:
            players_idx[(code, name)] = row

    added_players = 0
    print(f"Player aggregates detectados: {len(player_aggr)}")
    for (code, nname), aggr in player_aggr.items():
        row = players_idx.get((code, nname))
        if row is None:
            # Alta minima: conserva esquema estricto del dataset.
            row = {k: "" for k in jugadores_fields}
            row["equipo"] = code
            row["jugador"] = nname.title()
            row["posicion"] = "MED"
            row["estado_fisico"] = "disponible"
            row["titular_probable"] = "False"
            row["tarjetas_amarillas"] = "0"
            row["tarjetas_rojas"] = "0"
            row["fecha_actualizacion"] = today
            jugadores_rows.append(row)
            players_idx[(code, nname)] = row
            added_players += 1

        # Goles: solo sobrescribe si estaba vacio o en cero.
        current_goals = _safe_float(row.get("goles") or "")
        if (current_goals is None or current_goals == 0.0) and aggr["g"] > 0:
            row["goles"] = str(float(aggr["g"]))

        # Asistencias: se llena cuando existe en ESPN.
        if aggr["a"] > 0:
            row["asistencias"] = str(float(aggr["a"]))

        # Tarjetas: mantiene el max entre valor actual y agregado.
        current_yc = _safe_float(row.get("tarjetas_amarillas") or "") or 0.0
        current_rc = _safe_float(row.get("tarjetas_rojas") or "") or 0.0
        if aggr["yc"] > current_yc:
            row["tarjetas_amarillas"] = str(float(aggr["yc"]))
        if aggr["rc"] > current_rc:
            row["tarjetas_rojas"] = str(float(aggr["rc"]))

        # Trazabilidad ligera en notas.
        notes = (row.get("notas") or "").strip()
        tag = f"EST-ESPN-SUMMARY: APP={aggr['app']}; G={aggr['g']}; A={aggr['a']}; YC={aggr['yc']}; RC={aggr['rc']}."
        if "EST-ESPN-SUMMARY:" not in notes:
            row["notas"] = (notes + " " + tag).strip()

        row["fecha_actualizacion"] = today

    _write_csv(EQUIPOS_CSV, equipos_rows, equipos_fields)
    _write_csv(JUGADORES_CSV, jugadores_rows, jugadores_fields)

    print(f"Eventos procesados: {len(event_ids)}")
    print(f"Equipos con resultados actualizados: {sum(1 for k in team_results if team_results[k])}")
    print(f"Jugadores agregados: {added_players}")
    print("OK: equipos.csv y jugadores.csv actualizados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
