# Changelog

Todos os cambios notáveis neste projeto serão documentados neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere a [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.8.0] — 2026-08-14

### Adicionado (Sprint 4 — Modo Pesquisa + Exportação)

**Modo Explorar / Modo Pesquisar** (`site/assets/renderers/research-mode.js`):
- Toggle no header entre "Explorar" (didático, sem metadados técnicos) e "Pesquisar" (denso, com IDs, status, páginas, método de inferência).
- Persistência da preferência em `localStorage` (sobrevive recarga da página).
- Modo Pesquisar mostra elementos com classe `.technical-only` (painel técnico, IDs no dossiê).
- Matriz fica mais densa em modo Pesquisar (`.matrix-table--dense`).

**Exportação CSV da matriz filtrada**:
- Botão "Exportar resultados em CSV" na seção Matriz.
- Exporta apenas os textos atualmente filtrados (respeita perguntas narrativas e busca).
- Colunas: `texto, fasciculo, data, autor, original, status_original, rota, operacoes, tem_versao_francesa, rota_francesa_demonstrada`.
- Escape correto de vírgulas, aspas e quebras de linha.

**Exportação JSON do dossiê**:
- Botão "Baixar dossiê em JSON" no dossiê (visível em modo Pesquisar).
- Exporta: corpus item completo, manifestação brasileira, manifestação original, operações tradutórias, evidências, versão do pacote, fonte primária.
- Nome do arquivo: `visaomodernidade-dossie-{slug}.json`.

**Copiar citação acadêmica**:
- Botão "Copiar citação acadêmica" na barra de exportação.
- Cita: SOARES (2006) + versão do projeto + data de consulta.
- Feedback visual: "✓ Citação copiada!" por 2 segundos.

**Deep link de evidência**:
- Função `getEvidenceDeepLink(evidenceId)` gera URL permanente para qualquer evidência.
- Botão "Copiar link" ao lado de cada evidência no painel técnico.

**Painel de Consulta Técnica**:
- Disponível apenas no Modo Pesquisar, na seção "Pesquisa e Evidências".
- Mostra: Corpus ID, Work ID, fascículo(s), autor + status, original + status, fonte declarada + status, rota tradutória + status, mediação francesa (tem_versao_francesa, rota_para_brasil_demonstrada, status, método), operações tradutórias, evidências relacionadas com paginação dupla e botão copiar link.
- Atualiza automaticamente ao abrir um dossiê.

**Metadados técnicos no dossiê**:
- Em modo Pesquisar, o dossiê ganha uma seção "Metadados técnicos" com Corpus ID, Work ID, versão do pacote e botões de exportação JSON + copiar citação.

### Testes E2E novos (8 testes, total 54 E2E)

- `test_research_mode.py`:
  - `test_mode_toggle_exists`: toggle Explorar/Pesquisar presente
  - `test_default_mode_is_explorar`: modo padrão é Explorar
  - `test_switch_to_pesquisar_shows_technical_panel`: troca para Pesquisar mostra painel
  - `test_switch_back_to_explorar_hides_technical`: volta para Explorar esconde técnicos
  - `test_export_csv_button_exists`: botão CSV na seção matriz
  - `test_copy_citation_button_exists`: botão citação presente
  - `test_mode_preference_persists`: preferência salva em localStorage
  - `test_technical_panel_updates_on_dossier_open`: painel atualiza ao abrir dossiê

### Estatísticas
- **121 testes totais** (67 regressão + 54 E2E), todos passando
- 2 modos de interface (Explorar / Pesquisar)
- 3 tipos de exportação (CSV matriz, JSON dossiê, citação)
- 1 painel de consulta técnica com IDs e paginação dupla
- Deep links de evidência com copiar link

## [0.7.2] — 2026-08-14

### Corrigido (Sprint 3.2 — refinamentos de rótulos e acessibilidade)

**Refinamento metodológico: rótulo do filtro França**:
- Renomeado: "Quais textos tiveram versão francesa identificada?" → "Quais textos são associados a versões francesas?" (formulação mais precisa — evita afirmar identificação individual onde há inferência por exclusão).
- Adicionado novo filtro: "Versão francesa documentalmente localizada" (retorna apenas Costumes Ingleses — o único caso com versão individualmente identificada na tese).
- Renomeado: "Quais rotas via França são apenas inferidas?" → "Versão francesa inferida por exclusão" (mais descritivo).
- Adicionada **nota explicativa visível** abaixo da matriz quando filtros de França estão ativos, mostrando a decomposição metodológica: "1 caso com versão localizada; 7 casos inferidos por exclusão; 2 exceções explicitamente nomeadas".

