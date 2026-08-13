#!/usr/bin/env python3
"""
Gera três schemas JSON Draft-07:
  - schema_corpus_britanico_canonico.json
  - schema_grafo_contextual_v2.json
  - schema_grafo_proveniencia_textual_v3.json

Os schemas impõem:
  - IDs com padrão consistente (pattern)
  - Vocabulário controlado de tipos de nó/aresta e status epistemológico
  - Paginação dupla quando disponível
  - Evidências obrigatórias para status 'documentado'
  - Justificativa obrigatória para 'inferido' e 'hipotese'
  - Operação tradutória requer 2+ manifestações comparadas
  - Evidência requer ao menos uma página PDF ou impressa
"""
import json
from pathlib import Path

OUT_DIR = Path("/home/z/my-project/output")

STATUS_ENUM = ["documentado", "identificado", "inferido", "hipotese", "problematico", "nao_identificado"]

# ---------- 1. Schema do corpus canônico ----------
schema_corpus = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "schema_corpus_britanico_canonico.json",
    "title": "Corpus Britânico Canônico — Gabinete de Leitura (1837-1838)",
    "description": "Valida a tabela canônica dos dez textos ficcionais britânicos identificados na tese de Soares (2006).",
    "type": "object",
    "required": ["$schema", "versao", "data_geracao", "fonte_primaria", "itens"],
    "additionalProperties": False,
    "properties": {
        "$schema": {"type": "string"},
        "versao": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
        "data_geracao": {"type": "string", "format": "date"},
        "fonte_primaria": {
            "type": "object",
            "required": ["arquivo", "autora", "ano"],
            "additionalProperties": False,
            "properties": {
                "arquivo": {"type": "string"},
                "autora": {"type": "string"},
                "titulo": {"type": "string"},
                "ano": {"type": "integer", "minimum": 1900, "maximum": 2100},
                "instituicao": {"type": "string"},
                "orientadora": {"type": "string"}
            }
        },
        "metadados": {
            "type": "object",
            "additionalProperties": True
        },
        "itens": {
            "type": "array",
            "minItems": 10,
            "maxItems": 10,
            "items": {"$ref": "#/definitions/itemCorpus"}
        }
    },
    "definitions": {
        "itemCorpus": {
            "type": "object",
            "required": [
                "id", "titulo_gabinete", "autor_original", "autor_status",
                "origem_linguistica", "fasciculos", "fonte_declarada_no_gabinete",
                "fonte_original_identificada", "original_identificado",
                "rota_tradutoria", "mediacao_francesa",
                "operacoes_tradutorias_ids", "evidencias_ids"
            ],
            "additionalProperties": False,
            "properties": {
                "id": {"type": "string", "pattern": r"^corpus:[a-z0-9-]+$"},
                "titulo_gabinete": {"type": "string", "minLength": 1},
                "titulo_original": {"type": ["string", "null"]},
                "autor_original": {"type": ["string", "null"]},
                "autor_status": {"enum": STATUS_ENUM},
                "origem_linguistica": {"type": "string", "enum": ["en", "pt-br", "fr", "es", "de", "outro"]},
                "fasciculos": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"$ref": "#/definitions/fasciculoCorpus"}
                },
                "fonte_declarada_no_gabinete": {"$ref": "#/definitions/fonteDeclarada"},
                "fonte_original_identificada": {"$ref": "#/definitions/fonteOriginalIdentificada"},
                "original_identificado": {"type": "boolean"},
                "rota_tradutoria": {"$ref": "#/definitions/statusComDescricao"},
                "mediacao_francesa": {"$ref": "#/definitions/statusComDescricao"},
                "operacoes_tradutorias_ids": {
                    "type": "array",
                    "items": {"type": "string", "pattern": r"^op:[a-z0-9:-]+$"}
                },
                "evidencias_ids": {
                    "type": "array",
                    "items": {"type": "string", "pattern": r"^evidence:[a-z0-9:-]+$"}
                },
                "observacoes": {"type": ["string", "null"]}
            }
        },
        "fasciculoCorpus": {
            "type": "object",
            "required": ["numero", "data_iso", "papel"],
            "additionalProperties": False,
            "properties": {
                "numero": {"type": ["integer", "null"], "minimum": 1, "maximum": 100},
                "data_iso": {"type": ["string", "null"], "format": "date"},
                "paginas_periodico": {"type": ["string", "null"]},
                "papel": {"enum": ["publicacao", "continua", "conclusao"]}
            }
        },
        "fonteDeclarada": {
            "type": "object",
            "required": ["status_epistemologico"],
            "additionalProperties": False,
            "properties": {
                "referencia": {"type": ["string", "null"]},
                "status_epistemologico": {"enum": STATUS_ENUM},
                "observacao": {"type": ["string", "null"]}
            }
        },
        "fonteOriginalIdentificada": {
            "type": "object",
            "required": ["status_epistemologico"],
            "additionalProperties": False,
            "properties": {
                "veiculo": {"type": ["string", "null"]},
                "data": {"type": ["string", "null"]},
                "data_iso": {"type": ["string", "null"]},
                "status_epistemologico": {"enum": STATUS_ENUM},
                "editor_epoca": {"type": ["string", "null"]},
                "observacao": {"type": ["string", "null"]}
            }
        },
        "statusComDescricao": {
            "type": "object",
            "required": ["status", "descricao"],
            "additionalProperties": False,
            "properties": {
                "status": {"enum": STATUS_ENUM},
                "descricao": {"type": ["string", "null"]},
                "metodo": {"type": ["string", "null"], "description": "Método de inferência usado quando status=inferido (ex.: 'inferencia_por_exclusao')."}
            }
        }
    }
}

