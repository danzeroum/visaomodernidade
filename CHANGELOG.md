# Changelog

Todos os cambios notáveis neste projeto serão documentados neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere a [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.6.2] — 2026-08-14

### Corrigido (hotfix #2 para CI)

- **Bug crítico**: o workflow do GitHub executava `python -m pytest tests/ -q` (sem `--ignore=tests/e2e`), fazendo com que os 24 testes E2E tentassem rodar sem o Chromium do Playwright instalado, resultando em 24 erros (`BrowserType.launch: Executable doesn't exist`).
- **`tests/e2e/conftest.py`**: a fixture `browser_context` agora detecta se o Chromium está disponível e **pula graciosamente** todos os testes E2E com `pytest.skip()` quando o navegador não está instalado, em vez de falhar com erro de execução.
- **`validate-data.yml` simplificado**: consolidado em **job único** que instala Playwright + Chromium antes de rodar todos os testes (regressão + E2E). Antes havia dois jobs e o primeiro não instalava Playwright.
- **Resultado no CI**: 67 passed + 24 passed (com Chromium) ou 67 passed + 24 skipped (sem Chromium). Nunca mais 24 erros.

### Comportamento de resiliência

| Cenário | Resultado |
|---------|-----------|
| CI com `playwright install chromium` | 67 passed + 24 passed (91 total) |
| CI sem `playwright install` | 67 passed + 24 skipped (0 erros) |
| Desenvolvedor sem Chromium local | 67 passed + 24 skipped |

## [0.6.1] — 2026-08-14

### Corrigido (hotfix para CI)

- **Bug crítico**: `arquivos_validados` no `relatorio_validacao.json` ainda referenciava nomes antigos de schemas (`schema_corpus_britanico_canonico.json` etc.) que foram movidos para `data/schemas/` com nomes padronizados (`corpus.schema.json` etc.) na v0.4.0. Isso causava falha no teste `test_arquivos_validados_presentes` no CI do GitHub Actions (PR #5 falhou).
- **`validador_semantico.py`**: atualizada a lista `arquivos_validados` para usar os novos nomes: `schemas/corpus.schema.json`, `schemas/contextual.schema.json`, `schemas/proveniencia.schema.json`.
- **`test_relatorio_validacao.py`**: adicionadas asserções explícitas para os 3 nomes de schemas no `arquivos_validados`.
- **`build_schemas.py`**: corrigidos os `$id` dos 3 schemas para refletir os novos caminhos (`schemas/corpus.schema.json` etc.).
- **Schemas duplicados removidos**: arquivos antigos `data/schema_*.json` foram removidos; apenas `data/schemas/*.schema.json` permanecem.

### Melhorado (robustez de CI)

- **`tests/e2e/conftest.py`**: porta do servidor HTTP agora é dinâmica (usa porta livre via `socket.bind(0)`) em vez de fixa 8091, evitando conflitos em ambientes CI.
- **`tests/e2e/conftest.py`**: servidor agora faz bind em `127.0.0.1` (mais confiável que `localhost` em alguns ambientes CI).
- **`tests/e2e/conftest.py`**: timeout do `wait_for_function` aumentado de 10s para 15s.
- **`tests/e2e/conftest.py`**: `page.goto` agora usa `wait_until="networkidle"` com timeout de 30s.
- **`tests/e2e/conftest.py`**: retry loop (5 tentativas) para aguardar servidor subir antes de prosseguir.

## [0.6.0] — 2026-08-14

### Adicionado (Sprint 2 — validação antes do deploy + smoke tests E2E)

**PR1 — Publicação segura** (`deploy-pages.yml` reescrito):
- O workflow de deploy agora valida dados acadêmicos **ANTES** de montar o artefato do Pages.
- Etapa explícita: `python scripts/build_all.py` → `python scripts/validate.py` → check `resultado == "aprovado"` (falha o deploy se não estiver aprovado).
- Etapa de verificação de sincronia `data/↔scripts` (falha se `git status data/` mostrar mudanças após o build).
- Montagem do `_site/` com `data/` dentro, permitindo `fetch('./data/*.json')` no GitHub Pages.

**PR2 — Smoke test estático no CI**:
- Etapa "Verify public assets (smoke test)" no `deploy-pages.yml`: 14 recursos públicos verificados via `curl --fail` (HTML, JS, CSS, JSONs, schemas, renderers).
- Etapa "Verify data integrity in artifact": valida que os 4 JSONs no `_site/data/` são sintaticamente válidos, validação aprovada e corpus tem 10 itens.
- Servidor HTTP local subido via `python -m http.server 8080 --directory _site` durante o CI.

**PR2b — Testes E2E com Playwright** (`tests/e2e/`):
- `test_homepage.py` (6 testes): título, hero stats (35/92/10/7), 5 seções principais, 5 links de navegação, banner de estado ready/warning, ausência de erros de console.
- `test_timeline.py` (6 testes): 35 fascículos, primeira data 13/08/1837, datas calculadas corretamente (13/08/1837 + (n-1)*7 dias), 13 fascículos britânicos destacados (9 únicos + 4 de Esboços), clique abre dossiê, Esboços Sicilianos serializado em n.31-34.
- `test_dossier_costumes.py` (3 testes consolidados): identidade (n.30, 4 mar 1838, pp. 233-236), original identificado (A Cockney Country-Gentleman, John Poole), fonte declarada problemática (Colburn's Magazine), versão francesa marcada como NÃO sendo fonte direta, rota efetiva não identificada, 3 operações tradutórias, evidências com paginação dupla (PDF 103-111 / impressa 95-103), botão fechar e tecla ESC.
- `test_translation_lab.py` (9 testes): 4 seletores, default mostra Costumes (3 ops), layout 3 colunas (Original/Gabinete/Leitura), flags visuais, troca para Honras (2 ops: gesto + espaço), Álibi (1 op: irlandeses), Esboços (1 op: punição moral), badges de status, evidências com paginação PDF.
- `tests/e2e/conftest.py`: fixtures para subir servidor HTTP local em :8091, instanciar browser Chromium headless, capturar erros de console, limpar estado entre testes.

**CI atualizado** (`validate-data.yml`):
- Novo job `e2e-smoke-tests` que depende de `academic-data-validation`.
- Instala Playwright + Chromium, monta `_site/`, roda `pytest tests/e2e/`.
- Upload de artefatos em caso de falha para debug.

### Alterado
- `requirements-dev.txt`: adicionado `playwright>=1.40,<2`.
- `pyproject.toml`: `python_files` agora inclui `*.spec.py` e `*_spec.py` (embora os arquivos finais usem `test_*.py`).
- `pyproject.toml`: adicionado `playwright>=1.40,<2` às dependências dev.

### Estatísticas
- **91 testes totais** (67 regressão + 24 E2E), todos passando.
- **14 recursos públicos** verificados via smoke test curl no CI.
- **Deploy agora falha** se validação semântica não estiver aprovada ou se data/ estiver dessincronizado.

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
