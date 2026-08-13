# Modelo de dados

## Visão geral

O pacote é composto por três JSONs canônicos e seus respectivos schemas:

```text
data/
├── corpus_britanico_canonico.json      # Tabela canônica dos 10 textos britânicos
├── grafo_contextual_v2.json             # Ambiente editorial/intelectual/institucional
├── grafo_proveniencia_textual_v3.json   # Proveniência textual (obras, manifestações, fontes)
├── relatorio_validacao.json             # Resultado da validação semântica
└── schemas/
    ├── corpus.schema.json               # Draft-07 do corpus
    ├── contextual.schema.json           # Draft-07 do grafo contextual
    └── proveniencia.schema.json         # Draft-07 do grafo de proveniência
```

## Corpus canônico (`corpus_britanico_canonico.json`)

Tabela canônica dos dez textos ficcionais britânicos identificados no Gabinete de Leitura. **É a fonte da verdade para datas, fascículos e status de cada texto**. O HTML deve consumir este arquivo para cronologia; os grafos acrescentam relações e contexto, mas não redefinem fatos bibliográficos.

### Estrutura

```json
{
  "versao": "1.1.0",
  "itens": [
    {
      "id": "corpus:slug-estavel",
      "titulo_gabinete": "...",
      "titulo_original": null | "...",
      "autor_original": null | "...",
      "autor_status": "identificado | problematico | nao_identificado",
      "fasciculos": [
        {
          "numero": 30,
          "data_iso": "1838-03-04",
          "paginas_periodico": "233-236",
          "papel": "publicacao | continua | conclusao"
        }
      ],
      "fonte_declarada_no_gabinete": {
        "referencia": null | "Colburn's Magazine",
        "status_epistemologico": "documentado | problematico",
        "observacao": "..."
      },
      "fonte_original_identificada": {
        "veiculo": null | "The New Monthly Magazine and Humorist",
        "data": null | "1837-06",
        "status_epistemologico": "identificado | nao_identificado"
      },
      "rota_tradutoria": {
        "status": "documentado | nao_identificado | ...",
        "descricao": "..."
      },
      "mediacao_francesa": {
        "status": "documentado | inferido",
        "metodo": "inferencia_por_exclusao",  // quando status=inferido
        "descricao": "..."
      },
      "operacoes_tradutorias_ids": ["op:..."],
      "evidencias_ids": ["evidence:..."],
      "observacoes": "..."
    }
  ]
}
```

## Grafo contextual (`grafo_contextual_v2.json`)

Responde: *Quem compõe o ambiente editorial, intelectual, institucional e histórico do Gabinete de Leitura?*

### Tipos de nó

```text
Tese, Capitulo, Secao, Periodico, Fasciculo, Instituicao, Tipografia, Livraria,
Pessoa, ObraAbstrata, ManifestacaoTextual, Conceito, Tema, MovimentoLiterario,
Local, ReferenciaBibliografica, Evidencia, Argumento
```

### Tipos de aresta

```text
AUTORA_DE, ORIENTA, ANALISA, PUBLICADA_EM, IMPRESSA_EM, VENDIDA_EM,
REDIGE, COLABORA_COM, CONTRIBUI_PARA, REPUBLICADA_EM, RELACIONA_SE_A,
CITA, SUSTENTA, ASSOCIA_SE_A, CONTEXTO_DE, INTEGRA, INFLUENCIA, TEM_TEMA
```

## Grafo de proveniência textual (`grafo_proveniencia_textual_v3.json`)

Responde: *Como cada texto de origem britânica chegou ao Gabinete de Leitura e o que mudou no percurso até o leitor fluminense?*

### Tipos de nó

```text
Tese, Periodico, Giftbook, Fasciculo, PublicacaoSerializada,
ObraAbstrata, ManifestacaoTextual, Pessoa, FonteDeclarada, Trecho,
OperacaoTradutoria, Evidencia, Argumento, Local
```

### Tipos de aresta

```text
AUTOR_DE, MANIFESTA, PUBLICADA_EM, PERTENCE_A, SERIALIZADA_EM,
PARTE_EM, DECLARA_COMO_FONTE, PUBLICADA_ORIGINALMENTE_EM,
RELACAO_DE_DEPENDENCIA_TEXTUAL, INTERMEDIADA_POR,
TEM_VERSAO_FRANCESA_NA_REVUE,    # existência inferida (não rota)
NAO_E_FONTE_DIRETA_DE,           # afirmação negativa expressa da tese
COMPARA_COM, TEM_TRECHO, AFETA, SUSTENTA, ANALISA
```

### Distinção crítica: fonte declarada vs original vs mediação

