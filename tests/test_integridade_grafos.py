"""Testes de integridade estrutural dos grafos.

Verificam que:
- IDs de nós/arestas/evidências/operações são únicos
- Toda origem/destino de aresta existe em nos
- Todo evidence_id referido existe em evidencias
- Obras serializadas têm todas as partes registradas
- Status epistemológico segue o vocabulário controlado
- Evidências têm paginação dupla (PDF e impressa) com offset correto quando ambas presentes
"""
from __future__ import annotations

import json
from collections import Counter

import pytest

from visaomodernidade import config


class TestIntegridadeGrafoContextual:
    """Integridade do grafo_contextual_v2.json."""

    def test_ids_nos_unicos(self, grafo_contextual):
        ids = [n["id"] for n in grafo_contextual["nos"]]
        dupes = [i for i, c in Counter(ids).items() if c > 1]
        assert not dupes, f"IDs de nós duplicados: {dupes}"

    def test_ids_arestas_unicos(self, grafo_contextual):
        ids = [a["id"] for a in grafo_contextual["arestas"]]
        dupes = [i for i, c in Counter(ids).items() if c > 1]
        assert not dupes, f"IDs de arestas duplicados: {dupes}"

    def test_toda_aresta_aponta_para_nos_existentes(self, grafo_contextual):
        node_ids = set(n["id"] for n in grafo_contextual["nos"])
        for a in grafo_contextual["arestas"]:
            assert a["origem"] in node_ids, (
                f"Aresta {a['id']}: origem não existe: {a['origem']}"
            )
            assert a["destino"] in node_ids, (
                f"Aresta {a['id']}: destino não existe: {a['destino']}"
            )

    def test_evidence_ids_referenciados_existem(self, grafo_contextual):
        ev_ids = set(e["id"] for e in grafo_contextual["evidencias"])
        for n in grafo_contextual["nos"]:
            for eid in n.get("evidence_ids", []):
                assert eid in ev_ids, f"Nó {n['id']} referencia evidência inexistente: {eid}"
        for a in grafo_contextual["arestas"]:
            for eid in a.get("evidence_ids", []):
                assert eid in ev_ids, f"Aresta {a['id']} referencia evidência inexistente: {eid}"

    def test_status_epistemologico_no_vocabulario(self, grafo_contextual):
        valid = set(config.STATUS_EPISTEMOLOGICO)
        for n in grafo_contextual["nos"]:
            assert n["status_epistemologico"] in valid, (
                f"Nó {n['id']}: status inválido {n['status_epistemologico']}"
            )