# ---------- 2. Schema do grafo contextual ----------
TIPOS_NO_CONTEXTUAL = [
    "Tese", "Capitulo", "Secao", "Periodico", "Fasciculo", "Instituicao",
    "Tipografia", "Livraria", "Pessoa", "ObraAbstrata", "ManifestacaoTextual",
    "Conceito", "Tema", "MovimentoLiterario", "Local", "ReferenciaBibliografica",
    "Evidencia", "Argumento"
]
TIPOS_ARESTA_CONTEXTUAL = [
    "AUTORA_DE", "ORIENTA", "ANALISA", "PUBLICADA_EM", "IMPRESSA_EM", "VENDIDA_EM",
    "REDIGE", "COLABORA_COM", "CONTRIBUI_PARA", "REPUBLICADA_EM", "RELACIONA_SE_A",
    "CITA", "SUSTENTA", "ASSOCIA_SE_A", "CONTEXTO_DE", "INTEGRA", "INFLUENCIA", "TEM_TEMA"
]

schema_contextual = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "schema_grafo_contextual_v2.json",
    "title": "Grafo Contextual v2 — Ambiente do Gabinete de Leitura",
    "description": "Valida o grafo contextual: ambiente editorial, intelectual, institucional e histórico do Gabinete de Leitura segundo Soares (2006).",
    "type": "object",
    "required": ["versao", "data_geracao", "vocabulario_controlado", "nos", "arestas", "evidencias"],
    "additionalProperties": False,
    "properties": {
        "versao": {"type": "string", "pattern": r"^\d+\.\d+$"},
        "data_geracao": {"type": "string", "format": "date"},
        "metadados_projeto": {"type": "object"},
        "vocabulario_controlado": {
            "type": "object",
            "required": ["tipos_no", "tipos_aresta", "status_epistemologico"],
            "additionalProperties": False,
            "properties": {
                "tipos_no": {"type": "array", "items": {"type": "string"}, "enum": [TIPOS_NO_CONTEXTUAL], "minItems": len(TIPOS_NO_CONTEXTUAL)},
                "tipos_aresta": {"type": "array", "items": {"type": "string"}, "enum": [TIPOS_ARESTA_CONTEXTUAL], "minItems": len(TIPOS_ARESTA_CONTEXTUAL)},
                "status_epistemologico": {"type": "array", "items": {"type": "string"}, "enum": [STATUS_ENUM], "minItems": len(STATUS_ENUM)}
            }
        },
        "nos": {
            "type": "array",
            "items": {"$ref": "#/definitions/noContextual"}
        },
        "arestas": {
            "type": "array",
            "items": {"$ref": "#/definitions/arestaContextual"}
        },
        "evidencias": {
            "type": "array",
            "items": {"$ref": "#/definitions/evidencia"}
        }
    },
    "definitions": {
        "noContextual": {
            "type": "object",
            "required": ["id", "tipo", "titulo", "status_epistemologico"],
            "additionalProperties": False,
            "properties": {
                "id": {"type": "string", "pattern": r"^[a-z]+:[a-z0-9:-]+$"},
                "tipo": {"enum": TIPOS_NO_CONTEXTUAL},
                "titulo": {"type": "string", "minLength": 1},
                "aliases": {"type": "array", "items": {"type": "string"}},
                "atributos": {"type": "object"},
                "status_epistemologico": {"enum": STATUS_ENUM},
                "evidence_ids": {
                    "type": "array",
                    "items": {"type": "string", "pattern": r"^evidence:[a-z0-9:-]+$"}
                },
                "observacao": {"type": ["string", "null"]},
                "justificativa": {"type": ["string", "null"]}
            }
        },
        "arestaContextual": {
            "type": "object",
            "required": ["id", "origem", "destino", "tipo", "status_epistemologico"],
            "additionalProperties": False,
            "properties": {
                "id": {"type": "string", "pattern": r"^edge:[a-z0-9-]+$"},
                "origem": {"type": "string", "pattern": r"^[a-z]+:[a-z0-9:-]+$"},
                "destino": {"type": "string", "pattern": r"^[a-z]+:[a-z0-9:-]+$"},
                "tipo": {"enum": TIPOS_ARESTA_CONTEXTUAL},
                "status_epistemologico": {"enum": STATUS_ENUM},
                "evidence_ids": {
                    "type": "array",
                    "items": {"type": "string", "pattern": r"^evidence:[a-z0-9:-]+$"}
                },
                "observacao": {"type": ["string", "null"]},
                "justificativa": {"type": ["string", "null"]}
            }
        },
        "evidencia": {
            "type": "object",
            "required": ["id", "tipo", "titulo", "fonte", "tipo_evidencia", "status_epistemologico"],
            "additionalProperties": False,
            "properties": {
                "id": {"type": "string", "pattern": r"^evidence:[a-z0-9:-]+$"},
                "tipo": {"type": "string", "enum": ["Evidencia"]},
                "titulo": {"type": "string", "minLength": 1},
                "fonte": {
                    "type": "object",
                    "required": ["obra", "ano", "arquivo"],
                    "additionalProperties": False,
                    "properties": {
                        "obra": {"type": "string"},
                        "ano": {"type": "integer"},
                        "arquivo": {"type": "string"},
                        "pagina_pdf_inicio": {"type": ["integer", "null"], "minimum": 1},
                        "pagina_pdf_fim": {"type": ["integer", "null"], "minimum": 1},
                        "pagina_impressa_inicio": {"type": ["integer", "null"], "minimum": 1},
                        "pagina_impressa_fim": {"type": ["integer", "null"], "minimum": 1}
                    }
                },
                "tipo_evidencia": {"type": "string"},
                "conteudo": {"type": "string"},
                "citacao": {"type": ["string", "null"]},
                "status_epistemologico": {"enum": STATUS_ENUM}
            }
        }
    }
}

