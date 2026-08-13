# Metodologia

## Hierarquia de confiança

```
Tese (PDF)                                  >  evidência primária
Fontes e páginas explicitamente citadas     >  evidência documentada
HTML e JSONs anteriores (v2, v2.1, v2.2)   >  somente candidatos / pistas
Inferência do agente                        >  marcada como 'inferido' ou 'hipotese'
Ausência de dado                            >  marcada como 'nao_identificado'
```

Em caso de conflito entre um JSON anterior e a tese, **a tese prevalece**. As divergências foram registradas em `relatorio_divergencias.md`.

## Paginação dupla

Cada evidência armazena as duas formas de paginação quando disponíveis:

```json
{
  "pagina_pdf_inicio": 106,
  "pagina_pdf_fim": 111,
  "pagina_impressa_inicio": 98,
  "pagina_impressa_fim": 103
}
```

### Offset verificado (somente para o corpo da dissertação)

`pagina_pdf = pagina_impressa + 8` — verificado para o corpo da dissertação a partir do Capítulo 1 (Capítulo 6 começa no PDF p.84 = impressa p.76).

> ⚠️ **Não há offset universal garantido para toda a dissertação.** As páginas pré-textuais (capa, folha de rosto, resumo, abstract, sumário) seguem paginação própria e não devem ser derivadas por esta regra. Consumidores (HTML, scripts) **nunca** devem derivar uma paginação a partir da outra em tempo de execução.

## Status epistemológico

Toda afirmação, evidência, nó ou aresta usa um dos seis status abaixo:

| Status | Quando usar | Exige |
|--------|-------------|-------|
| `documentado` | Declaração explícita, transcrição, comparação ou dado verificável na tese. | `evidence_ids` não vazio |
| `identificado` | Original ou atribuição localizado e confirmado pela pesquisa apresentada na tese. | — |
| `inferido` | Conclusão derivada de evidências indiretas. | `observacao` ou `justificativa` (e `metodo` quando aplicável) |
| `hipotese` | Possibilidade acadêmica plausível, mas sem confirmação documental suficiente. | `observacao` ou `justificativa` |
| `problematico` | Fonte declarada inconsistente, original não localizado, atribuição duvidosa ou conflito documental. | — |
| `nao_identificado` | Informação ausente ou ainda não localizada. | — |

## Proibições filológicas

1. **Não invente dados.** Não troque autor, título, fascículo ou data por informação obtida fora da tese sem registrar `fonte_externa`.
2. **Não crie título inglês** quando a tese apenas identifica o autor.
3. **Não transforme fonte declarada em publicação original confirmada** — use arestas separadas (`DECLARA_COMO_FONTE` vs `PUBLICADA_ORIGINALMENTE_EM`).
4. **Não afirme tradução direta do inglês** quando a rota permanece indeterminada — use `RELACAO_DE_DEPENDENCIA_TEXTUAL` com qualificador `original_identificado_para_comparacao`.
5. **Não crie operações tradutórias** sem comparação textual explícita na tese.
6. **Não inclua biografias ou dados externos** sem `fonte_externa` e sem separá-los da evidência da tese.

## Fonte declarada ≠ fonte efetiva

Modele separadamente:

```text
Manifestação brasileira
  ├── DECLARA_COMO_FONTE → Referência declarada no Gabinete
  └── RELACAO_DE_DEPENDENCIA_TEXTUAL → Original identificado para comparação

Manifestação original
  └── PUBLICADA_EM → Periódico ou giftbook original

Versão francesa
  └── NAO_E_FONTE_DIRETA_DE → Manifestação brasileira (quando a tese descarta)

Existência de versão francesa (inferida por exclusão)
  └── TEM_VERSAO_FRANCESA_NA_REVUE → Revue Britannique
```

Exemplo conceitual (Costumes Ingleses):

```text
Costumes Ingleses (manifestação brasileira)
  ├── declarou: "Colburn's Magazine" (problemática — não existiu)
  ├── original identificado: A Cockney Country-Gentleman
  ├── publicação original: The New Monthly Magazine and Humorist, jun. 1837
  ├── versão francesa existente: Le Cockney Campagnard (Revue Britannique, fev. 1838)
  └── NÃO é fonte direta da versão brasileira (afirmação expressa da tese)
```

Não reduza essas relações a uma única aresta.

## Serialização

Uma obra publicada em vários fascículos não deve receber uma única data fictícia. Use `PublicacaoSerializada` e partes:

```text
Manifestação brasileira
  └── SERIALIZADA_EM → Publicação serializada
                              ├── PARTE_EM → Fascículo 31
                              ├── PARTE_EM → Fascículo 32
                              ├── PARTE_EM → Fascículo 33
                              └── PARTE_EM → Fascículo 34
```

## Regras de validação

O JSON Schema impõe:

1. Todos os nós têm `id`, `tipo`, `titulo` e `status_epistemologico`.
2. Todos os IDs obedecem a padrão consistente (regex).
3. Toda aresta tem `id`, `origem`, `destino`, `tipo` e `status_epistemologico`.
4. `tipo` de nó e de aresta deve pertencer ao vocabulário controlado.
5. Toda manifestação em português deve possuir data ISO e fascículo ou publicação serializada.
6. `documentado` exige pelo menos um `evidence_id`.
7. `inferido` e `hipotese` exigem `observacao`/`justificativa`.
8. Operação tradutória deve ter duas ou mais manifestações comparadas.
9. Evidência deve ter ao menos uma página PDF ou uma página impressa.

O validador semântico (`scripts/validador_semantico.py`) implementa regras adicionais que o JSON Schema não resolve sozinho — veja `modelo-de-dados.md` para a lista completa.
