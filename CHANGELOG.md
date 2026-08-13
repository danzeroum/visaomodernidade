# Changelog

Todos os cambios notáveis neste projeto serão documentados neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere a [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.5.0] — 2026-08-14

### Adicionado
- **MVP da exposição digital estática** em `site/`:
  - `index.html` — app shell completo com 5 seções (Início, O Periódico, Narrativas em Trânsito, Laboratório de Tradução, Pesquisa e Evidências).
  - `assets/styles.css` — design system sepia+papel com 6 status epistêmicos visualmente distintos (ícone+texto+cor, nunca cor sozinha).
  - `assets/app.js` — orquestrador com 4 estados (loading, ready, warning, error) que lê `relatorio_validacao.json` primeiro.
  - `assets/data-loader.js` — carrega os 4 JSONs via `fetch()` + helpers de consulta ao grafo (findNode, findEdges, findBrazilianManifestation, findOriginalManifestation, etc.).
  - `assets/icons.svg` — SVG sprite com 13 ícones (check, star, approx, hypothesis, warning, unknown, arrows, book, link, doc, periodical).
  - `assets/renderers/badges.js` — selos epistêmicos com ícone SVG + texto + cor + tooltip + `aria-label`.
  - `assets/renderers/timeline.js` — linha do tempo dos 35 fascículos com os 10 textos britânicos destacados.
  - `assets/renderers/dossier.js` — painel lateral de dossiê com diagrama de rota visual (original → fonte declarada → versão francesa → versão brasileira → rota efetiva).
  - `assets/renderers/evidence.js` — painel de evidência com paginação dupla (PDF + impressa) e citação literal.
  - `assets/renderers/translation-lab.js` — laboratório de comparação com layout 3 colunas (desktop) / vertical (mobile) para os 4 casos prioritários.
  - `site/README.md` — documentação do site.
- **Atualização do `deploy-pages.yml`**: agora monta `_site/` com `data/` dentro, permitindo `fetch('./data/*.json')` no GitHub Pages.

### Alterado
- `deploy-pages.yml` agora copia `data/*.json` e `data/schemas/` para `_site/data/` antes do deploy.
- Site agora é uma aplicação ES6 module (`<script type="module">`) com renderização client-side dos dados.

## [0.4.0] — 2026-08-14

### Adicionado
- Estrutura de pacote Python (`pyproject.toml`, `requirements.txt`, `requirements-dev.txt`) com entry points `visaomodernidade-build` e `visaomodernidade-validate`.
- Módulo `src/visaomodernidade/` com `config.py` (caminhos, constantes, vocabulário controlado) e `cli.py` (entry points).
- `scripts/build_all.py` — ponto de entrada único para regenerar todo o pacote.
- `scripts/validate.py` — ponto de entrada único para validação semântica.
- `Makefile` com alvos `install`, `dev`, `build`, `validate`, `test`, `ci`, `site`, `deploy-site`, `clean`.
- `tests/` com 67 testes de regressão cobrindo:
  - Corpus canônico (10 textos, fascículos, datas, status).
  - 4 ajustes da v3.1 (offset não universal, mediação inferida, rota de Costumes, Anatomy of Drunkness).
  - Validação de schemas Draft-07.
  - Integridade estrutural dos grafos (IDs únicos, arestas não órfãs, evidências referenciadas existem).
  - Paginação dupla com offset correto quando ambas presentes.
  - Relatório de validação (resultado aprovado, 0 erros de alta).
  - Fixtures inválidas (testes negativos).
- `.github/workflows/validate-data.yml` — CI no GitHub Actions: build + validate + test + verificação de sincronia `data/`↔scripts.
- `.github/workflows/deploy-pages.yml` — Deploy automático do `site/` no GitHub Pages.
- `CONTRIBUTING.md` — princípios filológicos, fluxo de contribuição, convenção de commits semânticos.
- `CHANGELOG.md` — este arquivo.
- `docs/metodologia.md` e `docs/modelo-de-dados.md` — documentação de metodologia e modelo de dados.
- `site/index.html`, `site/assets/styles.css`, `site/assets/app.js` — placeholder do MVP da exposição digital.
- `data/schemas/` — schemas movidos para subdiretório com nomes padronizados (`corpus.schema.json`, `contextual.schema.json`, `proveniencia.schema.json`).

### Alterado
- Schemas movidos de `data/schema_*.json` para `data/schemas/{corpus,contextual,proveniencia}.schema.json`.
- Scripts de build passam a escrever em caminhos relativos ao repositório (não mais em `/home/z/my-project/output/`).
- `$schema` do corpus atualizado para `./schemas/corpus.schema.json`.

## [0.3.1] — 2026-08-14

### Adicionado
- 4 ajustes de revisão editorial aplicados sobre a v3.0:
  1. **Offset de paginação não universal**: removida regra global `pagina_pdf = pagina_impressa + 8`; substituída por `mapeamento_verificado` que registra apenas o Capítulo 6 como seção confirmada.
  2. **Mediação francesa individual rebaixada**: para os 7 textos não-excepcionais, `mediacao_francesa.status` rebaixado de `documentado` para `inferido` com `metodo: "inferencia_por_exclusao"`. Nova aresta `TEM_VERSAO_FRANCESA_NA_REVUE` (distinta de `INTERMEDIADA_POR`) criada para registrar apenas a existência, sem afirmar rota.
  3. **Rota tradutória de Costumes Ingleses**: `rota_tradutoria.status` rebaixado de `problematico` para `nao_identificado`. O problemático é a fonte declarada "Colburn's Magazine", não a rota em si.
  4. **Divergência interna da tese sobre The Anatomy of Drunkness**: preservada sem escolher uma das datas (corpo do Cap. 6.2 registra "1824"; Anexo 3 registra "tese apresentada em 1825, publicada em 1827").

### Documentado
- 4 novas divergências (19-22) registradas em `docs/relatorio_divergencias.md`.

## [0.3.0] — 2026-08-14

### Adicionado
- Corpus canônico com 10 textos britânicos e fascículos corrigidos.
- Grafo contextual (76 nós, 65 arestas).
- Grafo de proveniência textual (108 nós, 127 arestas, 7 operações tradutórias, 5 argumentos).
- 3 JSON Schemas Draft-07 (corpus, contextual, proveniência).
- Validador semântico com 13 regras que o JSON Schema não resolve sozinho.
- 22 divergências documentadas em `docs/relatorio_divergencias.md` (vs. rascunhos v2/v2.1/v2.2).

### Corrigido (vs. rascunhos anteriores)
- 12 correções de número de fascículo/data (Costumes n.4→n.30; Testamento n.16→n.9; Livro da Vida n.18→n.6; Sedutor n.23→n.10; Terêncio n.21→n.14; Álibi n.13→n.12; Manuscrito data 01/04/1838→01/10/1837; Uma Noite no Mar n.5→n.2; Esboços n.19→serialização n.31-34).
- 2 correções de ID de pessoa (richard-harris-poole→john-poole; simon-macnish→robert-macnish).
- 5 placeholders "c1830"/"c1835" substituídos por datas precisas ou `null`.
- Remoção da manifestação inglesa fabricada de O Sedutor.
- Aresta `TRADUZIDA_DE` substituída por `RELACAO_DE_DEPENDENCIA_TEXTUAL` com qualificador.

## [0.2.2] — anterior

Rascunho com fascículos embaralhados, placeholders "c1830", manifestação inglesa fabricada de O Sedutor, aresta `TRADUZIDA_DE` indevida. Ver `docs/relatorio_divergencias.md` para detalhes.
