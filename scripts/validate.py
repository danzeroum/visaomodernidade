#!/usr/bin/env python3
"""validate.py — Ponto de entrada único para validar o pacote.

Executa:
    1. validador_semantico.py — produz data/relatorio_validacao.json

Saída: código de saída 0 se aprovado, 1 se reprovado.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPTS_DIR.parent
VALIDATOR = SCRIPTS_DIR / "validador_semantico.py"
RELATORIO = PROJECT_ROOT / "data" / "relatorio_validacao.json"


def main() -> int:
    print("=" * 60)
    print("visaomodernidade — validação semântica")
    print("=" * 60)
    if not VALIDATOR.exists():
        print(f"✗ Validador não encontrado: {VALIDATOR}", file=sys.stderr)
        return 2
    result = subprocess.run([sys.executable, str(VALIDATOR)], cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print(f"✗ Validador falhou (código {result.returncode})", file=sys.stderr)
        return result.returncode

    # Lê o relatório e decide exit code
    try:
        r = json.loads(RELATORIO.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"✗ Não foi possível ler {RELATORIO}: {e}", file=sys.stderr)
        return 2

    print("\n" + "=" * 60)
    print(f"Resultado: {r['resultado'].upper()}")
    print(f"Erros: {len(r['erros'])} ({sum(1 for e in r['erros'] if e['gravidade']=='alta')} alta)")
    print(f"Avisos: {len(r['avisos'])}")
    print("=" * 60)

    if r["resultado"] == "aprovado":
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