**Padronização de política pushState/replaceState**:
- Regra aplicada: ações explícitas do usuário usam `history.pushState()`; inicialização/renderização/sincronização interna usam `history.replaceState()`.
- `matrix.js`: clique em pergunta narrativa usa `pushState`; digitação em busca usa `replaceState` com debounce de 500ms.
- `trails.js`: seleção de trilha usa `pushState`.
- `contextual.js`: mudança de foco/profundidade usa `pushState`.
- `app.js`: fechamento de dossiê usa `pushState` (permite Voltar reabrir o dossiê).
- Resultado: botão Voltar/Avançar do navegador agora navega por matriz filtrada → dossiê → grafo focado → Voltar → retorna à matriz com filtro preservado.

**Reforço de testes E2E do modal**:
- `test_contextual_modal_focus_trap`: agora verifica que `document.activeElement.id === 'node-details-close'` após abrir o modal (foco real, não apenas existência do botão).
- Adicionado ciclo de Tab: verifica que Tab e Shift+Tab permanecem no botão fechar (trap de foco confirmado).
- `test_contextual_modal_focus_return` (novo): verifica que após fechar com Escape, `document.activeElement.dataset.nodeId` é igual ao ID do nó que abriu o modal (retorno de foco confirmado).
- Nós do grafo agora têm `tabindex="0"`, `role="button"` e `aria-label` para serem focalizáveis por teclado.

**Acessibilidade adicional**:
- Nós do grafo contextual agora são focalizáveis por teclado (Tab) e acionáveis com Enter/Espaço.
- `showNodeDetails()` aceita parâmetro `triggerEl` explícito para garantir retorno de foco mesmo quando `document.activeElement` não é confiável.

### Testes E2E atualizados (7 testes em `test_fixes.py`, total 46 E2E)

| Teste | Verificação |
|-------|-------------|
| `test_filter_franca_excludes_exceptions` | Filtro "associados a versões francesas" exclui Testamento e Honras (8 textos) |
| `test_filter_franca_documentada_returns_one` | **NOVO** — Filtro "documentalmente localizada" retorna apenas Costumes Ingleses (1 texto) |
| `test_filter_franca_inferida_returns_seven` | Filtro "inferida por exclusão" retorna 7 textos |
| `test_alteracoes_column_selects_text_in_lab` | Coluna Alterações seleciona texto correto no laboratório |
| `test_contextual_modal_has_aria` | Modal tem `role=dialog`, `aria-modal`, `aria-labelledby`, fecha com Escape |
| `test_contextual_modal_focus_trap` | **REFORÇADO** — Verifica foco real no botão fechar + ciclo Tab/Shift+Tab |
| `test_contextual_modal_focus_return` | **NOVO** — Verifica retorno de foco ao nó após fechar modal |

### Estatísticas
- **113 testes totais** (67 regressão + 46 E2E), todos passando
- 9 perguntas narrativas na matriz (era 8)
- Política de histórico consistente: `pushState` para ações, `replaceState` para sincronização

## [0.7.1] — 2026-08-14

### Corrigido (Sprint 3.1 — refinamentos metodológicos e de UX)

**Correção crítica: filtro "passaram pela França"**:
- Adicionados campos `tem_versao_francesa` e `rota_para_brasil_demonstrada` ao `mediacao_francesa` em cada item do corpus canônico.
- `tem_versao_francesa`: `True` para os 7 textos inferidos por exclusão + Costumes Ingleses (tem versão mas não é fonte direta); `False` para O Testamento e As Honras Hereditárias (exceções explícitas).
- `rota_para_brasil_demonstrada`: `False` para todos (a tese não demonstra rota caso a caso).
- Filtro renomeado: "Quais textos tiveram versão francesa identificada?" (usa `tem_versao_francesa === true`).
- Novo filtro: "Quais rotas via França são apenas inferidas?" (usa `status === 'inferido'`).
- Schema `statusComDescricao` atualizado para permitir os novos campos.

