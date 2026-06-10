#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python "$SCRIPT_DIR/auditar_info_quiniela.py"
python "$SCRIPT_DIR/generar_checklist_automatico.py"

echo "Revision completa terminada"
