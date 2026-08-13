# Contribuindo para visaomodernidade

Obrigado por contribuir! Este repositório é um projeto de humanidades digitais que versiona dados acadêmicos extraídos da tese de Maria Angélica Lau Pereira Soares (2006). Para preservar a integridade filológica, siga as regras abaixo.

## Princípios filológicos (obrigatórios)

1. **A tese é a fonte de verdade primária.** Nenhum dado pode ser inventado, preenchido por plausibilidade ou derivado de fontes externas sem registro explícito em `fonte_externa`.
2. **Status epistemológico é obrigatório.** Toda afirmação, nó ou aresta deve usar um dos seis status: `documentado`, `identificado`, `inferido`, `hipotese`, `problematico`, `nao_identificado`.
3. **`documentado` exige evidência.** Todo nó/aresta com status `documentado` deve ter `evidence_ids` não vazio (exceto nós que são metadados da própria tese: `tese:soares:2006`, `pessoa:maria-angelica-soares`, etc.).
4. **`inferido` e `hipotese` exigem justificativa.** Toda afirmação com esses status deve ter `observacao` ou `justificativa` preenchida.
5. **Paginação dupla.** Toda evidência deve armazenar explicitamente `pagina_pdf_*` e `pagina_impressa_*` quando disponíveis. **Nunca** derive uma a partir da outra em tempo de execução — o offset não é universal para toda a dissertação.
6. **Fonte declarada ≠ fonte efetiva.** Modele separadamente: `DECLARA_COMO_FONTE` (o que o Gabinete diz), `RELACAO_DE_DEPENDENCIA_TEXTUAL` (original identificado para comparação), `PUBLICADA_ORIGINALMENTE_EM` (veículo original), `TEM_VERSAO_FRANCESA_NA_REVUE` (existência de versão francesa), `NAO_E_FONTE_DIRETA_DE` (afirmação negativa expressa da tese).

## Fluxo de contribuição

```text
1. Abra uma issue descrevendo a correção ou acréscimo pretendido.
2. Crie uma branch: feat/<tema> ou fix/<tema>.
3. Faça as alterações nos scripts em scripts/ — NUNCA edite data/ diretamente.
4. Rode: make build && make validate && make test
5. Verifique: git status data/ — deve mostrar mudanças (se não mostrar, os scripts não regeneraram os dados).
6. Commite os scripts E os dados regenerados.
7. Abra um pull request.
8. O CI rodará: build + validate + test + verificação de sincronia data/↔scripts.
```

## Convenção de commits

Use mensagens semânticas prefixadas por área:

```text
data: <descrição da mudança nos dados>
schema: <descrição da mudança no schema>
docs: <descrição da documentação>
feat(site): <nova funcionalidade do HTML>
fix(provenance): <correção no grafo de proveniência>
fix(corpus): <correção no corpus canônico>
test: <novo teste ou correção de teste>
ci: <mudança no GitHub Actions>
chore: <tarefas de manutenção>
```

Exemplos:

```text
data: corrigir fascículo de Costumes Ingleses (n.4 → n.30)
schema: adicionar TEM_VERSAO_FRANCESA_NA_REVUE ao vocabulário controlado
docs: documentar divergência interna sobre Anatomy of Drunkness
fix(provenance): rebaixar rota de Costumes para nao_identificado
test: adicionar regressão para Esboços Sicilianos serializado
```

## Proteção da branch main

A branch `main` está protegida. Para fazer merge:

- ✅ Pull request obrigatório
- ✅ Status check "Validate academic data" deve passar
- ✅ Branch atualizada antes do merge
- ✅ Conversas resolvidas
- ✅ Sem force push direto em main

## Adicionando um novo texto ao corpus

Se a tese identificar um novo texto britânico que deva entrar no corpus:

1. Edite `scripts/build_corpus_canonico.py` e adicione a entrada em `corpus["itens"]`.
2. Edite `src/visaomodernidade/config.py` e adicione a entrada em `CORPUS_ESPERADO`.
3. Edite `scripts/build_grafo_proveniencia.py` e adicione obra, manifestações, arestas.
4. Adicione um teste em `tests/test_corpus_canonico.py` para o novo item.
5. Rode `make build && make validate && make test`.
6. Atualize `CHANGELOG.md` e `docs/relatorio_divergencias.md` se houver correção.

## Reportando divergências

Se você encontrar divergência entre o que está no JSON e o que está na tese:

1. Abra uma issue com o título: `Divergência: <texto> — <campo>`.
2. No corpo, descreva: dado no JSON, dado na tese, página PDF e impressa, decisão sugerida.
3. Não corrija silenciosamente: toda divergência deve ser registrada em `docs/relatorio_divergencias.md`.

## Estilo de código

- Python 3.10+, type hints em todas as funções públicas.
- Docstrings em módulos e funções públicas.
- Linhas até 100 caracteres.
- `black` e `isort` recomendados (não obrigatórios no CI atual).