**Correção crítica: grafo contextual deriva nós do JSON**:
- Removidos nós editoriais hardcoded (`Tipografia Commercial`, `Livraria H. & E. Laemmert`, `O Chronista`, `Revue Britannique`) de `contextual.js`.
- Agora consulta `findNode(contextual, 'tipografia:commercial')` etc. no `grafo_contextual_v2.json`.
- Subtítulos derivados dos atributos do nó (proprietário, periodo, local, papel).
- Fallback gracioso: se o nó não existir no JSON, mostra como lacuna com status `nao_identificado` e aviso no console.

**Ajuste funcional: coluna Alterações → laboratório**:
- Criada função `selectTranslationWork(workId)` exportada de `translation-lab.js`.
- `app.js` agora chama `selectTranslationWork(workId)` após scroll, selecionando automaticamente o texto correto no laboratório.
- Comportamento: clicar em "3 operações" na matriz → abre laboratório → seleciona Costumes Ingleses → mostra as 3 operações correspondentes.

**Acessibilidade: modal de nó contextual**:
- Adicionados `role="dialog"`, `aria-modal="true"`, `aria-labelledby="node-details-title"`.
- Foco automático no botão fechar ao abrir.
- Trap de foco: Tab no último elemento volta para o primeiro; Shift+Tab no primeiro vai para o último.
- Retorno de foco: ao fechar, o foco volta para o elemento que abriu o modal.
- Fechamento por Escape, clique fora e botão fechar.

**Deep links e histórico do navegador**:
- Trocado `history.replaceState()` por `history.pushState()` para criar entradas reais no histórico.
- Adicionados listeners `popstate` e `hashchange` para responder ao botão Voltar/Avançar do navegador.
- Comportamento: matriz filtrada → dossiê aberto → botão Voltar → retorna à matriz com filtro preservado.

### Testes E2E novos (5 testes, total 44 E2E)

- `test_fixes.py`:
  - `test_filter_franca_excludes_exceptions`: filtro "versão francesa identificada" exclui Testamento e Honras (8 textos)
  - `test_filter_franca_inferida_returns_seven`: filtro "rotas inferidas" retorna 7 textos
  - `test_alteracoes_column_selects_text_in_lab`: coluna Alterações seleciona texto correto no laboratório
  - `test_contextual_modal_has_aria`: modal tem `role=dialog`, `aria-modal`, `aria-labelledby`, fecha com Escape
  - `test_contextual_modal_focus_trap`: modal tem botão fechar focado

### Estatísticas
- **111 testes totais** (67 regressão + 44 E2E), todos passando
- Schema do corpus atualizado com `tem_versao_francesa` e `rota_para_brasil_demonstrada`
- Grafo contextual 100% derivado do JSON (zero nós hardcoded)

## [0.7.0] — 2026-08-14

### Adicionado (Sprint 3 — matriz, trilhas, grafo contextual, deep links)

**P1.1 — Matriz filtrável com busca por sintaxe** (`site/assets/renderers/matrix.js`):
- Tabela dos 10 textos com colunas: Texto, Fascículo, Original, Rota, Alterações, Certeza
- **7 perguntas narrativas** (filtros prontos): "O que ainda não sabemos?", "Quais textos passaram pela França?", "Onde a tradução mudou o sentido?", "Quais narrativas criticam a sociedade?", "Quais textos não têm original identificado?", "Quais textos têm fonte problemática?", "Quais textos foram serializados?"
- **Busca com sintaxe**: `status:problematico`, `autor:bulwer`, `fasciculo:30`, `fonte:revue`, `operacao:ironia`
- Colunas clicáveis: Texto→dossiê, Fascículo→timeline, Alterações→laboratório
- Navegação por teclado (j/k/Enter)
- Estado refletido na URL (`#matriz?pergunta=...&q=...`)

**P1.3 — Trilhas guiadas** (`site/assets/renderers/trails.js`):
- **3 trilhas**: "Uma história em viagem" (5 passos), "O que a tradução apaga?" (4 passos), "O que ainda não sabemos?" (4 passos)
- Cada passo abre o dossiê correspondente
- Navegação: passo anterior/próximo, abrir dossiê
- Estado na URL (`#trilha=traducao-apaga`)

