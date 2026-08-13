# Gabinete de Leitura — Pacote de Dados Versionado (v3.1)

Pacote de dados extraído, validado e revisado a partir da tese de Maria Angélica Lau Pereira Soares (2006), ***Visão da Modernidade — A presença britânica no Gabinete de Leitura (1837-1838)***, dissertação de mestrado defendida na FFLCH/USP.

Este repositório contém dois grafos complementares acadêmicamente auditáveis sobre a presença britânica no *Gabinete de Leitura* (periódico publicado no Rio de Janeiro entre 13/08/1837 e 08/04/1838):

1. **Grafo contextual** — ambiente editorial, intelectual, institucional e histórico do *Gabinete de Leitura*.
2. **Grafo de proveniência textual** — obras, manifestações, fascículos, fontes declaradas, originais identificados, mediações, comparações e transformações tradutórias.

> ⚠️ **Princípio filológico**: a tese é a fonte de verdade primária. Nenhum dado foi inventado, preenchido por plausibilidade ou derivado de fontes externas sem registro explícito. Hipóteses e inferências estão marcadas com `status_epistemologico` apropriado.

## Estrutura do repositório

```
.
├── README.md                                  # Este arquivo
├── LICENSE                                    # MIT
├── .gitignore
├── data/
│   ├── corpus_britanico_canonico.json         # Tabela canônica dos 10 textos britânicos
│   ├── grafo_contextual_v2.json               # Ambiente editorial, intelectual, institucional
│   ├── grafo_proveniencia_textual_v3.json     # Proveniência textual: obras, manifestações, fontes, operações
│   ├── schema_corpus_britanico_canonico.json  # JSON Schema Draft-07 do corpus
│   ├── schema_grafo_contextual_v2.json         # JSON Schema Draft-07 do grafo contextual
│   ├── schema_grafo_proveniencia_textual_v3.json
│   └── relatorio_validacao.json               # Resultado da validação sintática, estrutural e semântica
├── docs/
│   ├── README.md                              # Documentação detalhada do pacote (v3.1)
│   └── relatorio_divergencias.md              # 22 divergências documentadas entre rascunhos e a tese
└── scripts/
    ├── build_corpus_canonico.py               # Gera o corpus canônico
    ├── build_grafo_contextual.py              # Gera o grafo contextual
    ├── build_grafo_proveniencia.py            # Gera o grafo de proveniência
    ├── build_schemas.py                       # Gera os três JSON Schemas
    └── validador_semantico.py                 # Validador semântico (regras que o JSON Schema não resolve)
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
# Requer Python 3.8+ e jsonschema
pip install jsonschema

# 1. Validar sintaxe JSON
for f in data/*.json; do python3 -c "import json; json.load(open('$f'))" && echo "OK: $f"; done

# 2. Validar cada JSON contra seu schema
python3 -c "
import json, jsonschema
pairs = [
    ('data/corpus_britanico_canonico.json', 'data/schema_corpus_britanico_canonico.json'),
    ('data/grafo_contextual_v2.json', 'data/schema_grafo_contextual_v2.json'),
    ('data/grafo_proveniencia_textual_v3.json', 'data/schema_grafo_proveniencia_textual_v3.json'),
]
for g, s in pairs:
    jsonschema.validate(json.load(open(g)), json.load(open(s)))
    print(f'OK: {g}')
"

# 3. Validador semântico (regras que o JSON Schema não resolve sozinho)
python3 scripts/validador_semantico.py
# Saída: data/relatorio_validacao.json
```

## Histórico de versões

| Versão | Data | Descrição |
|--------|------|-----------|
| v2.2 | anterior | Rascunho com fascículos embaralhados, placeholders "c1830", manifestação inglesa fabricada de O Sedutor, aresta `TRADUZIDA_DE` indevida |
| v3.0 | 2026-08-14 | Correção dos 12 fascículos/datas; eliminação de placeholders; separação de schemas; relatório de divergências; modelo tri-relacional (fonte declarada / original / mediação) |
| **v3.1** | **2026-08-14** | **Quatro ajustes finais de revisão:** (1) offset de paginação não universal; (2) mediação francesa rebaixada para `inferido` com nova aresta `TEM_VERSAO_FRANCESA_NA_REVUE`; (3) rota de Costumes Ingleses rebaixada para `nao_identificado`; (4) divergência interna da tese sobre *The Anatomy of Drunkness* preservada. |

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
@misc{gabinete_leitura_pacote_v31,
  title  = {Gabinete de Leitura — Pacote de Dados Versionado (v3.1)},
  author = {Extraído e validado a partir de Soares, Maria Angélica Lau Pereira (2006)},
  year   = {2026},
  note   = {Grafo contextual e grafo de proveniência textual dos dez textos britânicos do Gabinete de Leitura (1837-1838)},
  url    = {https://github.com/SEU_USUARIO/gabinete-leitura-dados}
}
```
