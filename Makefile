# visaomodernidade — Makefile
# Atalhos para construir, validar, testar e publicar o pacote.
# Use: `make help` para listar os alvos disponíveis.

PYTHON ?= python3
PIP ?= pip

.PHONY: help install dev-build build validate test ci clean site deploy-site

help: ## Mostra os alvos disponíveis
	@echo "visaomodernidade — alvos do Makefile"
	@echo ""
	@echo "Uso:"
	@echo "  make install        Instala dependências de execução"
	@echo "  make dev            Instala dependências de desenvolvimento"
	@echo "  make build          Regenera schemas, grafos e corpus"
	@echo "  make validate       Roda validador semântico"
	@echo "  make test           Roda testes de regressão"
	@echo "  make ci             Roda build + validate + test (espelha GitHub Actions)"
	@echo "  make site           Servidor local para o site/ (http://localhost:8000)"
	@echo "  make deploy-site    Publica o site no GitHub Pages (via actions/"
	@echo "  make clean          Remove artefatos regeneráveis"
	@echo ""

install: ## Instala dependências de execução
	$(PIP) install -r requirements.txt

dev: install ## Instala dependências de desenvolvimento
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .

build: ## Regenera schemas, corpus e grafos
	$(PYTHON) scripts/build_all.py

validate: build ## Roda validador semântico (regenera relatorio_validacao.json)
	$(PYTHON) scripts/validate.py

test: ## Roda testes de regressão
	$(PYTHON) -m pytest tests/ -v

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
	@echo "✓ Limpo"
