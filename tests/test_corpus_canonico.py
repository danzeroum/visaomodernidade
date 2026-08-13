"""Testes de regressão do corpus canônico.

Garantem que as 12 correções de fascículo/data da v3.0 e os 4 ajustes
da v3.1 não regrediram.
"""
from __future__ import annotations

import pytest

from visaomodernidade import config


class TestCorpusCanonico:
    """Valida estrutura e conteúdo do corpus_britanico_canonico.json."""

    def test_corpus_tem_exatamente_dez_textos(self, corpus):
        assert len(corpus["itens"]) == 10, (
            f"Corpus deve ter exatamente 10 itens; encontrado {len(corpus['itens'])}."
        )

    def test_corpus_id_pattern(self, corpus):
        """Todos os IDs seguem o padrão corpus:slug."""
        import re
        pat = re.compile(config.ID_PATTERN_CORPUS)
        for item in corpus["itens"]:
            assert pat.match(item["id"]), f"ID fora do padrão: {item['id']}"

    def test_corpus_ids_unicos(self, corpus):
        ids = [i["id"] for i in corpus["itens"]]
        assert len(ids) == len(set(ids)), f"IDs duplicados: {set([i for i in ids if ids.count(i) > 1])}"

    @pytest.mark.parametrize("corpus_id, _work_id, expected_fasc, expected_data", config.CORPUS_ESPERADO)
    def test_fasciculo_e_data_canonicos(self, corpus, corpus_id, _work_id, expected_fasc, expected_data):
        """Verifica fascículos e datas corrigidas na v3.0."""
        item = next((i for i in corpus["itens"] if i["id"] == corpus_id), None)
        assert item is not None, f"Item não encontrado: {corpus_id}"
        actual_fasc = [f["numero"] for f in item["fasciculos"]]
        assert actual_fasc == expected_fasc, (
            f"{corpus_id}: fascículos esperados {expected_fasc}, encontrados {actual_fasc}"
        )
        assert item["fasciculos"][0]["data_iso"] == expected_data, (
            f"{corpus_id}: data esperada {expected_data}, encontrada {item['fasciculos'][0]['data_iso']}"
        )

    def test_esbocos_sicilianos_serializado_em_quatro_partes(self, corpus):
        """Esboços Sicilianos deve ter 4 fascículos (n.31-34), não um único evento."""
        item = next(i for i in corpus["itens"] if i["id"] == "corpus:esbocos-sicilianos")
        assert len(item["fasciculos"]) == 4, f"Esperado 4 fascículos, encontrado {len(item['fasciculos'])}"
        fasciculos = [f["numero"] for f in item["fasciculos"]]
        assert fasciculos == [31, 32, 33, 34], f"Fascículos esperados [31,32,33,34], encontrados {fasciculos}"
        # Papeis: publicacao, continua, continua, conclusao
        papeis = [f["papel"] for f in item["fasciculos"]]
        assert papeis == ["publicacao", "continua", "continua", "conclusao"], (
            f"Papeis esperados [publicacao,continua,continua,conclusao], encontrados {papeis}"
        )

    def test_costumes_ingleses_nao_e_fasciculo_4(self, corpus):
        """Protege contra regressão: Costumes Ingleses era n.4 na v2.2; corrigido para n.30 na v3.0."""
        item = next(i for i in corpus["itens"] if i["id"] == "corpus:costumes-ingleses")
        fasc = item["fasciculos"][0]["numero"]
        assert fasc == 30, f"Costumes Ingleses deve ser n.30 (regressão da v2.2); encontrado n.{fasc}"
        assert fasc != 4, "Regressão: Costumes Ingleses voltou para n.4"

    def test_alibi_e_fasciculo_12(self, corpus):
        """Álibi corrigido na v3.0: era n.13, agora n.12."""
        item = next(i for i in corpus["itens"] if i["id"] == "corpus:alibi")
        assert item["fasciculos"][0]["numero"] == 12

    def test_terencio_e_fasciculo_14(self, corpus):
        """Terêncio corrigido na v3.0: era n.21, agora n.14."""
        item = next(i for i in corpus["itens"] if i["id"] == "corpus:terencio-alfaiate")
        assert item["fasciculos"][0]["numero"] == 14

    def test_testamento_e_problematico(self, corpus):
        """O Testamento tem original não localizado e fonte problemática."""
        item = next(i for i in corpus["itens"] if i["id"] == "corpus:testamento")
        assert item["original_identificado"] is False
        assert item["fonte_declarada_no_gabinete"]["status_epistemologico"] == "problematico"
        assert item["fonte_original_identificada"]["status_epistemologico"] == "nao_identificado"

    def test_livro_da_vida_e_problematico(self, corpus):
        """O Livro da Vida tem original não localizado e fonte Retrospective Review problemática."""
        item = next(i for i in corpus["itens"] if i["id"] == "corpus:livro-da-vida")
        assert item["original_identificado"] is False
        assert item["fonte_declarada_no_gabinete"]["status_epistemologico"] == "problematico"

    def test_sedutor_nao_tem_original_inventado(self, corpus):
        """O Sedutor não deve ter título_original inventado."""
        item = next(i for i in corpus["itens"] if i["id"] == "corpus:sedutor")
        assert item["titulo_original"] is None, "O Sedutor não deve ter título_original inventado"
        assert item["fonte_original_identificada"]["veiculo"] is None
        assert item["fonte_original_identificada"]["status_epistemologico"] == "nao_identificado"
        assert item["original_identificado"] is False


