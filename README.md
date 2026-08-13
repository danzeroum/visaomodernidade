# visaomodernidade — Pacote de Dados Acadêmicos Versionados (v0.4.0)

[![Validate academic data](https://github.com/danzeroum/visaomodernidade/actions/workflows/validate-data.yml/badge.svg)](https://github.com/danzeroum/visaomodernidade/actions/workflows/validate-data.yml)
[![Deploy to Pages](https://github.com/danzeroum/visaomodernidade/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/danzeroum/visaomodernidade/actions/workflows/deploy-pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Pacote de dados extraído, validado e revisado a partir da tese de Maria Angélica Lau Pereira Soares (2006), ***Visão da Modernidade — A presença britânica no Gabinete de Leitura (1837-1838)***, dissertação de mestrado defendida na FFLCH/USP.

Este repositório contém dois grafos complementares acadêmicamente auditáveis sobre a presença britânica no *Gabinete de Leitura* (periódico publicado no Rio de Janeiro entre 13/08/1837 e 08/04/1838):

1. **Grafo contextual** — ambiente editorial, intelectual, institucional e histórico do *Gabinete de Leitura*.
2. **Grafo de proveniência textual** — obras, manifestações, fascículos, fontes declaradas, originais identificados, mediações, comparações e transformações tradutórias.

> ⚠️ **Princípio filológico**: a tese é a fonte de verdade primária. Nenhum dado foi inventado, preenchido por plausibilidade ou derivado de fontes externas sem registro explícito. Hipóteses e inferências estão marcadas com `status_epistemologico` apropriado.

## Estrutura do repositório

```
.
├── README.md                                  # Este arquivo
├── LICENSE                                    # MIT + nota acadêmica
├── CONTRIBUTING.md                            # Princípios filológicos e fluxo de contribuição
├── CHANGELOG.md                               # Histórico de versões
├── pyproject.toml                             # Configuração do pacote Python
├── requirements.txt                           # Dependências de execução
├── requirements-dev.txt                       # Dependências de desenvolvimento
├── Makefile                                   # Atalhos: install, build, validate, test, site
├── .gitignore
├── .github/workflows/
│   ├── validate-data.yml                      # CI: build + validate + test + sync check
│   └── deploy-pages.yml                       # Deploy do site/ no GitHub Pages
├── data/
│   ├── corpus_britanico_canonico.json         # Tabela canônica dos 10 textos britânicos
│   ├── grafo_contextual_v2.json               # Ambiente editorial, intelectual, institucional
│   ├── grafo_proveniencia_textual_v3.json     # Proveniência textual
│   ├── relatorio_validacao.json               # Resultado da validação semântica
│   └── schemas/
│       ├── corpus.schema.json                 # JSON Schema Draft-07 do corpus
│       ├── contextual.schema.json             # JSON Schema Draft-07 do grafo contextual
│       └── proveniencia.schema.json           # JSON Schema Draft-07 do grafo de proveniência
├── docs/
│   ├── README.md                              # Documentação detalhada
│   ├── metodologia.md                         # Princípios filológicos e regras
│   ├── modelo-de-dados.md                     # Estrutura dos JSONs e regras de validação
│   └── relatorio_divergencias.md              # 22 divergências documentadas
├── scripts/
│   ├── build_all.py                           # Ponto de entrada único para regenerar tudo
│   ├── validate.py                            # Ponto de entrada único para validação
│   ├── build_schemas.py                       # Gera os 3 JSON Schemas
│   ├── build_corpus_canonico.py               # Gera o corpus canônico
│   ├── build_grafo_contextual.py              # Gera o grafo contextual
│   ├── build_grafo_proveniencia.py            # Gera o grafo de proveniência
│   └── validador_semantico.py                 # Validador semântico (13 regras extras)
├── src/visaomodernidade/
│   ├── __init__.py
│   ├── config.py                              # Caminhos, constantes, vocabulário controlado
│   └── cli.py                                 # Entry points (visaomodernidade-build, -validate)
├── tests/
│   ├── conftest.py                            # Fixtures compartilhadas
│   ├── test_corpus_canonico.py                # 33 testes (10 textos + ajustes v3.1 + placeholders)
│   ├── test_schema_validacao.py               # 5 testes (schemas Draft-07)
│   ├── test_integridade_grafos.py             # 15 testes (IDs, arestas, evidências, paginação)
│   ├── test_relatorio_validacao.py            # 9 testes (critérios de aceite Parte H)
│   ├── test_fixtures_invalidas.py             # 4 testes (testes negativos)
│   └── fixtures/
│       ├── corpus_invalido.json
│       └── grafo_com_aresta_orfa.json
└── site/
    ├── index.html                             # MVP da exposição digital (placeholder)
    └── assets/
        ├── styles.css
        └── app.js
```

## Início rápido

```bash
# Clone o repositório
git clone https://github.com/danzeroum/visaomodernidade.git
cd visaomodernidade

# Instale as dependências (execução + desenvolvimento)
make dev

# Regenera todos os dados a partir dos scripts
make build

# Valida os dados (semântica + schemas)
make validate

# Roda os 67 testes de regressão
make test

# Espelha o CI do GitHub Actions localmente
make ci

# Servir o site/ localmente em http://localhost:8000
make site
```

## Resumo do pacote

| Métrica | Valor |
|---------|-------|
| Textos no corpus canônico | 10 |
| Nós no grafo contextual | 76 |
| Arestas no grafo contextual | 65 |
| Nós no grafo de proveniência | 108 |
| Arestas no grafo de proveniência | 127 |
| Evidências (com paginação dupla PDF/impressa) | 42 (36 únicas, 6 compartilhadas) |
| Operações tradutórias documentadas | 7 |
| Argumentos da tese modelados | 10 (5 em cada grafo) |
| Erros de validação (alta gravidade) | 0 |
| Placeholders remanescentes | 0 |
| Arestas órfãs | 0 |
| **Testes de regressão** | **67 (todos passando)** |

## Status epistemológico

Toda afirmação usa um dos seis status abaixo, garantindo distinção visual entre fatos, inferências, hipóteses e lacunas:

| Status | Quando usar |
|--------|-------------|
| `documentado` | Declaração explícita, transcrição, comparação ou dado verificável na tese. Exige `evidence_ids` não vazio. |
| `identificado` | Original ou atribuição localizado e confirmado pela pesquisa apresentada na tese. |
| `inferido` | Conclusão derivada de evidências indiretas; exige `observacao`/`justificativa` e, quando aplicável, `metodo`. |
| `hipotese` | Possibilidade acadêmica plausível, mas sem confirmação documental suficiente. |
| `problematico` | Fonte declarada inconsistente, original não localizado, atribuição duvidosa ou conflito documental. |
| `nao_identificado` | Informação ausente ou ainda não localizada. |

Veja `docs/metodologia.md` para detalhes.

## Os dez textos do corpus

| # | Título no Gabinete | Fasc. | Data | Original | Autor |
|---|---------------------|-------|------|----------|-------|
| 1 | Costumes Ingleses — Um Amador da Vida Campestre | n.30 | 04/03/1838 | A Cockney Country-Gentleman (NMM, jun/1837) | John Poole |
| 2 | Uma Noite no Mar | n.2 | 20/08/1837 | Davy Jones and the Yankee Privateer (Blackwood's, jul/1830) | não identificado |
| 3 | O Testamento | n.9 | 08/10/1837 | **não localizado** | George Crabbe (atribuição problemática) |
| 4 | O Livro da Vida | n.6 | 17/09/1837 | **não localizado** | não identificado |
| 5 | O Sedutor | n.10 | 15/10/1837 | **não identificado pela tese** | Washington Irving (americano) |
| 6 | Manuscrito Achado em uma Casa de Loucos | n.8 | 01/10/1837 | A Manuscript Found in a Madhouse (Literary Souvenir 1829) | Edward Bulwer-Lytton |
| 7 | As Honras Hereditárias | n.11 | 22/10/1837 | Hereditary Honours (NMM, 1832) | Edward Bulwer-Lytton |
| 8 | Terêncio o Alfaiate | n.14 | 12/11/1837 | Terence O'Flaherty (Forget-me-Not 1829) | Robert Macnish (pseud. A Modern Pythagorean) |
| 9 | Álibi | n.12 | 29/10/1837 | The Alibi; an Assize Anedocte (NMM, fev/1836) | Thomas Colley Grattan |
| 10 | Esboços Sicilianos | n.31-34 | 11/03 a 01/04/1838 | Sicilian Facts (The Metropolitan; data não especificada) | Edward D. Baynes |

## Como reproduzir a validação

```bash
# 1. Sintaxe JSON
for f in data/*.json data/schemas/*.json; do python -c "import json; json.load(open('$f'))" && echo "OK: $f"; done

# 2. Cada JSON contra seu schema
python -c "
import json, jsonschema
pairs = [
    ('data/corpus_britanico_canonico.json', 'data/schemas/corpus.schema.json'),
    ('data/grafo_contextual_v2.json', 'data/schemas/contextual.schema.json'),
    ('data/grafo_proveniencia_textual_v3.json', 'data/schemas/proveniencia.schema.json'),
]
for g, s in pairs:
    jsonschema.validate(json.load(open(g)), json.load(open(s)))
    print(f'OK: {g}')
"

# 3. Validador semântico
python scripts/validate.py

# 4. Testes de regressão (67 testes)
python -m pytest tests/ -v
```

## Automação CI/CD

### `validate-data.yml` (CI em cada PR/push para main)

1. Instala dependências (`pip install -r requirements-dev.txt && pip install -e .`).
2. Roda `python scripts/build_all.py` (regenera schemas, corpus, grafos).
3. Roda `python scripts/validate.py` (validador semântico).
4. Roda `python -m pytest tests/ -v` (67 testes de regressão).
5. **Verifica sincronia `data/`↔scripts**: se `git status data/` mostra mudanças após o build, o CI falha (dados committed estão stale).
6. Upload do `relatorio_validacao.json` como artifact.

### `deploy-pages.yml` (deploy automático no push para main)

1. Valida os dados (rodando build + validate).
2. Copia `data/*.json` e `data/schemas/` para `site/data/`.
3. Faz upload de `site/` como artifact do GitHub Pages.
4. Deploy em `https://danzeroum.github.io/visaomodernidade/`.

## Histórico de versões

| Versão | Data | Descrição |
|--------|------|-----------|
| v0.2.2 | anterior | Rascunho com fascículos embaralhados, placeholders, manifestação inglesa fabricada |
| v0.3.0 | 2026-08-14 | Correção dos 12 fascículos/datas; eliminação de placeholders; separação de schemas; 22 divergências documentadas; modelo tri-relacional |
| v0.3.1 | 2026-08-14 | 4 ajustes finais: offset não universal; mediação rebaixada para `inferido` + nova aresta `TEM_VERSAO_FRANCESA_NA_REVUE`; rota de Costumes `nao_identificado`; divergência interna de Anatomy of Drunkness preservada |
| **v0.4.0** | **2026-08-14** | **Engenharia de projeto:** `pyproject.toml`, `Makefile`, `src/visaomodernidade/` modular, 67 testes de regressão, GitHub Actions CI/CD, `CONTRIBUTING.md`, `CHANGELOG.md`, `docs/metodologia.md`, `docs/modelo-de-dados.md`, `site/` placeholder |

Veja `CHANGELOG.md` para detalhes completos.

## Lacunas reais que permanecem abertas na tese

1. **O Testamento** — original não localizado; atribuição a George Crabbe não confirmada nem negada; fonte declarada (Crabbe's Posthumous Works) inexistente.
2. **O Livro da Vida** — original não localizado; fonte declarada (Retrospective Review) problemática.
3. **O Sedutor** — tese não identifica título, veículo ou data de publicação original do texto de Washington Irving.
4. **Sicilian Facts** — tese não fornece data específica de publicação em The Metropolitan.
5. **Edward D. Baynes** — sem verbete no Anexo 3; apenas menção no corpo do texto.
6. **Redatores do Gabinete** — a tese afirma: "Não se pode saber com certeza quem eram os redatores do Gabinete de Leitura".
7. **Rota tradutória exata** — a tese demonstra comparação mas não afirma rota direta do inglês, nem via francês (exceto para o caso negativo de Costumes Ingleses).
8. **Tradutor(es)** — em nenhum dos dez textos o tradutor é identificado; todos os atributos `tradutor` são `null`.

## Fonte primária

```
SOARES, Maria Angélica Lau Pereira. Visão da Modernidade: A Presença
Britânica no Gabinete de Leitura (1837-1838). 209f. Dissertação
(Mestrado em Estudos Lingüísticos e Literários em Inglês) —
Universidade de São Paulo, São Paulo, 2006.
Orientadora: Sandra Guardini Teixeira Vasconcelos.
```

## Licença

MIT — veja `LICENSE`.

## Como citar este pacote

```bibtex
@misc{visaomodernidade_v040,
  title  = {visaomodernidade — Pacote de Dados Acadêmicos Versionados (v0.4.0)},
  author = {Extraído e validado a partir de Soares, Maria Angélica Lau Pereira (2006)},
  year   = {2026},
  note   = {Grafo contextual e grafo de proveniência textual dos dez textos britânicos do Gabinete de Leitura (1837-1838)},
  url    = {https://github.com/danzeroum/visaomodernidade}
}
```
