"""Testes E2E do Modo Pesquisa e Exportação.

Verifica:
- Toggle entre modo Explorar/Pesquisar
- Modo Pesquisar mostra painel técnico
- Exportação CSV disponível
- Cópia de citação disponível
- Painel técnico atualiza ao abrir dossiê
"""
from __future__ import annotations


def test_mode_toggle_exists(page):
    """Deve haver um toggle de modo Explorar/Pesquisar."""
    toggle = page.query_selector('#mode-toggle')
    assert toggle is not None, "Toggle de modo não encontrado"
    btns = toggle.query_selector_all('.mode-btn')
    assert len(btns) == 2
    texts = [b.text_content().strip() for b in btns]
    assert 'Explorar' in texts
    assert 'Pesquisar' in texts


def test_default_mode_is_explorar(page):
    """Modo padrão deve ser Explorar."""
    body_classes = page.evaluate("() => document.body.className")
    assert 'mode-explorar' in body_classes, f"Esperado mode-explorar; body class = {body_classes}"


def test_switch_to_pesquisar_shows_technical_panel(page):
    """Trocar para modo Pesquisar deve mostrar o painel técnico."""
    # Clica em Pesquisar
    page.evaluate("document.querySelector('.mode-btn[data-mode=\"pesquisar\"]').click()")
    page.wait_for_timeout(500)

    # Body deve ter class mode-pesquisar
    body_classes = page.evaluate("() => document.body.className")
    assert 'mode-pesquisar' in body_classes

    # Painel técnico deve estar visível (display != none)
    panel_display = page.evaluate("() => getComputedStyle(document.getElementById('technical-panel')).display")
    assert panel_display != 'none', f"Painel técnico deveria estar visível; display = {panel_display}"


def test_switch_back_to_explorar_hides_technical(page):
    """Voltar para modo Explorar deve esconder elementos técnicos."""
    page.evaluate("document.querySelector('.mode-btn[data-mode=\"explorar\"]').click()")
    page.wait_for_timeout(500)

    body_classes = page.evaluate("() => document.body.className")
    assert 'mode-explorar' in body_classes
    assert 'mode-pesquisar' not in body_classes


def test_export_csv_button_exists(page):
    """Deve haver um botão de exportar CSV na seção matriz."""
    page.evaluate("document.querySelector('#matriz').scrollIntoView()")
    page.wait_for_timeout(300)
    btn = page.query_selector('#export-csv-btn')
    assert btn is not None, "Botão de exportar CSV não encontrado"
    assert 'CSV' in btn.text_content()


def test_copy_citation_button_exists(page):
    """Deve haver um botão de copiar citação."""
    page.evaluate("document.querySelector('#matriz').scrollIntoView()")
    page.wait_for_timeout(300)
    btn = page.query_selector('#copy-citation-btn')
    assert btn is not None, "Botão de copiar citação não encontrado"


def test_mode_preference_persists(page):
    """Preferência de modo deve persistir em localStorage."""
    page.evaluate("document.querySelector('.mode-btn[data-mode=\"pesquisar\"]').click()")
    page.wait_for_timeout(300)
    stored = page.evaluate("() => localStorage.getItem('visaomodernidade-mode')")
    assert stored == 'pesquisar', f"Esperado 'pesquisar' no localStorage; encontrado '{stored}'"

    page.evaluate("document.querySelector('.mode-btn[data-mode=\"explorar\"]').click()")
    page.wait_for_timeout(300)
    stored = page.evaluate("() => localStorage.getItem('visaomodernidade-mode')")
    assert stored == 'explorar'


def test_technical_panel_updates_on_dossier_open(page):
    """Abrir um dossiê no modo Pesquisar deve atualizar o painel técnico."""
    # Troca para modo pesquisar
    page.evaluate("document.querySelector('.mode-btn[data-mode=\"pesquisar\"]').click()")
    page.wait_for_timeout(300)

    # Abre um dossiê
    page.evaluate("document.querySelector('#matriz').scrollIntoView()")
    page.wait_for_timeout(300)
    rows = page.query_selector_all('.matrix-row')
    if rows:
        rows[0].click()
        page.wait_for_timeout(800)

        # Verifica que o painel técnico tem conteúdo
        result = page.query_selector('#technical-query-result')
        assert result is not None
        text = result.text_content()
        assert 'Corpus ID' in text or 'corpus:' in text, f"Painel técnico deveria mostrar Corpus ID; texto = {text[:200]}"
