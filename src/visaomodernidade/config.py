"""Configuração central: caminhos, constantes e vocabulário controlado.

Centraliza todos os caminhos do projeto para que scripts e testes possam
importar de um único lugar. Não há lógica aqui — apenas declarações.
"""
from __future__ import annotations

from pathlib import Path

# ---------- Caminhos do projeto ----------
# Resolve a raiz do repositório subindo três níveis a partir deste arquivo:
# src/visaomodernidade/config.py -> repo raiz
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
SCHEMAS_DIR = DATA_DIR / "schemas"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
TESTS_DIR = PROJECT_ROOT / "tests"
DOCS_DIR = PROJECT_ROOT / "docs"
SITE_DIR = PROJECT_ROOT / "site"

# Arquivos de dados
CORPUS_PATH = DATA_DIR / "corpus_britanico_canonico.json"
GRAFO_CONTEXTUAL_PATH = DATA_DIR / "grafo_contextual_v2.json"
GRAFO_PROVENIENCIA_PATH = DATA_DIR / "grafo_proveniencia_textual_v3.json"
RELATORIO_VALIDACAO_PATH = DATA_DIR / "relatorio_validacao.json"

# Schemas
CORPUS_SCHEMA_PATH = SCHEMAS_DIR / "corpus.schema.json"
CONTEXTUAL_SCHEMA_PATH = SCHEMAS_DIR / "contextual.schema.json"
PROVENIENCIA_SCHEMA_PATH = SCHEMAS_DIR / "proveniencia.schema.json"

# Documentação
RELATORIO_DIVERGENCIAS_PATH = DOCS_DIR / "relatorio_divergencias.md"

# ---------- Fonte primária ----------
TESE_BASE = {
    "obra": "Soares, Maria Angélica Lau Pereira. Visão da Modernidade: A Presença Britânica no Gabinete de Leitura (1837-1838). 209f. Dissertação (Mestrado em Estudos Lingüísticos e Literários em Inglês) — Universidade de São Paulo, São Paulo, 2006.",
    "autora": "Maria Angélica Lau Pereira Soares",
    "ano": 2006,
    "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf",
    "orientadora": "Sandra Guardini Teixeira Vasconcelos",
}

# ---------- Paginação ----------
# IMPORTANTE: não há offset universal garantido para toda a dissertação.
# O offset 8 foi verificado APENAS para o corpo do Capítulo 6 (PDF p.84 = impressa p.76).
# Consumidores nunca devem derivar uma paginação a partir da outra em tempo de execução.
PAGINACAO_MAPEAMENTO_VERIFICADO = [
    {
        "secao": "Capítulo 6 (A nação britânica no Gabinete de Leitura)",
        "pagina_impressa_inicio": 76,
        "pagina_pdf_inicio": 84,
        "offset": 8,
        "metodo_verificacao": "Marcador 'Capítulo 6' encontrado no PDF p.84 = impressa p.76 (confirmado via pdftotext -layout).",
    }
]

# ---------- Vocabulário controlado ----------
STATUS_EPISTEMOLOGICO = [
    "documentado",
    "identificado",
    "inferido",
    "hipotese",
    "problematico",
    "nao_identificado",
]

TIPOS_NO_CONTEXTUAL = [
    "Tese", "Capitulo", "Secao", "Periodico", "Fasciculo", "Instituicao",
    "Tipografia", "Livraria", "Pessoa", "ObraAbstrata", "ManifestacaoTextual",
    "Conceito", "Tema", "MovimentoLiterario", "Local", "ReferenciaBibliografica",
    "Evidencia", "Argumento",
]

TIPOS_ARESTA_CONTEXTUAL = [
    "AUTORA_DE", "ORIENTA", "ANALISA", "PUBLICADA_EM", "IMPRESSA_EM", "VENDIDA_EM",
    "REDIGE", "COLABORA_COM", "CONTRIBUI_PARA", "REPUBLICADA_EM", "RELACIONA_SE_A",
    "CITA", "SUSTENTA", "ASSOCIA_SE_A", "CONTEXTO_DE", "INTEGRA", "INFLUENCIA", "TEM_TEMA",
]

