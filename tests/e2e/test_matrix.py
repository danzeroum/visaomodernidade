"""Testes E2E da matriz filtrável e busca.

Verifica:
- Matriz renderiza 10 linhas por padrão
- Perguntas narrativas filtram corretamente
- Busca com sintaxe (autor:, status:, fasciculo:) funciona
- Clique em linha abre dossiê
"""
from __future__ import annotations


def test_matrix_has_ten_rows_by_default(page):
    """A matriz deve ter 10 linhas por padrão."""
    page.evaluate("document.querySelector('#matriz').scrollIntoView()")
    page.wait_for_timeout(500)
    rows = page.query_selector_all('.matrix-row')
    assert len(rows) == 10, f"Esperado 10 linhas, encontrado {len(rows)}"


def test_matrix_has_perguntas_narrativas(page):
    """Deve haver botões de perguntas narrativas."""
    page.evaluate("document.querySelector('#matriz').scrollIntoView()")
    page.wait_for_timeout(300)
    btns = page.query_selector_all('.pergunta-btn')
    assert len(btns) >= 7, f"Esperado ≥7 botões de perguntas, encontrado {len(btns)}"


def test_matrix_filter_nao_sabemos(page):
    """Filtro 'O que ainda não sabemos?' deve reduzir a lista."""
    page.evaluate("document.querySelector('#matriz').scrollIntoView()")
    page.wait_for_timeout(300)
    # Clica no segundo botão (índice 1 = "O que ainda não sabemos?")
    btns = page.query_selector_all('.pergunta-btn')
    btns[1].click()
    page.wait_for_timeout(500)
    rows = page.query_selector_all('.matrix-row')
    # Esperado: 7 (Testamento, Livro da Vida, Sedutor, Esboços, + 3 com rota indeterminada)
    assert len(rows) < 10, f"Filtro deveria reduzir de 10; encontrado {len(rows)}"
    assert len(rows) >= 5, f"Filtro deveria manter ao menos 5; encontrado {len(rows)}"


def test_matrix_search_autor_bulwer(page):
    """Busca 'autor:bulwer' deve retornar 2 textos (Manuscrito + Honras)."""
    page.evaluate("document.querySelector('#matriz').scrollIntoView()")
    page.wait_for_timeout(300)
    # Limpa filtros
    btns = page.query_selector_all('.pergunta-btn')
    btns[0].click()  # "Todos os textos"
    page.wait_for_timeout(300)

    input_el = page.query_selector('#matrix-search-input')
    input_el.fill('autor:bulwer')
    page.wait_for_timeout(500)
    rows = page.query_selector_all('.matrix-row')
    assert len(rows) == 2, f"Esperado 2 textos de Bulwer, encontrado {len(rows)}"


def test_matrix_search_status_problematico(page):
    """Busca 'status:problematico' deve retornar textos com fonte problemática."""
    page.evaluate("document.querySelector('#matriz').scrollIntoView()")
    page.wait_for_timeout(300)
    btns = page.query_selector_all('.pergunta-btn')
    btns[0].click()  # Limpa
    page.wait_for_timeout(300)

    input_el = page.query_selector('#matrix-search-input')
    input_el.fill('status:problematico')
    page.wait_for_timeout(500)
    rows = page.query_selector_all('.matrix-row')
    # Esperado: Testamento, Livro da Vida, Costumes Ingleses (3 fontes problemáticas)
    assert len(rows) == 3, f"Esperado 3 textos com fonte problemática, encontrado {len(rows)}"


def test_matrix_click_row_opens_dossier(page):
    """Clique em uma linha da matriz deve abrir o dossiê."""
    page.evaluate("document.querySelector('#matriz').scrollIntoView()")
    page.wait_for_timeout(300)
    btns = page.query_selector_all('.pergunta-btn')
    btns[0].click()  # Limpa
    page.wait_for_timeout(300)

    rows = page.query_selector_all('.matrix-row')
    rows[0].click()
    page.wait_for_timeout(800)
    panel = page.query_selector('#dossier-panel')
    assert 'dossier-panel--open' in panel.get_attribute('class')
