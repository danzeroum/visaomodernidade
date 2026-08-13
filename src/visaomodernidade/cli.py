"""CLI entry points para visaomodernidade.

Fornece dois comandos:
    build    — regenera schemas, corpus e grafos (chama scripts/build_all.py)
    validate — roda validador semântico (chama scripts/validate.py)

Estes entry points são declarados em pyproject.toml:
    visaomodernidade-build     -> visaomodernidade.cli:build
    visaomodernidade-validate  -> visaomodernidade.cli:validate
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from . import config


def _run_script(script_name: str) -> int:
    """Executa um script Python do diretório scripts/ como subprocess.

    Retorna o código de saída.
    """
    script_path = config.SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"ERRO: script não encontrado: {script_path}", file=sys.stderr)
        return 2
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=config.PROJECT_ROOT,
    )
    return result.returncode


def build() -> int:
    """Regenera schemas, corpus e grafos."""
    print("→ Construindo schemas, corpus e grafos...")
    rc = _run_script("build_all.py")
    if rc == 0:
        print("✓ Build concluído")
    else:
        print(f"✗ Build falhou (código {rc})", file=sys.stderr)
    return rc


def validate() -> int:
    """Roda validador semântico e escreve data/relatorio_validacao.json."""
    print("→ Validando dados...")
    rc = _run_script("validate.py")
    if rc == 0:
        print("✓ Validação concluída")
        # Lê o relatório e mostra o resultado
        try:
            import json
            with open(config.RELATORIO_VALIDACAO_PATH) as f:
                r = json.load(f)
            print(f"  Resultado: {r['resultado']}")
            print(f"  Erros: {len(r['erros'])} ({sum(1 for e in r['erros'] if e['gravidade']=='alta')} alta)")
            print(f"  Avisos: {len(r['avisos'])}")
        except Exception as e:
            print(f"  (não foi possível ler relatório: {e})", file=sys.stderr)
    else:
        print(f"✗ Validação falhou (código {rc})", file=sys.stderr)
    return rc


def main() -> int:
    """Entry point genérico: aceita subcomando."""
    if len(sys.argv) < 2:
        print("Uso: python -m visaomodernidade.cli [build|validate]", file=sys.stderr)
        return 2
    cmd = sys.argv[1]
    if cmd == "build":
        return build()
    if cmd == "validate":
        return validate()
    print(f"Comando desconhecido: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
