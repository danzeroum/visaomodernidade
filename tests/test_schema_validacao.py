"""Testes de validação de schemas.

Garantem que os 3 JSONs passam contra seus schemas Draft-07.
"""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from visaomodernidade import config


class TestSchemaValidacao:
    """Valida que os 3 JSONs passam contra seus schemas."""

    @pytest.fixture(scope="class")
    def schemas(self):
        return {
            "corpus": json.loads(config.CORPUS_SCHEMA_PATH.read_text(encoding="utf-8")),
            "contextual": json.loads(config.CONTEXTUAL_SCHEMA_PATH.read_text(encoding="utf-8")),
            "proveniencia": json.loads(config.PROVENIENCIA_SCHEMA_PATH.read_text(encoding="utf-8")),
        }

    def test_corpus_valido_contra_schema(self, schemas):
        corpus = json.loads(config.CORPUS_PATH.read_text(encoding="utf-8"))
        jsonschema.validate(corpus, schemas["corpus"])

    def test_grafo_contextual_valido_contra_schema(self, schemas):
        ctx = json.loads(config.GRAFO_CONTEXTUAL_PATH.read_text(encoding="utf-8"))
        jsonschema.validate(ctx, schemas["contextual"])

    def test_grafo_proveniencia_valido_contra_schema(self, schemas):
        prov = json.loads(config.GRAFO_PROVENIENCIA_PATH.read_text(encoding="utf-8"))
        jsonschema.validate(prov, schemas["proveniencia"])

    def test_schemas_sao_json_valido(self):
        for path in [
            config.CORPUS_SCHEMA_PATH,
            config.CONTEXTUAL_SCHEMA_PATH,
            config.PROVENIENCIA_SCHEMA_PATH,
        ]:
            assert path.exists(), f"Schema não encontrado: {path}"
            json.loads(path.read_text(encoding="utf-8"))

    def test_schema_proveniencia_tem_nova_aresta(self, schemas):
        """Ajuste 2: TEM_VERSAO_FRANCESA_NA_REVUE deve estar no vocabulário controlado."""
        # Lê o grafo de proveniência para acessar o vocabulário controlado declarado
        prov = json.loads(config.GRAFO_PROVENIENCIA_PATH.read_text(encoding="utf-8"))
        assert "TEM_VERSAO_FRANCESA_NA_REVUE" in prov["vocabulario_controlado"]["tipos_aresta"]
        # E no enum do schema
        edge_enum = schemas["proveniencia"]["definitions"]["arestaProv"]["properties"]["tipo"]["enum"]
        assert "TEM_VERSAO_FRANCESA_NA_REVUE" in edge_enum
