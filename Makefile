# visaomodernidade — Makefile
# Atalhos para construir, validar, testar e publicar o pacote.
# Use: `make help` para listar os alvos disponíveis.

PYTHON ?= python3
PIP ?= pip

.PHONY: help install dev build validate test test-regression test-e2e ci clean site deploy-site

help: ## Mostra os alvos disponíveis
	@echo "visaomodernidade — alvos do Makefile"
	@echo ""
	@echo "Uso:"
	@echo "  make install          Instala dependências de execução"
	@echo "  make dev              Instala dependências de desenvolvimento (inclui playwright)"
	@echo "  make build            Regenera schemas, grafos e corpus"
	@echo "  make validate         Roda validador semântico"
	@echo "  make test              Roda testes de regressão + E2E (91 testes)"
	@echo "  make test-regression  Roda apenas testes de regressão (67, sem E2E)"
	@echo "  make test-e2e         Roda apenas testes E2E com Playwright (24)"
	@echo "  make ci               Roda build + validate + test (espelha GitHub Actions)"
	@echo "  make site             Servidor local para o site/ (http://localhost:8000)"
	@echo "  make deploy-site      Publica o site no GitHub Pages (via workflow)"
	@echo "  make clean            Remove artefatos regeneráveis"
	@echo ""

install: ## Instala dependências de execução
	$(PIP) install -r requirements.txt

dev: install ## Instala dependências de desenvolvimento (inclui playwright)
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .
	@echo "Para testes E2E, instale o Chromium:"
	@echo "  python -m playwright install chromium"

build: ## Regenera schemas, corpus e grafos
	$(PYTHON) scripts/build_all.py

validate: build ## Roda validador semântico (regenera relatorio_validacao.json)
	$(PYTHON) scripts/validate.py

test: ## Roda testes de regressão (67) e E2E com Playwright (24)
	$(PYTHON) -m pytest tests/ -v --tb=short

test-regression: ## Roda apenas testes de regressão (sem E2E)
	$(PYTHON) -m pytest tests/ -v --tb=short --ignore=tests/e2e

test-e2e: ## Roda apenas testes E2E com Playwright (requer _site/ montado)
	@echo "Montando _site/..."
	@rm -rf _site && mkdir -p _site/data/schemas
	@cp -R site/. _site/
	@cp data/corpus_britanico_canonico.json data/grafo_contextual_v2.json data/grafo_proveniencia_textual_v3.json data/relatorio_validacao.json _site/data/
	@cp data/schemas/*.json _site/data/schemas/
	$(PYTHON) -m pytest tests/e2e/ -v --tb=short

ci: build validate test ## Espelha pipeline do GitHub Actions
	@echo "✓ CI local completo"

site: ## Servidor local para site/ na porta 8000
	@echo "Servindo site/ em http://localhost:8000"
	@echo "Pressione Ctrl+C para parar"
	cd site && $(PYTHON) -m http.server 8000

deploy-site: ## Publica no GitHub Pages (via workflow deploy-pages.yml)
	@echo "O deploy é feito automaticamente via GitHub Actions no push para main."
	@echo "Para forçar: git push origin main"
	@echo "Workflow: .github/workflows/deploy-pages.yml"

clean: ## Remove artefatos regeneráveis
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf _site 2>/dev/null || true
	@echo "✓ Limpo"