**P2.1 — Grafo contextual em camadas** (`site/assets/renderers/contextual.js`):
- Rede vertical em camadas: Pessoa → Obra → Veículo britânico → Mediação → Gabinete → Fascículo
- **3 níveis de profundidade**: 1 (básico), 2 (com mediações), 3 (com contexto editorial)
- Foco em uma entidade por vez (10 opções)
- Semântica visual: linha contínua (documentado), tracejada (inferido), interrompida (lacuna), âmbar (problemático)
- Ícones: 👤 pessoa, 📖 obra, 📰 periódico
- Modal de detalhes do nó ao clicar
- Estado na URL (`#grafo?foco=alibi&profundidade=2`)

**P1.2 — Deep links**:
- `#texto=costumes-ingleses` → abre dossiê automaticamente
- `#matriz?pergunta=...&q=...` → estado da matriz
- `#trilha=traducao-apaga` → trilha ativa
- `#grafo?foco=alibi&profundidade=2` → grafo focado
- Barra de "link permanente" no rodapé com botão copiar

**Ficha de confiabilidade global**:
- Disponível na seção "Pesquisa e Evidências"
- Mostra: dados verificados, inferências, lacunas, fontes problemáticas, última validação, versão dos dados

**Acessibilidade**:
- Skip link "Pular para conteúdo principal"
- Foco visível em todos os elementos interativos
- `prefers-reduced-motion` respeitado
- Navegação por teclado na matriz (j/k/Enter)

### Testes E2E novos (15 testes adicionais, total 39 E2E)

- `test_matrix.py` (6 testes): 10 linhas padrão, perguntas narrativas, filtro "não sabemos", busca `autor:bulwer`, busca `status:problematico`, clique abre dossiê
- `test_trails.py` (4 testes): 3 trilhas, passos renderizados, título/subtítulo, clique abre dossiê
- `test_contextual.py` (5 testes): seletor de foco (10 opções), nós em camadas, legenda, troca de foco, troca de profundidade

### Estatísticas
- **106 testes totais** (67 regressão + 39 E2E), todos passando
- **8 seções** no site (Início, Periódico, Matriz, Trilhas, Narrativas, Laboratório, Grafo, Pesquisa)
- **7 perguntas narrativas** + busca com 5 operadores de sintaxe
- **3 trilhas guiadas** com 13 passos totais
- **10 opções de foco** no grafo contextual × 3 níveis de profundidade
- **4 tipos de deep link** com estado persistente na URL

## [0.6.3] — 2026-08-14

### Corrigido (sincronização README com MVP da exposição digital)

- **README.md reescrito** para refletir o estado real do `site/` (v0.5.0+):
  - Árvore do `site/` agora lista todos os 5 renderizadores (`badges.js`, `timeline.js`, `dossier.js`, `evidence.js`, `translation-lab.js`), `data-loader.js`, `icons.svg` e `app.js`.
  - `index.html` descrito como "MVP da exposição digital estática" (não mais "placeholder").
- **`make site` corrigido**: agora monta `_site/` com `data/` dentro e serve o resultado (idêntico ao artefato do GitHub Pages). Antes servia apenas `site/` sem os JSONs, fazendo `fetch('./data/*.json')` falhar.
- **Novo alvo `make site-build`**: monta `_site/` sem iniciar servidor (útil para inspeção do artefato de produção).
- **Correção de formulação sobre Crabbe**: em vez de "Crabbe's Posthumous Works inexistente", agora registra "não houve publicação com o título indicado" — formulação da própria tese (Anexo 3, verbete George Crabbe).
- **Correção de formulação sobre Retrospective Review**: agora explica que "era uma revista de resenhas críticas, não publicava narrativas completas".
- **Chave BibTeX corrigida**: `visaomodernidade_v063` (era `visaomodernidade_v040`).
- **Seção "Exposição digital" adicionada** no topo do README, com URL pública: `https://danzeroum.github.io/visaomodernidade/`.
- **Histórico de versões reorganizado**: estritamente do mais novo (v0.6.3) para o mais antigo (v0.2.2), sem misturar ordem temporal.
- **Contagem de testes padronizada**: 67 regressão + 24 E2E = 91 totais, mencionada consistentemente em README, CHANGELOG e Makefile.

### Alterado

- `Makefile` reescrito com tabs corretas (antes usava espaços, que quebravam `make`).
- `Makefile` `help` atualizado com novos alvos `site-build` e descrição de `site`.

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
