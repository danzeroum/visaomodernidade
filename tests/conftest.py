"""conftest.py — fixtures compartilhadas entre os testes.

Carrega os JSONs uma única vez por sessão de testes.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Adiciona src/ ao sys.path para permitir `from visaomodernidade import config`
REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from visaomodernidade import config  # noqa: E402


@pytest.fixture(scope="session")
def project_root() -> Path:
    return config.PROJECT_ROOT


@pytest.fixture(scope="session")
def corpus() -> dict:
    """Carrega corpus_britanico_canonico.json uma vez por sessão."""
    with open(config.CORPUS_PATH, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def grafo_contextual() -> dict:
    with open(config.GRAFO_CONTEXTUAL_PATH, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def grafo_proveniencia() -> dict:
    with open(config.GRAFO_PROVENIENCIA_PATH, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def relatorio_validacao() -> dict:
    with open(config.RELATORIO_VALIDACAO_PATH, encoding="utf-8") as f:
        return json.load(f)
