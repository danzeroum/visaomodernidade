"""Testes do relatório de validação.

Garantem que o validador semântico produziu resultado 'aprovado'
e que os critérios de aceite da Parte H do prompt original são satisfeitos.
"""
from __future__ import annotations

import pytest


class TestRelatorioValidacao:
    """Valida o resultado do validador semântico."""

    def test_resultado_aprovado(self, relatorio_validacao):
        assert relatorio_validacao["resultado"] == "aprovado", (
            f"Validação reprovada: {relatorio_validacao['resultado']}"
        )

    def test_sem_erros_alta_gravidade(self, relatorio_validacao):
        erros_alta = [e for e in relatorio_validacao["erros"] if e["gravidade"] == "alta"]
        assert not erros_alta, (
            f"Encontrados {len(erros_alta)} erros de alta gravidade: "
            f"{[e['codigo'] for e in erros_alta]}"
        )

    def test_sem_arestas_orfas(self, relatorio_validacao):
        assert relatorio_validacao["estatisticas"]["arestas_orfas"] == 0

    def test_sem_evidencias_ausentes(self, relatorio_validacao):
        assert relatorio_validacao["estatisticas"]["evidencias_ausentes"] == 0

    def test_sem_placeholders(self, relatorio_validacao):
        assert relatorio_validacao["estatisticas"]["placeholders_encontrados"] == 0

    def test_corpus_tem_dez_textos(self, relatorio_validacao):
        assert relatorio_validacao["estatisticas"]["textos_corpus"] == 10

    def test_arquivos_validados_presentes(self, relatorio_validacao):
        """Os 6 arquivos validados devem estar listados (3 dados + 3 schemas)."""
        arquivos = relatorio_validacao["arquivos_validados"]
        assert len(arquivos) == 6
        assert "corpus_britanico_canonico.json" in arquivos
        assert "grafo_contextual_v2.json" in arquivos
        assert "grafo_proveniencia_textual_v3.json" in arquivos
        # Schemas foram movidos para data/schemas/ com nomes padronizados
        assert "schemas/corpus.schema.json" in arquivos
        assert "schemas/contextual.schema.json" in arquivos
        assert "schemas/proveniencia.schema.json" in arquivos


class TestCriteriosAceiteParteH:
    """Critérios de aceite da Parte H do prompt original."""

    def test_jsons_sintaticamente_validos(self):
        """Todos os JSONs em data/ são sintaticamente válidos."""
        import json
        from visaomodernidade import config
        for path in [
            config.CORPUS_PATH,
            config.GRAFO_CONTEXTUAL_PATH,
            config.GRAFO_PROVENIENCIA_PATH,
            config.CORPUS_SCHEMA_PATH,
            config.CONTEXTUAL_SCHEMA_PATH,
            config.PROVENIENCIA_SCHEMA_PATH,
            config.RELATORIO_VALIDACAO_PATH,
        ]:
            json.loads(path.read_text(encoding="utf-8"))

    def test_ambos_grafos_passam_nos_schemas(self):
        """Ambos os grafos passam nos schemas correspondentes."""
        import json
        import jsonschema
        from visaomodernidade import config
        pairs = [
            (config.CORPUS_PATH, config.CORPUS_SCHEMA_PATH),
            (config.GRAFO_CONTEXTUAL_PATH, config.CONTEXTUAL_SCHEMA_PATH),
            (config.GRAFO_PROVENIENCIA_PATH, config.PROVENIENCIA_SCHEMA_PATH),
        ]
        for data_path, schema_path in pairs:
            data = json.loads(data_path.read_text(encoding="utf-8"))
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            jsonschema.validate(data, schema)
