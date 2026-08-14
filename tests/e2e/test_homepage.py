"""Smoke test da página inicial.

Verifica:
- página carrega sem erro de console
- título correto
- 4 estatísticas do hero presentes (35, 92, 10, 7)
- 5 seções principais presentes
"""
from __future__ import annotations


def test_homepage_loads_without_console_errors(page, console_errors):
    """A página inicial não deve produzir erros de console."""
    # Tira snapshot após wait (já esperado no fixture)
    page.wait_for_timeout(500)
    # Filtra erros esperados (404 favicon.ico é OK)
    real_errors = [e for e in console_errors
                   if not (isinstance(e, str) and "favicon" in e.lower())
                   and not (hasattr(e, 'text') and "favicon" in e.text.lower())]
    assert not real_errors, f"Erros de console encontrados: {[getattr(e, 'text', str(e)) for e in real_errors]}"


def test_homepage_title(page):
    assert "Gabinete de Leitura" in page.title()
    assert "Visão da Modernidade" in page.title()


def test_homepage_hero_stats(page):
    """As 4 estatísticas do hero devem estar presentes e com valores corretos."""
    stats = page.query_selector_all(".stat-num")
    assert len(stats) == 4, f"Esperado 4 estatísticas, encontrado {len(stats)}"
    values = [s.text_content().strip() for s in stats]
    # Após animação, valores devem chegar aos alvos
    page.wait_for_timeout(1500)
    values = [s.text_content().strip() for s in stats]
    assert values == ["35", "92", "10", "7"], f"Estatísticas esperadas [35,92,10,7], encontradas {values}"


def test_homepage_has_five_main_sections(page):
    """As 5 seções principais devem estar presentes."""
    sections = page.query_selector_all("section.section, section.hero")
    # hero + 4 sections (periodico, narrativas, laboratorio, pesquisa)
    assert len(sections) >= 5, f"Esperado ≥5 seções, encontrado {len(sections)}"


def test_homepage_nav_has_links(page):
    """A navegação deve ter os links das seções principais."""
    nav_links = page.query_selector_all(".site-nav a")
    assert len(nav_links) >= 5, f"Esperado ≥5 links, encontrado {len(nav_links)}"
    texts = [l.text_content().strip() for l in nav_links]
    assert "Início" in texts
    assert "O Periódico" in texts
    # Sprint 3 adicionou: Matriz, Trilhas, Grafo
    assert "Matriz" in texts or "Narrativas em Trânsito" in texts
    assert "Laboratório" in texts or "Laboratório de Tradução" in texts
    assert "Pesquisa" in texts


def test_state_banner_ready_or_warning(page):
    """O banner de estado deve estar hidden (ready) ou amarelo (warning), nunca error."""
    banner = page.query_selector("#state-banner")
    assert banner is not None
    classes = banner.get_attribute("class")
    assert "state-banner--error" not in classes, f"Banner de erro: {banner.text_content()}"
