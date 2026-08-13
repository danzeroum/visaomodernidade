#!/usr/bin/env python3
"""build_all.py — Ponto de entrada único para regenerar todo o pacote.

Executa em sequência:
    1. build_schemas.py        — gera os 3 JSON Schemas
    2. build_corpus_canonico.py — gera corpus_britanico_canonico.json
    3. build_grafo_contextual.py — gera grafo_contextual_v2.json
    4. build_grafo_proveniencia.py — gera grafo_proveniencia_textual_v3.json

Os scripts antigos em scripts/ são mantidos para granularidade;
este wrapper é o comando recomendado para CI e desenvolvimento.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
STEPS = [
    ("build_schemas.py", "schemas"),
    ("build_corpus_canonico.py", "corpus"),
    ("build_grafo_proveniencia.py", "grafo_proveniencia"),
    ("build_grafo_contextual.py", "grafo_contextual"),
]


def main() -> int:
    print("=" * 60)
    print("visaomodernidade — build completo")
    print("=" * 60)
    for script, label in STEPS:
        script_path = SCRIPTS_DIR / script
        if not script_path.exists():
            print(f"✗ Script não encontrado: {script_path}", file=sys.stderr)
            return 2
        print(f"\n→ [{label}] {script}")
        result = subprocess.run([sys.executable, str(script_path)], cwd=SCRIPTS_DIR.parent)
        if result.returncode != 0:
            print(f"✗ FALHA em {script} (código {result.returncode})", file=sys.stderr)
            return result.returncode
    print("\n" + "=" * 60)
    print("✓ Build completo")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