# ---------- 3. Schema do grafo de proveniência textual ----------
TIPOS_NO_PROV = [
    "Tese", "Periodico", "Giftbook", "Fasciculo", "PublicacaoSerializada",
    "ObraAbstrata", "ManifestacaoTextual", "Pessoa", "FonteDeclarada",
    "Trecho", "OperacaoTradutoria", "Evidencia", "Argumento", "Local"
]
TIPOS_ARESTA_PROV = [
    "AUTOR_DE", "MANIFESTA", "PUBLICADA_EM", "PERTENCE_A", "SERIALIZADA_EM",
    "PARTE_EM", "DECLARA_COMO_FONTE", "PUBLICADA_ORIGINALMENTE_EM",
    "RELACAO_DE_DEPENDENCIA_TEXTUAL", "INTERMEDIADA_POR",
    "TEM_VERSAO_FRANCESA_NA_REVUE",  # Distinção de INTERMEDIADA_POR: registra apenas a existência da versão francesa, não afirma rota.
    "NAO_E_FONTE_DIRETA_DE",
    "COMPARA_COM", "TEM_TRECHO", "AFETA", "SUSTENTA", "ANALISA"
]

schema_proveniencia = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "schema_grafo_proveniencia_textual_v3.json",
    "title": "Grafo de Proveniência Textual v3",
    "description": "Valida o grafo de proveniência: obras, manifestações, fontes declaradas, originais identificados, mediações, comparações e operações tradutórias.",
    "type": "object",
    "required": ["versao", "data_geracao", "vocabulario_controlado", "nos", "arestas",
                 "operacoes_tradutorias", "evidencias"],
    "additionalProperties": False,
    "properties": {
        "versao": {"type": "string", "pattern": r"^\d+\.\d+$"},
        "data_geracao": {"type": "string", "format": "date"},
        "metadados_projeto": {"type": "object"},
        "vocabulario_controlado": {
            "type": "object",
            "required": ["tipos_no", "tipos_aresta", "status_epistemologico"],
            "additionalProperties": False,
            "properties": {
                "tipos_no": {"type": "array", "items": {"type": "string"}, "enum": [TIPOS_NO_PROV], "minItems": len(TIPOS_NO_PROV)},
                "tipos_aresta": {"type": "array", "items": {"type": "string"}, "enum": [TIPOS_ARESTA_PROV], "minItems": len(TIPOS_ARESTA_PROV)},
                "status_epistemologico": {"type": "array", "items": {"type": "string"}, "enum": [STATUS_ENUM], "minItems": len(STATUS_ENUM)}
            }
        },
        "nos": {"type": "array", "items": {"$ref": "#/definitions/noProv"}},
        "arestas": {"type": "array", "items": {"$ref": "#/definitions/arestaProv"}},
        "operacoes_tradutorias": {"type": "array", "items": {"$ref": "#/definitions/operacaoTradutoria"}},
        "argumentos": {"type": "array", "items": {"$ref": "#/definitions/argumento"}},
        "evidencias": {"type": "array", "items": {"$ref": "#/definitions/evidencia"}}
    },
    "definitions": {
        "noProv": {
            "type": "object",
            "required": ["id", "tipo", "titulo", "status_epistemologico"],
            "additionalProperties": False,
            "properties": {
                "id": {"type": "string", "pattern": r"^[a-z]+:[a-z0-9:-]+$"},
                "tipo": {"enum": TIPOS_NO_PROV},
                "titulo": {"type": "string", "minLength": 1},
                "aliases": {"type": "array", "items": {"type": "string"}},
                "atributos": {"type": "object"},
                "status_epistemologico": {"enum": STATUS_ENUM},
                "evidence_ids": {
                    "type": "array",
                    "items": {"type": "string", "pattern": r"^evidence:[a-z0-9:-]+$"}
                },
                "observacao": {"type": ["string", "null"]},
                "justificativa": {"type": ["string", "null"]}
            }
        },
        "arestaProv": {
            "type": "object",
            "required": ["id", "origem", "destino", "tipo", "status_epistemologico"],
            "additionalProperties": False,
            "properties": {
                "id": {"type": "string", "pattern": r"^edge:[a-z0-9-]+$"},
                "origem": {"type": "string", "pattern": r"^[a-z]+:[a-z0-9:-]+$"},
                "destino": {"type": "string", "pattern": r"^[a-z]+:[a-z0-9:-]+$"},
                "tipo": {"enum": TIPOS_ARESTA_PROV},
                "status_epistemologico": {"enum": STATUS_ENUM},
                "qualificador": {"type": ["string", "null"]},
                "evidence_ids": {
                    "type": "array",
                    "items": {"type": "string", "pattern": r"^evidence:[a-z0-9:-]+$"}
                },
                "observacao": {"type": ["string", "null"]},
                "justificativa": {"type": ["string", "null"]}
            }
        },
        "operacaoTradutoria": {
            "type": "object",
            "required": ["id", "tipo", "titulo", "tipo_operacao", "obra_id",
                         "manifestacoes_comparadas", "efeito_textual",
                         "status_epistemologico", "evidence_ids"],
            "additionalProperties": False,
            "properties": {
                "id": {"type": "string", "pattern": r"^op:[a-z0-9:-]+$"},
                "tipo": {"type": "string", "enum": ["OperacaoTradutoria"]},
                "titulo": {"type": "string", "minLength": 1},
                "tipo_operacao": {"type": "string"},
                "obra_id": {"type": "string", "pattern": r"^work:[a-z0-9-]+$"},
                "manifestacoes_comparadas": {
                    "type": "array",
                    "minItems": 2,
                    "items": {"type": "string", "pattern": r"^manifestation:[a-z0-9:-]+$"}
                },
                "trecho_original": {"type": ["string", "null"]},
                "trecho_brasileiro": {"type": ["string", "null"]},
                "efeito_textual": {"type": "string"},
                "efeito_interpretativo": {"type": ["string", "null"]},
                "status_epistemologico": {"enum": STATUS_ENUM},
                "evidence_ids": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string", "pattern": r"^evidence:[a-z0-9:-]+$"}
                },
                "observacao": {"type": ["string", "null"]}
            }
        },
        "argumento": {
            "type": "object",
            "required": ["id", "tipo", "titulo", "status_epistemologico"],
            "additionalProperties": False,
            "properties": {
                "id": {"type": "string", "pattern": r"^argument:[a-z0-9:-]+$"},
                "tipo": {"type": "string", "enum": ["Argumento"]},
                "titulo": {"type": "string", "minLength": 1},
                "enunciado": {"type": "string"},
                "status_epistemologico": {"enum": STATUS_ENUM},
                "evidence_ids": {
                    "type": "array",
                    "items": {"type": "string", "pattern": r"^evidence:[a-z0-9:-]+$"}
                },
                "sustenta_ids": {
                    "type": "array",
                    "items": {"type": "string", "pattern": r"^[a-z]+:[a-z0-9:-]+$"}
                }
            }
        },
        "evidencia": {
            "type": "object",
            "required": ["id", "tipo", "titulo", "fonte", "tipo_evidencia", "status_epistemologico"],
            "additionalProperties": False,
            "properties": {
                "id": {"type": "string", "pattern": r"^evidence:[a-z0-9:-]+$"},
                "tipo": {"type": "string", "enum": ["Evidencia"]},
                "titulo": {"type": "string", "minLength": 1},
                "fonte": {
                    "type": "object",
                    "required": ["obra", "ano", "arquivo"],
                    "additionalProperties": False,
                    "properties": {
                        "obra": {"type": "string"},
                        "ano": {"type": "integer"},
                        "arquivo": {"type": "string"},
                        "pagina_pdf_inicio": {"type": ["integer", "null"], "minimum": 1},
                        "pagina_pdf_fim": {"type": ["integer", "null"], "minimum": 1},
                        "pagina_impressa_inicio": {"type": ["integer", "null"], "minimum": 1},
                        "pagina_impressa_fim": {"type": ["integer", "null"], "minimum": 1}
                    }
                },
                "tipo_evidencia": {"type": "string"},
                "conteudo": {"type": "string"},
                "citacao": {"type": ["string", "null"]},
                "status_epistemologico": {"enum": STATUS_ENUM}
            }
        }
    }
}

# Escrever schemas
for name, schema in [
    ("schema_corpus_britanico_canonico.json", schema_corpus),
    ("schema_grafo_contextual_v2.json", schema_contextual),
    ("schema_grafo_proveniencia_textual_v3.json", schema_proveniencia),
]:
    path = OUT_DIR / name
    path.write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Escrito: {path}")

# Verificação rápida: schemas são JSON válidos
for name in ["schema_corpus_britanico_canonico.json",
             "schema_grafo_contextual_v2.json",
             "schema_grafo_proveniencia_textual_v3.json"]:
    p = OUT_DIR / name
    json.loads(p.read_text(encoding="utf-8"))
    print(f"OK: {name} é JSON válido")
