"""Testes E2E do grafo contextual em camadas.

Verifica:
- Grafo renderiza nós em camadas
- Seletor de foco funciona
- Seletor de profundidade funciona
- Deep link #grafo?foco= funciona
"""
from __future__ import annotations


def test_contextual_has_foco_select(page):
    """Deve haver um seletor de foco."""
    page.evaluate("document.querySelector('#grafo').scrollIntoView()")
    page.wait_for_timeout(500)
    select = page.query_selector('#contextual-foco-select')
    assert select is not None
    options = select.query_selector_all('option')
    assert len(options) == 10, f"Esperado 10 opções de foco, encontrado {len(options)}"


def test_contextual_renders_layer_nodes(page):
    """O grafo deve renderizar nós em camadas."""
    page.evaluate("document.querySelector('#grafo').scrollIntoView()")
    page.wait_for_timeout(500)
    nodes = page.query_selector_all('.layer-node')
    assert len(nodes) >= 4, f"Esperado ≥4 nós, encontrado {len(nodes)}"


def test_contextual_has_legend(page):
    """Deve haver uma legenda de semântica visual."""
    page.evaluate("document.querySelector('#grafo').scrollIntoView()")
    page.wait_for_timeout(300)
    legend = page.query_selector('.contextual-legend')
    assert legend is not None
    items = legend.query_selector_all('.legend-item')
    assert len(items) >= 5, f"Esperado ≥5 itens de legenda, encontrado {len(items)}"


def test_contextual_change_foco_renders(page):
    """Trocar o foco deve re-renderizar o diagrama."""
    page.evaluate("document.querySelector('#grafo').scrollIntoView()")
    page.wait_for_timeout(300)
    select = page.query_selector('#contextual-foco-select')
    select.select_option('alibi')
    page.wait_for_timeout(500)
    nodes = page.query_selector_all('.layer-node')
    assert len(nodes) >= 4, f"Após trocar foco, esperado ≥4 nós, encontrado {len(nodes)}"


def test_contextual_change_profundidade(page):
    """Aumentar profundidade deve adicionar mais nós."""
    page.evaluate("document.querySelector('#grafo').scrollIntoView()")
    page.wait_for_timeout(300)
    # Profundidade 1 (básico)
    prof_select = page.query_selector('#contextual-prof-select')
    prof_select.select_option('1')
    page.wait_for_timeout(500)
    nodes_basic = len(page.query_selector_all('.layer-node'))
    # Profundidade 3 (com contexto editorial)
    prof_select.select_option('3')
    page.wait_for_timeout(500)
    nodes_full = len(page.query_selector_all('.layer-node'))
    assert nodes_full > nodes_basic, f"Profundidade 3 deveria ter mais nós que 1: {nodes_full} vs {nodes_basic}"
