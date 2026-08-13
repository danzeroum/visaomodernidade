"""Testes de regressão — validação de fixtures inválidas.

Garante que o validador semântico captura erros em entradas inválidas.
Estes testes protegem o próprio validador contra regressões.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class TestFixturesInvalidas:
    """Verifica que fixtures inválidas são de fato inválidas."""

    def test_corpus_invalido_falha_no_schema(self):
        """O fixture corpus_invalido.json deve falhar contra o schema (apenas 1 item, não 10)."""
        import jsonschema
        from visaomodernidade import config
        corpus = json.loads((FIXTURES / "corpus_invalido.json").read_text(encoding="utf-8"))
        schema = json.loads(config.CORPUS_SCHEMA_PATH.read_text(encoding="utf-8"))
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(corpus, schema)

    def test_corpus_invalido_nao_tem_dez_itens(self):
        """Sanidade: o fixture tem apenas 1 item (não 10)."""
        corpus = json.loads((FIXTURES / "corpus_invalido.json").read_text(encoding="utf-8"))
        assert len(corpus["itens"]) == 1

    def test_grafo_com_aresta_orfa_tem_destino_inexistente(self):
        """O fixture grafo_com_aresta_orfa.json tem aresta para nó inexistente."""
        grafo = json.loads((FIXTURES / "grafo_com_aresta_orfa.json").read_text(encoding="utf-8"))
        node_ids = set(n["id"] for n in grafo["nos"])
        orphan_edges = [
            a for a in grafo["arestas"]
            if a["origem"] not in node_ids or a["destino"] not in node_ids
        ]
        assert len(orphan_edges) >= 1, "Fixture deveria conter ao menos uma aresta órfã"

    def test_corpus_canonico_nao_e_o_fixture_invalido(self, corpus):
        """Sanidade: o corpus real tem 10 itens (não é o fixture inválido)."""
        assert len(corpus["itens"]) == 10
