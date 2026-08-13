# Gabinete de Leitura — Pacote de Dados Versionado

Pacote de dados extraído e validado da tese de Maria Angélica Lau Pereira Soares (2006), *Visão da Modernidade — A presença britânica no Gabinete de Leitura (1837-1838)*, dissertação de mestrado defendida na FFLCH/USP.

## 1. Estrutura do pacote

```
output/
├── corpus_britanico_canonico.json       # Tabela canônica dos 10 textos britânicos
├── grafo_contextual_v2.json             # Ambiente editorial, intelectual, institucional e histórico
├── grafo_proveniencia_textual_v3.json    # Proveniência textual: obras, manifestações, fontes, operações
├── schema_corpus_britanico_canonico.json
├── schema_grafo_contextual_v2.json
├── schema_grafo_proveniencia_textual_v3.json
├── relatorio_validacao.json             # Resultado da validação sintática, estrutural e semântica
├── relatorio_divergencias.md            # Divergências entre rascunhos anteriores e a tese
└── README.md                            # Este arquivo
```

## 2. Hierarquia de confiança

```
Tese (PDF)                                  >  evidência primária
Fontes e páginas explicitamente citadas     >  evidência documentada
HTML e JSONs anteriores (v2, v2.1, v2.2)   >  somente candidatos / pistas
Inferência do agente                        >  marcada como 'inferido' ou 'hipotese'
Ausência de dado                            >  marcada como 'nao_identificado'
```

Em caso de conflito entre um JSON anterior e a tese, **a tese prevalece**. As divergências foram registradas em `relatorio_divergencias.md`.

## 3. Paginação dupla

Cada evidência armazena as duas formas de paginação quando disponíveis:

```json
{
  "pagina_pdf_inicio": 106,
  "pagina_pdf_fim": 111,
  "pagina_impressa_inicio": 98,
  "pagina_impressa_fim": 103
}
```

**Offset verificado** (somente para o corpo da dissertação a partir do Capítulo 1): `pagina_pdf = pagina_impressa + 8` (Capítulo 6 começa no PDF p.84 = impressa p.76).

> ⚠️ **Não há offset universal garantido para toda a dissertação.** As páginas pré-textuais (capa, folha de rosto, resumo, abstract, sumário) seguem paginação própria e não devem ser derivadas por esta regra. Consumidores (HTML, scripts) **nunca** devem derivar uma paginação a partir da outra em tempo de execução — cada evidência deve armazenar explicitamente ambas quando disponíveis.

## 4. Status epistemológico

Toda afirmação, evidência, nó ou aresta usa um dos status abaixo:

| Status | Quando usar |
|--------|-------------|
| `documentado` | Declaração explícita, transcrição, comparação ou dado verificável na tese. Exige `evidence_ids` não vazio. |
| `identificado` | Original ou atribuição localizado e confirmado pela pesquisa apresentada na tese. |
| `inferido` | Conclusão derivada de evidências indiretas; exige `observacao`/`justificativa`. |
| `hipotese` | Possibilidade acadêmica plausível, mas sem confirmação documental suficiente; exige `observacao`/`justificativa`. |
| `problematico` | Fonte declarada inconsistente, original não localizado, atribuição duvidosa ou conflito documental. |
| `nao_identificado` | Informação ausente ou ainda não localizada. |

## 5. Corpus canônico — os dez textos

