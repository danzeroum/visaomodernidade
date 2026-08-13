"""Testes do dossiê de Costumes Ingleses.

Verifica (em poucos testes para evitar lentidão):
- Dossiê abre com título correto
- Identidade (fascículo, data, páginas)
- Original identificado (A Cockney Country-Gentleman, John Poole)
- Fonte declarada problemática (Colburn's Magazine)
- Versão francesa existe mas NÃO é fonte direta
- Rota efetiva: não identificada
- 3 operações tradutórias documentadas
- Evidências com paginação dupla
- Botão fechar e tecla ESC funcionam
"""
from __future__ import annotations


def open_costumes_dossier(page):
    """Helper: abre o dossiê de Costumes Ingleses e retorna o conteúdo do body."""
    # Fecha dossiê se estiver aberto
    panel = page.query_selector("#dossier-panel")
    if panel and "dossier-panel--open" in (panel.get_attribute("class") or ""):
        overlay = page.query_selector("#dossier-overlay")
        if overlay:
            overlay.click()
        page.wait_for_timeout(300)

    # Procura o card de Costumes Ingleses
    cards = page.query_selector_all(".text-card")
    costumes_card = None
    for card in cards:
        title = card.query_selector(".text-card-title")
        if title and "Costumes Ingleses" in title.text_content():
            costumes_card = card
            break
    assert costumes_card is not None, "Card de Costumes Ingleses não encontrado"
    costumes_card.click()
    page.wait_for_timeout(800)
    return page.query_selector(".dossier-body").text_content()


def test_dossier_costumes_full(page):
    """Teste consolidado do dossiê de Costumes Ingleses (evita múltiplas aberturas lentas)."""
    body = open_costumes_dossier(page)

    # 1. Título
    title = page.query_selector("#dossier-title").text_content()
    assert "Costumes Ingleses" in title, f"Título incorreto: {title}"

    # 2. Identidade
    assert "Gabinete de Leitura" in body, "Gabinete não encontrado"
    assert "n.30" in body, "Fascículo n.30 não encontrado"
    assert "4 mar 1838" in body.lower(), f"Data 4 mar 1838 não encontrada: body={body[:500]}"
    assert "233-236" in body.replace("–", "-").replace("—", "-"), "Páginas 233-236 não encontradas"

    # 3. Original identificado
    assert "A Cockney Country-Gentleman" in body, "Título original não encontrado"
    assert "John Poole" in body, "Autor John Poole não encontrado"

    # 4. Fonte declarada problemática
    assert "Colburn" in body, "Fonte Colburn não encontrada"
    badges_prob = page.query_selector_all(".dossier-body .badge--problematico")
    assert len(badges_prob) >= 1, "Esperado ao menos um badge problemático"

    # 5. Versão francesa NÃO é fonte direta
    assert "Le Cockney Campagnard" in body, "Versão francesa não encontrada"
    assert ("não é fonte direta" in body.lower() or
            "Não é fonte direta" in body), "Aviso 'não é fonte direta' não encontrado"

    # 6. Rota não identificada (não problemática)
    badges_nao_id = page.query_selector_all(".dossier-body .badge--nao-identificado")
    assert len(badges_nao_id) >= 1, "Esperado badge 'não identificado' para a rota"

    # 7. 3 operações tradutórias
    assert "3 operação" in body or "3 operaç" in body, "Esperado '3 operações' no body"
    assert "Atenuação da ironia sobre Fieldlove" in body, "Operação ironia não encontrada"
    assert ("Modificação na representação do trabalho" in body or
            "trabalho rural" in body.lower()), "Operação trabalho não encontrada"
    assert ("Alteração de desfecho" in body or
            "desfecho" in body.lower()), "Operação desfecho não encontrada"

    # 8. Evidências com paginação dupla
    assert "95" in body and "103" in body, "Paginação impressa 95-103 não encontrada"
    assert "PDF" in body, "Paginação PDF não encontrada"
    assert "103" in body and "111" in body, "Paginação PDF 103-111 não encontrada"


def test_dossier_close_button(page):
    """O botão de fechar dossiê deve funcionar."""
    open_costumes_dossier(page)
    panel = page.query_selector("#dossier-panel")
    assert "dossier-panel--open" in panel.get_attribute("class"), "Painel não abriu"

    close_btn = page.query_selector(".dossier-close")
    close_btn.click()
    page.wait_for_timeout(500)

    panel = page.query_selector("#dossier-panel")
    assert "dossier-panel--open" not in panel.get_attribute("class"), "Painel não fechou"


def test_dossier_escape_key(page):
    """Pressionar ESC deve fechar o dossiê."""
    open_costumes_dossier(page)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    panel = page.query_selector("#dossier-panel")
    assert "dossier-panel--open" not in panel.get_attribute("class"), "ESC não fechou o painel"