class TestIntegridadeGrafoProveniencia:
    """Integridade do grafo_proveniencia_textual_v3.json."""

    def test_ids_nos_unicos(self, grafo_proveniencia):
        ids = [n["id"] for n in grafo_proveniencia["nos"]]
        dupes = [i for i, c in Counter(ids).items() if c > 1]
        assert not dupes, f"IDs de nós duplicados: {dupes}"

    def test_ids_arestas_unicos(self, grafo_proveniencia):
        ids = [a["id"] for a in grafo_proveniencia["arestas"]]
        dupes = [i for i, c in Counter(ids).items() if c > 1]
        assert not dupes, f"IDs de arestas duplicados: {dupes}"

    def test_toda_aresta_aponta_para_nos_existentes(self, grafo_proveniencia):
        node_ids = set(n["id"] for n in grafo_proveniencia["nos"])
        orphan_count = 0
        for a in grafo_proveniencia["arestas"]:
            if a["origem"] not in node_ids:
                orphan_count += 1
            if a["destino"] not in node_ids:
                orphan_count += 1
        assert orphan_count == 0, f"{orphan_count} arestas órfãs encontradas"

    def test_evidence_ids_referenciados_existem(self, grafo_proveniencia):
        ev_ids = set(e["id"] for e in grafo_proveniencia["evidencias"])
        # Em nós
        for n in grafo_proveniencia["nos"]:
            for eid in n.get("evidence_ids", []):
                assert eid in ev_ids, f"Nó {n['id']} referencia evidência inexistente: {eid}"
        # Em arestas
        for a in grafo_proveniencia["arestas"]:
            for eid in a.get("evidence_ids", []):
                assert eid in ev_ids, f"Aresta {a['id']} referencia evidência inexistente: {eid}"
        # Em operações tradutórias
        for op in grafo_proveniencia.get("operacoes_tradutorias", []):
            for eid in op.get("evidence_ids", []):
                assert eid in ev_ids, f"Operação {op['id']} referencia evidência inexistente: {eid}"

    def test_operacoes_tem_duas_ou_mais_manifestacoes(self, grafo_proveniencia):
        for op in grafo_proveniencia.get("operacoes_tradutorias", []):
            assert len(op["manifestacoes_comparadas"]) >= 2, (
                f"Operação {op['id']} deve ter 2+ manifestações comparadas; tem {len(op['manifestacoes_comparadas'])}"
            )

    def test_esbocos_sicilianos_serializada_completa(self, grafo_proveniencia):
        """PublicacaoSerializada de Esboços Sicilianos deve ter 4 partes (PARTE_EM)."""
        serial_nodes = [n for n in grafo_proveniencia["nos"] if n["tipo"] == "PublicacaoSerializada"]
        assert len(serial_nodes) == 1
        serial = serial_nodes[0]
        assert "esbocos" in serial["id"].lower()

        partes = [a for a in grafo_proveniencia["arestas"]
                  if a["tipo"] == "PARTE_EM" and a["origem"] == serial["id"]]
        assert len(partes) == 4, f"Esperado 4 partes, encontrado {len(partes)}"

        # Verifica fascículos 31-34
        fasciculos_esperados = [31, 32, 33, 34]
        fasc_encontrados = []
        for p in partes:
            fasc_node = next((n for n in grafo_proveniencia["nos"] if n["id"] == p["destino"]), None)
            assert fasc_node is not None
            fasc_encontrados.append(fasc_node["atributos"]["numero"])
        assert sorted(fasc_encontrados) == fasciculos_esperados, (
            f"Fascículos esperados {fasciculos_esperados}, encontrados {sorted(fasc_encontrados)}"
        )

    def test_intermediada_por_nao_presente(self, grafo_proveniencia):
        """Ajuste 2: INTERMEDIADA_POR não deve estar presente nos 7 textos não-excepcionais.

        Apenas TEM_VERSAO_FRANCESA_NA_REVUE deve ser usado para os 7 textos não-excepcionais,
        e NAO_E_FONTE_DIRETA_DE para o caso de Costumes Ingleses (afirmação expressa da tese).
        """
        # INTERMEDIADA_POR pode existir em casos muito específicos, mas não para os 7 textos
        br_manifestations_7 = [
            "manifestation:pt-br:gabinete:uma-noite-no-mar:1837-08-20",
            "manifestation:pt-br:gabinete:livro-da-vida:1837-09-17",
            "manifestation:pt-br:gabinete:sedutor:1837-10-15",
            "manifestation:pt-br:gabinete:manuscrito-casa-loucos:1837-10-01",
            "manifestation:pt-br:gabinete:terencio-alfaiate:1837-11-12",
            "manifestation:pt-br:gabinete:alibi:1837-10-29",
            "manifestation:pt-br:gabinete:esbocos-sicilianos:1838-03-11-a-04-01",
        ]
        intermediada_for_7 = [
            a for a in grafo_proveniencia["arestas"]
            if a["tipo"] == "INTERMEDIADA_POR" and a["origem"] in br_manifestations_7
        ]
        assert not intermediada_for_7, (
            f"INTERMEDIADA_POR não deve ser usado para os 7 textos não-excepcionais: "
            f"{[a['id'] for a in intermediada_for_7]}"
        )

    def test_tem_versao_francesa_para_os_7_textos(self, grafo_proveniencia):
        """Ajuste 2: 7 arestas TEM_VERSAO_FRANCESA_NA_REVUE devem existir, com status 'inferido'."""
        edges_tvf = [a for a in grafo_proveniencia["arestas"] if a["tipo"] == "TEM_VERSAO_FRANCESA_NA_REVUE"]
        assert len(edges_tvf) == 7, f"Esperado 7 arestas TEM_VERSAO_FRANCESA_NA_REVUE; encontrado {len(edges_tvf)}"
        for e in edges_tvf:
            assert e["status_epistemologico"] == "inferido", (
                f"{e['id']}: status deve ser 'inferido', é '{e['status_epistemologico']}'"
            )
            assert e.get("justificativa"), f"{e['id']}: inferido deve ter justificativa"

    def test_nao_e_fonte_direta_para_costumes(self, grafo_proveniencia):
        """NAO_E_FONTE_DIRETA_DE deve existir para Le Cockney Campagnard -> Costumes Ingleses."""
        edges = [
            a for a in grafo_proveniencia["arestas"]
            if a["tipo"] == "NAO_E_FONTE_DIRETA_DE"
            and "le-cockney" in a["origem"]
            and "costumes" in a["destino"]
        ]
        assert len(edges) == 1, f"Esperado 1 aresta NAO_E_FONTE_DIRETA_DE para Costumes; encontrado {len(edges)}"
        assert edges[0]["status_epistemologico"] == "documentado"