```text
Manifestação brasileira
  │
  ├── DECLARA_COMO_FONTE → FonteDeclarada        # o que o Gabinete diz
  │
  ├── RELACAO_DE_DEPENDENCIA_TEXTUAL              # comparação demonstrada
  │     → Manifestação original (em inglês)
  │     [qualificador: original_identificado_para_comparacao]
  │
  ├── PUBLICADA_ORIGINALMENTE_EM                  # veículo original identificado
  │     → Periodico ou Giftbook
  │
  ├── TEM_VERSAO_FRANCESA_NA_REVUE                # existência inferida (7 textos)
  │     → Revue Britannique
  │     [status: inferido, metodo: inferencia_por_exclusao]
  │
  └── NAO_E_FONTE_DIRETA_DE                      # negação expressa (Costumes Ingleses)
        → Manifestação francesa Le Cockney Campagnard
```

> ⚠️ `INTERMEDIADA_POR` (que sugeriria rota) **não deve** ser usada para os 7 textos não-excepcionais — apenas `TEM_VERSAO_FRANCESA_NA_REVUE`. A tese demonstra existência, não rota.

### Operação tradutória

```json
{
  "id": "op:costumes:atenuacao-ironia-fieldlove",
  "tipo": "OperacaoTradutoria",
  "titulo": "Atenuação da ironia sobre Fieldlove",
  "tipo_operacao": "ATENUACAO_DE_IRONIA",
  "obra_id": "work:a-cockney-country-gentleman",
  "manifestacoes_comparadas": [
    "manifestation:en:new-monthly:cockney-country-gentleman:1837-06",
    "manifestation:pt-br:gabinete:costumes-ingleses:1838-03-04"
  ],
  "trecho_original": "...",
  "trecho_brasileiro": "...",
  "efeito_textual": "...",
  "efeito_interpretativo": "...",
  "status_epistemologico": "documentado",
  "evidence_ids": ["evidence:..."]
}
```

> Não crie operação tradutória sem comparação textual explícita na tese. Toda operação deve ter 2+ manifestações comparadas.

### Evidência

```json
{
  "id": "evidence:soares:2006:pdf-p106-111:costumes-comparacao",
  "tipo": "Evidencia",
  "titulo": "...",
  "fonte": {
    "obra": "Soares, 2006",
    "ano": 2006,
    "arquivo": "TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf",
    "pagina_pdf_inicio": 106,
    "pagina_pdf_fim": 111,
    "pagina_impressa_inicio": 98,
    "pagina_impressa_fim": 103
  },
  "tipo_evidencia": "comparacao_textual | declaracao_autoral | identificacao_original | ...",
  "conteudo": "Resumo fiel da evidência, sem extrapolação.",
  "citacao": null | "texto literal",
  "status_epistemologico": "documentado"
}
```

## Regras que o JSON Schema não resolve sozinho

Implementadas em `scripts/validador_semantico.py`:

1. IDs únicos em nós, arestas, evidências, operações e argumentos.
2. Toda `origem` e `destino` de aresta existe em `nos`.
3. Todo `evidence_id` referido existe em `evidencias`.
4. O tipo de relação é compatível com tipos de origem/destino.
5. Fascículo, data e manifestação brasileira são coerentes com o corpus canônico.
6. Não há placeholders (`??`, `pendente`, `cerca de`, `c1830`, etc.).
7. Toda obra serializada tem todas as partes registradas.
8. Uma relação com `problematico` não pode ser apresentada como rota documentada.
9. Não existem páginas PDF/impressas trocadas (offset 8 verificado quando ambas presentes).
10. Toda afirmação `documentado` possui pelo menos um `evidence_id` (com exceções para nós-metadata da tese).
11. `inferido` e `hipotese` exigem `observacao` ou `justificativa` preenchida.
12. Operação tradutória deve ter 2+ manifestações comparadas.
13. Evidência deve ter ao menos uma página PDF ou impressa.

## Estatísticas atuais (v0.4.0)

| Métrica | Valor |
|---------|-------|
| Textos no corpus canônico | 10 |
| Nós no grafo contextual | 76 |
| Arestas no grafo contextual | 65 |
| Nós no grafo de proveniência | 108 |
| Arestas no grafo de proveniência | 127 |
| Evidências | 42 (36 únicas, 6 compartilhadas entre grafos) |
| Operações tradutórias | 7 |
| Argumentos da tese modelados | 10 (5 em cada grafo) |
| Erros de validação (alta gravidade) | 0 |
| Placeholders remanescentes | 0 |
| Arestas órfãs | 0 |
| Testes de regressão | 67 (todos passando) |