class TestAjustesV31:
    """Valida os 4 ajustes aplicados na revisão v3.0 → v3.1."""

    def test_ajuste1_offset_nao_universal(self, corpus):
        """Ajuste 1: removida regra global de offset; substituída por mapeamento_verificado."""
        pag = corpus["metadados"]["paginacao"]
        assert "regra_global" in pag
        assert "Não há offset universal" in pag["regra_global"]
        assert "mapeamento_verificado" in pag
        assert len(pag["mapeamento_verificado"]) >= 1
        # Capítulo 6 deve estar mapeado com offset 8
        cap6 = next((m for m in pag["mapeamento_verificado"] if "Capítulo 6" in m["secao"]), None)
        assert cap6 is not None, "Capítulo 6 deve estar no mapeamento_verificado"
        assert cap6["offset"] == 8
        # Não deve haver campo offset_paginacao antigo
        assert "offset_paginacao" not in corpus["metadados"], (
            "Campo obsoleto 'offset_paginacao' ainda presente; deve ser removido."
        )

    def test_ajuste2_mediacoes_francesas_inferidas(self, corpus):
        """Ajuste 2: 7 mediações não-excepcionais rebaixadas para 'inferido' com metodo."""
        for item in corpus["itens"]:
            if item["id"] in config.TEXTO_COM_VERSAO_FRANCESA_INFERIDA:
                mf = item["mediacao_francesa"]
                assert mf["status"] == "inferido", (
                    f"{item['id']}: mediacao_francesa.status deve ser 'inferido', é '{mf['status']}'"
                )
                assert mf.get("metodo") == "inferencia_por_exclusao", (
                    f"{item['id']}: metodo deve ser 'inferencia_por_exclusao'"
                )

    def test_ajuste2_excecoes_mantem_documentado(self, corpus):
        """Ajuste 2: as 3 exceções explícitas da tese mantêm 'documentado'."""
        for item in corpus["itens"]:
            if item["id"] in config.EXCECOES_REVUE_BRITANNIQUE:
                mf = item["mediacao_francesa"]
                assert mf["status"] == "documentado", (
                    f"{item['id']}: exceção deve manter 'documentado', é '{mf['status']}'"
                )

    def test_ajuste3_costumes_rota_nao_identificada(self, corpus):
        """Ajuste 3: rota_tradutoria de Costumes Ingleses = nao_identificado (não problematico)."""
        item = next(i for i in corpus["itens"] if i["id"] == "corpus:costumes-ingleses")
        rt = item["rota_tradutoria"]
        assert rt["status"] == "nao_identificado", (
            f"Costumes: rota_tradutoria.status deve ser 'nao_identificado', é '{rt['status']}'"
        )
        # A descrição deve mencionar que o problemático é a fonte declarada, não a rota
        assert "fonte declarada" in rt["descricao"].lower(), (
            "Descrição da rota deve esclarecer que o problemático é a fonte declarada"
        )

    def test_ajuste4_anatomy_drunkness_divergencia_preservada(self, corpus):
        """Ajuste 4: divergência interna da tese sobre The Anatomy of Drunkness preservada."""
        # Busca em observacoes e atributos
        str_corpus = __import__("json").dumps(corpus, ensure_ascii=False)
        assert "divergência interna" in str_corpus.lower(), (
            "A divergência interna sobre Anatomy of Drunkness deve estar preservada"
        )


class TestSemPlaceholders:
    """Garante que não há placeholders no corpus."""

    @pytest.mark.parametrize("pattern,label", [
        (r"\?\?", "placeholder ??"),
        (r"texto-0[0-9]", "placeholder texto-0X"),
        (r"\bpendente\b", "palavra 'pendente'"),
        (r"\bcerca de\b", "palavras 'cerca de'"),
        (r"\bTBD\b", "placeholder TBD"),
        (r"\bTODO\b", "placeholder TODO"),
        (r"c18\d0", "placeholder c18X0 (circa)"),
        (r"c183[0-9]", "placeholder c183X (circa)"),
    ])
    def test_sem_placeholders_no_corpus(self, corpus, pattern, label):
        import re
        # Verifica apenas em strings, não em números/booleans/null
        import json
        text = json.dumps(corpus, ensure_ascii=False)
        # Para 'cerca de' e 'pendente' precisamos ser case-insensitive
        flags = re.IGNORECASE if label.startswith("palavra") else 0
        matches = re.findall(pattern, text, flags)
        # Permite a palavra "circa" em descrições, mas não "c1830" como data
        assert not matches or all(m == "circa" for m in matches), (
            f"Encontrado {label}: {matches[:3]}"
        )
