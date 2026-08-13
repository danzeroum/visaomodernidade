"""conftest.py para testes E2E com Playwright.

Fornece fixtures para subir um servidor HTTP local servindo o _site/
e instanciar o browser Playwright.
"""
from __future__ import annotations

import http.server
import os
import socketserver
import subprocess
import sys
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


@pytest.fixture(scope="session")
def _site_dir():
    """Retorna o caminho para _site/. Se não existir, monta a partir de site/ + data/."""
    site_dir = REPO_ROOT / "_site"
    if not site_dir.exists():
        # Monta _site/ on-the-fly
        site_dir.mkdir(parents=True, exist_ok=True)
        (site_dir / "data" / "schemas").mkdir(parents=True, exist_ok=True)
        # Copia site/
        import shutil
        for item in (REPO_ROOT / "site").iterdir():
            if item.is_dir():
                shutil.copytree(item, site_dir / item.name, dirs_exist_ok=True)
            else:
                shutil.copy2(item, site_dir / item.name)
        # Copia data/
        for json_file in (REPO_ROOT / "data").glob("*.json"):
            shutil.copy2(json_file, site_dir / "data" / json_file.name)
        for schema in (REPO_ROOT / "data" / "schemas").glob("*.json"):
            shutil.copy2(schema, site_dir / "data" / "schemas" / schema.name)
    return site_dir


@pytest.fixture(scope="session")
def http_server(_site_dir):
    """Sobe um servidor HTTP na porta 8091 servindo _site/."""
    port = 8091
    cwd = str(_site_dir)

    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port)],
        cwd=cwd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    # Aguarda o servidor subir
    time.sleep(1.0)

    # Verifica que está respondendo
    import urllib.request
    try:
        urllib.request.urlopen(f"http://localhost:{port}/", timeout=2).read()
    except Exception as e:
        proc.terminate()
        proc.wait()
        pytest.fail(f"Servidor HTTP não subiu em :{port}: {e}")

    yield f"http://localhost:{port}"

    proc.terminate()
    proc.wait()


@pytest.fixture(scope="session")
def browser_context(http_server):
    """Fixture que abre um browser Chromium headless e navega para a página inicial."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            # Captura erros de console
        )
        page = context.new_page()

        # Coleta erros de console
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg) if msg.type == "error" else None)
        page.on("pageerror", lambda err: console_errors.append(f"pageerror: {err}"))

        page.goto(http_server)
        # Aguarda o carregamento dos dados (estado ready ou warning)
        try:
            page.wait_for_function(
                "() => { const b = document.getElementById('state-banner'); return b && (b.style.display === 'none' || b.className.includes('warning')); }",
                timeout=10000
            )
        except Exception:
            pass  # Continua mesmo se timeout (testes subsequentes vão falhar)

        # Disponibiliza o contexto para os testes
        class BrowserCtx:
            def __init__(self, page, context, browser, errors, base_url):
                self.page = page
                self.context = context
                self.browser = browser
                self.console_errors = errors
                self.base_url = base_url

        yield BrowserCtx(page, context, browser, console_errors, http_server)

        context.close()
        browser.close()


@pytest.fixture
def page(browser_context):
    """Cada teste recebe a página compartilhada, com limpeza automática."""
    # Antes de cada teste, fecha qualquer dossiê aberto e rola para o topo
    p = browser_context.page
    try:
        # Fecha dossiê se estiver aberto
        panel = p.query_selector("#dossier-panel")
        if panel and "dossier-panel--open" in (panel.get_attribute("class") or ""):
            p.evaluate("""
                document.getElementById('dossier-overlay').classList.remove('dossier-overlay--open');
                document.getElementById('dossier-panel').classList.remove('dossier-panel--open');
            """)
        # Rola para o topo
        p.evaluate("window.scrollTo(0, 0)")
    except Exception:
        pass
    yield p


@pytest.fixture
def console_errors(browser_context):
    """Lista de erros de console capturados."""
    return browser_context.console_errors


@pytest.fixture
def base_url(browser_context):
    return browser_context.base_url