class TestPaginacaoDupla:
    """Valida que evidências têm paginação dupla com offset correto quando ambas presentes."""

    def test_offset_correto_no_corpo_da_tese(self, grafo_contextual, grafo_proveniencia):
        """Quando ambas as paginações estão presentes, offset deve ser 8 (verificado Cap. 6)."""
        for ev in grafo_contextual["evidencias"] + grafo_proveniencia["evidencias"]:
            fonte = ev["fonte"]
            p_pdf_i = fonte.get("pagina_pdf_inicio")
            p_pdf_f = fonte.get("pagina_pdf_fim")
            p_imp_i = fonte.get("pagina_impressa_inicio")
            p_imp_f = fonte.get("pagina_impressa_fim")

            # Se ambas as paginações de início estiverem presentes, offset deve ser 8
            if p_pdf_i is not None and p_imp_i is not None:
                assert p_pdf_i - p_imp_i == 8, (
                    f"Evidência {ev['id']}: offset PDF-impressa (início) incorreto: "
                    f"PDF={p_pdf_i}, impressa={p_imp_i}, diff={p_pdf_i - p_imp_i} (esperado 8)"
                )
            # Mesmo para fim
            if p_pdf_f is not None and p_imp_f is not None:
                assert p_pdf_f - p_imp_f == 8, (
                    f"Evidência {ev['id']}: offset PDF-impressa (fim) incorreto: "
                    f"PDF={p_pdf_f}, impressa={p_imp_f}, diff={p_pdf_f - p_imp_f} (esperado 8)"
                )
            # PDF início <= PDF fim
            if p_pdf_i is not None and p_pdf_f is not None:
                assert p_pdf_i <= p_pdf_f, (
                    f"Evidência {ev['id']}: pagina_pdf_inicio ({p_pdf_i}) > pagina_pdf_fim ({p_pdf_f})"
                )

    def test_evidencias_tem_ao_menos_uma_paginacao(self, grafo_contextual, grafo_proveniencia):
        """Toda evidência deve ter ao menos uma página PDF ou impressa."""
        for ev in grafo_contextual["evidencias"] + grafo_proveniencia["evidencias"]:
            fonte = ev["fonte"]
            has_pdf = fonte.get("pagina_pdf_inicio") is not None or fonte.get("pagina_pdf_fim") is not None
            has_imp = fonte.get("pagina_impressa_inicio") is not None or fonte.get("pagina_impressa_fim") is not None
            assert has_pdf or has_imp, (
                f"Evidência {ev['id']} deve ter ao menos uma página PDF ou impressa"
            )
