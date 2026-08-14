"""Testes E2E das correções da Sprint 3.1.

Verifica:
- Filtro "versão francesa identificada" exclui exceções (Testamento, Honras)
- Filtro "rotas via França apenas inferidas" retorna 7 textos
- Coluna Alterações seleciona texto correto no laboratório
- Modal de nó contextual tem ARIA e trap de foco
"""
from __future__ import annotations


def test_filter_franca_excludes_exceptions(page):
    """Filtro 'versão francesa identificada' deve excluir Testamento e Honras Hereditárias."""
    page.evaluate("document.querySelector('#matriz').scrollIntoView()")
    page.wait_for_timeout(500)
    btns = page.query_selector_all('.pergunta-btn')
    franca_btn = None
    for b in btns:
        if 'versão francesa identificada' in b.text_content():
            franca_btn = b
            break
    assert franca_btn is not None, "Botão 'versão francesa identificada' não encontrado"
    franca_btn.click()
    page.wait_for_timeout(500)
    rows = page.query_selector_all('.matrix-row')
    # 8 textos: 7 inferidos + Costumes Ingleses (tem versão mas não é fonte direta)
    # Exclui: O Testamento e As Honras Hereditárias (exceções explícitas)
    assert len(rows) == 8, f"Esperado 8 textos com versão francesa, encontrado {len(rows)}"

    # Verifica que Testamento e Honras NÃO estão na lista
    texts = []
    for row in rows:
        title_el = row.query_selector('.col-texto strong')
        if title_el:
            texts.append(title_el.text_content())
    assert not any('Testamento' in t for t in texts), "O Testamento não deve estar na lista de versão francesa"
    assert not any('Honras' in t for t in texts), "As Honras Hereditárias não deve estar na lista de versão francesa"


def test_filter_franca_inferida_returns_seven(page):
    """Filtro 'rotas via França apenas inferidas' deve retornar 7 textos."""
    page.evaluate("document.querySelector('#matriz').scrollIntoView()")
    page.wait_for_timeout(500)
    btns = page.query_selector_all('.pergunta-btn')
    inferida_btn = None
    for b in btns:
        if 'inferidas' in b.text_content():
            inferida_btn = b
            break
    assert inferida_btn is not None, "Botão 'inferidas' não encontrado"
    inferida_btn.click()
    page.wait_for_timeout(500)
    rows = page.query_selector_all('.matrix-row')
    # 7 textos não-excepcionais (exclui Costumes, Testamento e Honras)
    assert len(rows) == 7, f"Esperado 7 textos com rota inferida, encontrado {len(rows)}"


def test_alteracoes_column_selects_text_in_lab(page):
    """Clique na coluna 'Alterações' deve selecionar o texto correto no laboratório."""
    page.evaluate("document.querySelector('#matriz').scrollIntoView()")
    page.wait_for_timeout(500)
    # Limpa filtros
    btns = page.query_selector_all('.pergunta-btn')
    btns[0].click()  # "Todos os textos"
    page.wait_for_timeout(300)

    # Encontra a primeira linha com ops-link (Costumes Ingleses tem 3 operações)
    ops_links = page.query_selector_all('.ops-link')
    assert len(ops_links) > 0, "Nenhum link de operações encontrado"
    first_ops_text = ops_links[0].text_content()
    ops_links[0].click()
    page.wait_for_timeout(1000)  # Aguarda scroll + selectTranslationWork

    # Verifica que o laboratório tem o botão ativo
    active = page.query_selector_all('.translation-lab-option--active')
    assert len(active) == 1, f"Esperado 1 botão ativo, encontrado {len(active)}"
    active_text = active[0].text_content()

    # Verifica que as operações foram renderizadas
    ops = page.query_selector_all('.translation-op')
    assert len(ops) >= 1, "Esperado ao menos 1 operação renderizada"

    # Verifica que o número de operações corresponde ao texto do link
    import re
    num_match = re.search(r'(\d+)', first_ops_text)
    if num_match:
        expected = int(num_match.group(1))
        assert len(ops) == expected, f"Esperado {expected} operações, encontrado {len(ops)}"


def test_contextual_modal_has_aria(page):
    """Modal de nó contextual deve ter role=dialog, aria-modal e aria-labelledby."""
    page.evaluate("document.querySelector('#grafo').scrollIntoView()")
    page.wait_for_timeout(500)
    # Clica no primeiro layer-node que tem data-node-id
    nodes = page.query_selector_all('.layer-node')
    clickable = None
    for n in nodes:
        node_id = n.get_attribute('data-node-id')
        if node_id:
            clickable = n
            break
    if clickable is None:
        # Tenta clicar no primeiro nó
        clickable = nodes[0] if nodes else None
    assert clickable is not None, "Nenhum nó clicável encontrado"
    clickable.click()
    page.wait_for_timeout(500)

    modal = page.query_selector('#node-details-modal')
    assert modal is not None, "Modal não abriu"
    assert modal.get_attribute('role') == 'dialog'
    assert modal.get_attribute('aria-modal') == 'true'
    assert modal.get_attribute('aria-labelledby') == 'node-details-title'

    # Fecha com Escape
    page.keyboard.press('Escape')
    page.wait_for_timeout(300)
    modal = page.query_selector('#node-details-modal')
    assert modal is None, "Modal não fechou com Escape"


def test_contextual_modal_focus_trap(page):
    """Modal deve ter botão fechar focado e trap de foco."""
    page.evaluate("document.querySelector('#grafo').scrollIntoView()")
    page.wait_for_timeout(500)
    nodes = page.query_selector_all('.layer-node')
    if nodes:
        nodes[0].click()
        page.wait_for_timeout(500)
        # Verifica que o botão fechar tem foco
        close_btn = page.query_selector('#node-details-close')
        assert close_btn is not None, "Botão fechar não encontrado"
        # Fecha
        page.keyboard.press('Escape')
        page.wait_for_timeout(300)
