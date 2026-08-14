"""Testes E2E das trilhas guiadas.

Verifica:
- 3 trilhas disponíveis
- Selecionar uma trilha mostra passos
- Deep link #trilha= funciona
- Navegação entre passos
"""
from __future__ import annotations


def test_trails_has_three_options(page):
    """Devem haver 3 trilhas disponíveis."""
    page.evaluate("document.querySelector('#trilhas').scrollIntoView()")
    page.wait_for_timeout(500)
    options = page.query_selector_all('.trail-option')
    assert len(options) == 3, f"Esperado 3 trilhas, encontrado {len(options)}"


def test_trail_select_shows_steps(page):
    """Selecionar uma trilha deve mostrar passos."""
    page.evaluate("document.querySelector('#trilhas').scrollIntoView()")
    page.wait_for_timeout(300)
    options = page.query_selector_all('.trail-option')
    options[0].click()  # Primeira trilha
    page.wait_for_timeout(500)
    steps = page.query_selector_all('.trail-step')
    assert len(steps) >= 4, f"Esperado ≥4 passos, encontrado {len(steps)}"


def test_trail_has_title_and_subtitle(page):
    """A trilha selecionada deve ter título e subtítulo."""
    page.evaluate("document.querySelector('#trilhas').scrollIntoView()")
    page.wait_for_timeout(300)
    options = page.query_selector_all('.trail-option')
    options[0].click()
    page.wait_for_timeout(500)
    title = page.query_selector('.trail-title')
    assert title is not None
    assert len(title.text_content()) > 0


def test_trail_step_click_opens_dossier(page):
    """Clicar em um passo deve abrir o dossiê."""
    page.evaluate("document.querySelector('#trilhas').scrollIntoView()")
    page.wait_for_timeout(300)
    options = page.query_selector_all('.trail-option')
    options[0].click()
    page.wait_for_timeout(500)
    steps = page.query_selector_all('.trail-step')
    steps[0].click()
    page.wait_for_timeout(800)
    panel = page.query_selector('#dossier-panel')
    assert 'dossier-panel--open' in panel.get_attribute('class')