| # | Título no Gabinete | Fascículo(s) | Data | Original identificado | Status |
|---|---------------------|---------------|------|----------------------|--------|
| 1 | Costumes Ingleses — Um Amador da Vida Campestre | n.30 | 04/03/1838 | A Cockney Country-Gentleman (John Poole, The New Monthly Magazine and Humorist, jun/1837) | identificado |
| 2 | Uma Noite no Mar | n.2 | 20/08/1837 | Davy Jones and the Yankee Privateer (Blackwood's Magazine, jul/1830; 4º de 5 episódios) | identificado |
| 3 | O Testamento | n.9 | 08/10/1837 | não localizado (atribuição a George Crabbe; fonte declarada inexistente) | problematico |
| 4 | O Livro da Vida | n.6 | 17/09/1837 | não localizado (fonte Retrospective Review problemática; já publicado n'O Chronista) | problematico |
| 5 | O Sedutor | n.10 | 15/10/1837 | Washington Irving (americano); título/veículo original não identificado pela tese | nao_identificado |
| 6 | Manuscrito Achado em uma Casa de Loucos | n.8 | 01/10/1837 | A Manuscript Found in a Madhouse (Edward Bulwer-Lytton, Literary Souvenir 1829) | identificado |
| 7 | As Honras Hereditárias | n.11 | 22/10/1837 | Hereditary Honours — A Tale of Love and Mystery (Bulwer-Lytton, The New Monthly and Literary Journal, 1832) | identificado |
| 8 | Terêncio o Alfaiate | n.14 | 12/11/1837 | Terence O'Flaherty (Robert Macnish, pseud. A Modern Pythagorean, Forget-me-Not para 1829) | identificado |
| 9 | Álibi | n.12 | 29/10/1837 | The Alibi; an Assize Anedocte (Thomas Colley Grattan, New Monthly Magazine and Literary Journal, fev/1836) | identificado |
| 10 | Esboços Sicilianos | n.31-34 | 11/03 a 01/04/1838 | Sicilian Facts (Edward D. Baynes, The Metropolitan; data não especificada na tese) | identificado |

## 6. Estatísticas dos grafos

| Métrica | Grafo contextual | Grafo de proveniência |
|---------|------------------|----------------------|
| Nós | 76 | 108 |
| Arestas | 65 | 127 |
| Evidências | 11 (+31 compartilhadas com proveniência) | 31 |
| Operações tradutórias | — | 7 |
| Argumentos | — | 5 (próprios) + 5 no contextual |

Evidências únicas totais: 36 (31 no proveniência + 5 contextuais exclusivas; 6 compartilhadas entre os dois grafos).

## 7. Como os dois grafos serão consumidos por HTML estático

Os dois grafos são **complementares** e projetados para alimentar uma visualização HTML estática (p. ex. o `gabinete-leitura-digital.html` já existente):

### Grafo contextual (`grafo_contextual_v2.json`)

**Pergunta respondida**: *Quem compõe o ambiente editorial, intelectual, institucional e histórico do Gabinete de Leitura?*

**Uso em HTML estático**:
- Renderizar a "linha do tempo" do periódico (1837-08-13 a 1838-04-08) com 35 fascículos.
- Renderizar a "rede de agentes" (redatores prováveis: Josino do Nascimento Silva, Justiniano José da Rocha, Firmino Rodrigues da Silva; livraria H. & E. Laemmert; tipografia Commercial).
- Renderizar os "capítulos da tese" como seções navegáveis com paginação dupla.
- Renderizar os conceitos e temas (modernidade, missão do intelectual, romantismo, silver-fork novels, romance gótico, mediação da Revue Britannique).
- Renderizar os locais (Rio de Janeiro, Londres, Paris, Albion) e suas conexões.

### Grafo de proveniência textual (`grafo_proveniencia_textual_v3.json`)

**Pergunta respondida**: *Como cada texto de origem britânica chegou ao Gabinete de Leitura e o que mudou no percurso até o leitor fluminense?*

**Uso em HTML estático**:
- Renderizar uma "árvore de proveniência" por texto, distinguindo:
  - **Fonte declarada no Gabinete** (às vezes problemática — visualmente diferenciada).
  - **Original identificado pela tese** (quando localizado).
  - **Veículo original** (periódico ou gift book britânico).
  - **Mediação francesa** (Revue Britannique — explícita para 7 textos, negada para Costumes Ingleses).
- Renderizar as **operações tradutórias** com trecho original vs trecho brasileiro e efeito interpretativo.
- Renderizar o **status epistemológico** de cada relação com código visual:
  - `documentado` = verde sólido
  - `identificado` = verde tracejado
  - `inferido` = amarelo
  - `hipotese` = laranja tracejado
  - `problematico` = vermelho sólido
  - `nao_identificado` = cinza
- Renderizar a **serialização** de Esboços Sicilianos (4 fascículos conectados em série).

### Estratégia de carregamento

```html
<!-- Exemplo de carregamento em HTML estático -->
<script type="module">
  import corpus from './corpus_britanico_canonico.json' assert { type: 'json' };
  import grafoCtx from './grafo_contextual_v2.json' assert { type: 'json' };
  import grafoProv from './grafo_proveniencia_textual_v3.json' assert { type: 'json' };

  // 1. Filtra o corpus para a tabela de 10 textos
  const tabela10Textos = corpus.itens;

  // 2. Para cada item da tabela, busca a manifestação brasileira no grafo de proveniência
  function encontrarManifestacaoBR(corpusId) {
    // ... usa arestas MANIFESTA + obra_id
  }

  // 3. Para cada manifestação brasileira, busca:
  //    a) DECLARA_COMO_FONTE → fonte declarada
  //    b) RELACAO_DE_DEPENDENCIA_TEXTUAL → original
  //    c) INTERMEDIADA_POR → Revue Britannique
  //    d) COMPARA_COM ← OperacaoTradutoria
</script>
```

## 8. Como reproduzir a validação

```bash
# Requer Python 3.8+ e jsonschema
pip install jsonschema

# 1. Validar sintaxe JSON (todos são válidos)
for f in output/*.json; do python3 -c "import json; json.load(open('$f'))" && echo "OK: $f"; done

# 2. Validar cada JSON contra seu schema
python3 -c "
import json, jsonschema
pairs = [
    ('output/corpus_britanico_canonico.json', 'output/schema_corpus_britanico_canonico.json'),
    ('output/grafo_contextual_v2.json', 'output/schema_grafo_contextual_v2.json'),
    ('output/grafo_proveniencia_textual_v3.json', 'output/schema_grafo_proveniencia_textual_v3.json'),
]
for g, s in pairs:
    jsonschema.validate(json.load(open(g)), json.load(open(s)))
    print(f'OK: {g}')
"

# 3. Validador semântico (regras que o JSON Schema não resolve sozinho)
python3 scripts/validador_semantico.py
# Saída: relatorio_validacao.json
```

## 9. Critérios de aceite (Parte H)

| Critério | Status |
|----------|--------|
| JSONs são sintaticamente válidos | OK |
| Ambos os JSONs passam nos schemas correspondentes | OK |
| O relatório semântico não possui erros de gravidade alta | OK (0 erros) |
| O corpus canônico contém exatamente 10 itens e nenhum placeholder | OK |
| Todos os fascículos e datas foram conferidos na tese | OK |
| Toda aresta aponta para nós existentes | OK (0 arestas órfãs) |
| Todo evidence_id aponta para uma evidência existente | OK (0 referências órfãs) |
| Toda afirmação documentada possui evidência paginada | OK |
| Hipóteses e inferências estão visualmente distinguíveis de fatos | OK (via `status_epistemologico`) |
| Fontes declaradas problemáticas estão separadas de fontes originais identificadas | OK (`FonteDeclarada` vs `PUBLICADA_ORIGINALMENTE_EM`) |
| Obras serializadas preservam todas as partes | OK (Esboços Sicilianos: n.31-34) |
| Nenhuma rota de tradução direta é afirmada sem prova explícita | OK (usado `RELACAO_DE_DEPENDENCIA_TEXTUAL` com qualificador) |
| O README explica como os dois grafos serão consumidos por HTML estático | OK (seção 7) |

## 10. Lacunas reais que permanecem abertas

1. **O Testamento** — original não localizado; atribuição a George Crabbe não confirmada nem negada; fonte declarada (Crabbe's Posthumous Works) inexistente.
2. **O Livro da Vida** — original não localizado; fonte declarada (Retrospective Review) problemática.
3. **O Sedutor** — tese não identifica título, veículo ou data de publicação original do texto de Washington Irving.
4. **Sicilian Facts** — tese não fornece data específica de publicação em The Metropolitan.
5. **Edward D. Baynes** — sem verbete no Anexo 3; apenas menção no corpo do texto.
6. **Redatores do Gabinete de Leitura** — a tese afirma: "Não se pode saber com certeza quem eram os redatores do Gabinete de Leitura". A modelagem usa `COLABORA_COM` (não `REDIGE`) com observação explicando que Josino, Justiniano e Firmino são prováveis (mas não confirmados) redatores.
7. **Rota tradutória exata** — a tese demonstra comparação mas não afirma rota direta do inglês ou via francês, exceto para o caso negativo de Costumes Ingleses.
8. **Tradutor(es)** — em nenhum dos dez textos o tradutor é identificado; todos os atributos `tradutor` são `null`.

## 11. Fonte primária

```
SOARES, Maria Angélica Lau Pereira. Visão da Modernidade: A Presença
Britânica no Gabinete de Leitura (1837-1838). 209f. Dissertação
(Mestrado em Estudos Lingüísticos e Literários em Inglês) —
Universidade de São Paulo, São Paulo, 2006.
Orientadora: Sandra Guardini Teixeira Vasconcelos.
```

Arquivo: `TESE_MARIA_ANGELICA_LAU_PEREIRA_SOARES.pdf` (209 páginas).

## 12. Data e versão

- Data de geração: 2026-08-14
- Versão do corpus: 1.1.0 (após 4 ajustes de revisão)
- Versão do grafo contextual: 2.0
- Versão do grafo de proveniência: 3.1 (após 4 ajustes de revisão)

## 13. Histórico de revisão (v3.0 → v3.1)

Após revisão editorial, foram aplicados quatro ajustes finais ao pacote v3.0:

1. **Offset de paginação não universal**: removida a regra `pagina_pdf = pagina_impressa + 8` como universal; substituída por um `mapeamento_verificado` que registra apenas onde o offset foi confirmado (Capítulo 6).
2. **Rebaixamento da mediação francesa individual**: para os 7 textos não-excepcionais (Uma Noite no Mar, O Livro da Vida, O Sedutor, Manuscrito, Terêncio, Álibi, Esboços Sicilianos), `mediacao_francesa.status` rebaixado de `documentado` para `inferido` com `metodo: "inferencia_por_exclusao"`. Nova aresta `TEM_VERSAO_FRANCESA_NA_REVUE` (distinta de `INTERMEDIADA_POR`) criada para registrar apenas a existência, sem afirmar rota.
3. **Rota tradutória de Costumes Ingleses**: `rota_tradutoria.status` rebaixado de `problematico` para `nao_identificado`. O que é problemático é a fonte declarada "Colburn's Magazine", não a rota em si (que permanece indeterminada, com original identificado e versão francesa descartada).
4. **Data de *The Anatomy of Drunkness***: preservada a divergência interna da tese (corpo do Cap. 6.2 registra "1824"; Anexo 3 registra "tese apresentada em 1825, publicada em 1827"). Em vez de escolher uma das datas, registrou-se a divergência nos três lugares onde a obra é mencionada.

Detalhes completos em `relatorio_divergencias.md`, seções 19-22.
