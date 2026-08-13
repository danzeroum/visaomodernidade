"""Testes do laboratório de tradução.

Verifica:
- 4 seletores de texto presentes
- Troca entre textos mostra operações diferentes
- Layout de 3 colunas (Original, Gabinete, Leitura da tese)
- Cada operação tem badge de status
- 7 operações totais nos 4 textos (Costumes: 3, Honras: 2, Álibi: 1, Esboços: 1)
"""
from __future__ import annotations

# (texto, número esperado de operações)
TEXTOS_LAB = [
    ("Costumes Ingleses", 3),
    ("As Honras Hereditárias", 2),
    ("Álibi", 1),
    ("Esboços Sicilianos", 1),
]


def test_translation_lab_has_four_selectors(page):
    """O laboratório deve ter 4 seletores de texto."""
    options = page.query_selector_all(".translation-lab-option")
    assert len(options) == 4, f"Esperado 4 opções, encontrado {len(options)}"
    texts = [o.text_content().strip() for o in options]
    for nome, _ in TEXTOS_LAB:
        assert nome in texts, f"Seletor '{nome}' não encontrado"


def test_translation_lab_default_shows_costumes(page):
    """Por padrão, deve mostrar as operações de Costumes Ingleses (3 ops)."""
    ops = page.query_selector_all(".translation-op")
    assert len(ops) == 3, f"Esperado 3 operações para Costumes, encontrado {len(ops)}"
    first_title = page.query_selector(".translation-op-title").text_content()
    assert "Fieldlove" in first_title or "ironia" in first_title.lower()


def test_translation_lab_layout_three_columns(page):
    """Cada operação deve ter layout de 3 colunas (Original, Gabinete, Leitura da tese)."""
    ops = page.query_selector_all(".translation-op")
    assert len(ops) >= 1
    for op in ops:
        cols = op.query_selector_all(".translation-op-col")
        assert len(cols) == 3, f"Operação deve ter 3 colunas, tem {len(cols)}"
        labels = [c.query_selector(".translation-op-col-label").text_content() for c in cols]
        assert any("Original" in l for l in labels), f"Coluna 'Original' não encontrada: {labels}"
        assert any("brasileira" in l.lower() or "Gabinete" in l for l in labels), f"Coluna 'Gabinete' não encontrada: {labels}"
        assert any("tese" in l.lower() or "Leitura" in l for l in labels), f"Coluna 'Leitura da tese' não encontrada: {labels}"


def test_translation_lab_has_flags(page):
    """Cada coluna deve ter um indicador visual (bandeira ou símbolo)."""
    flags = page.query_selector_all(".translation-op-col-label .flag")
    assert len(flags) >= 3, f"Esperado ≥3 flags, encontrado {len(flags)}"


def test_translation_lab_switch_to_honras(page):
    """Trocar para 'As Honras Hereditárias' deve mostrar 2 operações."""
    # Rola para a seção do laboratório
    page.evaluate("document.querySelector('#laboratorio').scrollIntoView()")
    page.wait_for_timeout(300)
    options = page.query_selector_all(".translation-lab-option")
    for opt in options:
        if "Honras" in opt.text_content():
            opt.click()
            page.wait_for_timeout(500)
            break
    ops = page.query_selector_all(".translation-op")
    assert len(ops) == 2, f"Esperado 2 operações para Honras, encontrado {len(ops)}"
    # Verifica título de uma das operações
    titles = [op.query_selector(".translation-op-title").text_content() for op in ops]
    assert any("gesto" in t.lower() for t in titles), f"Operação 'gesto' não encontrada em {titles}"
    assert any("espa" in t.lower() for t in titles), f"Operação 'espaço' não encontrada em {titles}"


def test_translation_lab_switch_to_alibi(page):
    """Trocar para 'Álibi' deve mostrar 1 operação sobre crítica aos irlandeses."""
    page.evaluate("document.querySelector('#laboratorio').scrollIntoView()")
    page.wait_for_timeout(300)
    options = page.query_selector_all(".translation-lab-option")
    for opt in options:
        if "Álibi" in opt.text_content():
            opt.click()
            page.wait_for_timeout(500)
            break
    ops = page.query_selector_all(".translation-op")
    assert len(ops) == 1, f"Esperado 1 operação para Álibi, encontrado {len(ops)}"
    title = page.query_selector(".translation-op-title").text_content()
    assert "irland" in title.lower(), f"Título deve mencionar irlandeses: {title}"


def test_translation_lab_switch_to_esbocos(page):
    """Trocar para 'Esboços Sicilianos' deve mostrar 1 operação sobre nota de punição moral."""
    page.evaluate("document.querySelector('#laboratorio').scrollIntoView()")
    page.wait_for_timeout(300)
    options = page.query_selector_all(".translation-lab-option")
    for opt in options:
        if "Esboços" in opt.text_content():
            opt.click()
            page.wait_for_timeout(500)
            break
    ops = page.query_selector_all(".translation-op")
    assert len(ops) == 1, f"Esperado 1 operação para Esboços, encontrado {len(ops)}"
    title = page.query_selector(".translation-op-title").text_content()
    assert "pun" in title.lower() or "moral" in title.lower(), (
        f"Título deve mencionar punição moral: {title}"
    )


def test_translation_lab_has_status_badges(page):
    """Cada operação deve ter um badge de status epistêmico."""
    ops = page.query_selector_all(".translation-op")
    for op in ops:
        badges = op.query_selector_all(".badge")
        assert len(badges) >= 1, "Operação deve ter ao menos um badge de status"


def test_translation_lab_has_evidence_with_pages(page):
    """Cada operação deve ter evidência com paginação dupla (PDF + impressa)."""
    ops = page.query_selector_all(".translation-op")
    found_evidence = False
    for op in ops:
        body = op.text_content()
        if "PDF" in body and "p." in body.lower():
            found_evidence = True
            break
    assert found_evidence, "Nenhuma operação mostra evidência com paginação PDF"