TIPOS_NO_PROVENIENCIA = [
    "Tese", "Periodico", "Giftbook", "Fasciculo", "PublicacaoSerializada",
    "ObraAbstrata", "ManifestacaoTextual", "Pessoa", "FonteDeclarada",
    "Trecho", "OperacaoTradutoria", "Evidencia", "Argumento", "Local",
]

TIPOS_ARESTA_PROVENIENCIA = [
    "AUTOR_DE", "MANIFESTA", "PUBLICADA_EM", "PERTENCE_A", "SERIALIZADA_EM",
    "PARTE_EM", "DECLARA_COMO_FONTE", "PUBLICADA_ORIGINALMENTE_EM",
    "RELACAO_DE_DEPENDENCIA_TEXTUAL", "INTERMEDIADA_POR",
    "TEM_VERSAO_FRANCESA_NA_REVUE",
    "NAO_E_FONTE_DIRETA_DE",
    "COMPARA_COM", "TEM_TRECHO", "AFETA", "SUSTENTA", "ANALISA",
]

# ---------- Padrões de ID (regex) ----------
# Permite múltiplos dois-pontos depois do prefixo (ex.: manifestation:en:new-monthly:cockney:1837-06)
ID_PATTERN_NODE = r"^[a-z]+:[a-z0-9:-]+$"
ID_PATTERN_EDGE = r"^edge:[a-z0-9-]+$"
ID_PATTERN_EVIDENCE = r"^evidence:[a-z0-9:-]+$"
ID_PATTERN_OP = r"^op:[a-z0-9:-]+$"
ID_PATTERN_WORK = r"^work:[a-z0-9-]+$"
ID_PATTERN_MANIFESTATION = r"^manifestation:[a-z0-9:-]+$"
ID_PATTERN_ARGUMENT = r"^argument:[a-z0-9:-]+$"
ID_PATTERN_CORPUS = r"^corpus:[a-z0-9-]+$"

# ---------- Corpus: 10 textos esperados ----------
# (corpus_id, work_id, fascículos_esperados, data_esperada)
CORPUS_ESPERADO = [
    ("corpus:costumes-ingleses", "work:a-cockney-country-gentleman", [30], "1838-03-04"),
    ("corpus:uma-noite-no-mar", "work:uma-noite-no-mar", [2], "1837-08-20"),
    ("corpus:testamento", "work:o-testamento", [9], "1837-10-08"),
    ("corpus:livro-da-vida", "work:o-livro-da-vida", [6], "1837-09-17"),
    ("corpus:sedutor", "work:o-sedutor-irving", [10], "1837-10-15"),
    ("corpus:manuscrito-casa-loucos", "work:manuscrito-casa-loucos", [8], "1837-10-01"),
    ("corpus:honras-hereditarias", "work:hereditary-honours", [11], "1837-10-22"),
    ("corpus:terencio-alfaiate", "work:terence-oflaherty", [14], "1837-11-12"),
    ("corpus:alibi", "work:alibi-grattan", [12], "1837-10-29"),
    ("corpus:esbocos-sicilianos", "work:esbocos-sicilianos", [31, 32, 33, 34], "1838-03-11"),
]

# Três exceções explícitas da tese à mediação da Revue Britannique
EXCECOES_REVUE_BRITANNIQUE = {
    "corpus:testamento",
    "corpus:honras-hereditarias",
    "corpus:costumes-ingleses",
}

# Sete textos não-excepcionais (tiveram versão francesa por inferência por exclusão)
TEXTO_COM_VERSAO_FRANCESA_INFERIDA = {
    "corpus:uma-noite-no-mar",
    "corpus:livro-da-vida",
    "corpus:sedutor",
    "corpus:manuscrito-casa-loucos",
    "corpus:terencio-alfaiate",
    "corpus:alibi",
    "corpus:esbocos-sicilianos",
}

# ---------- Versão do pacote ----------
VERSAO_CORPUS = "1.1.0"
VERSAO_GRAFO_CONTEXTUAL = "2.0"
VERSAO_GRAFO_PROVENIENCIA = "3.1"
DATA_GERACAO = "2026-08-14"
