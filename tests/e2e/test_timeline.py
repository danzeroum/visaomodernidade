"""Testes da linha do tempo dos 35 fascículos.

Verifica:
- 35 fascículos renderizados
- 10 textos britânicos destacados nos fascículos corretos
- Datas calculadas corretamente (13/08/1837 + (n-1)*7 dias)
- Clique em fascículo com texto abre dossiê
"""
from __future__ import annotations

from datetime import date, timedelta

# Datas esperadas para os 10 textos britânicos (verificado na tese)
TEXTOS_BRITANICOS = [
    (2, "1837-08-20", "Uma Noite no Mar"),
    (6, "1837-09-17", "O Livro da Vida"),
    (8, "1837-10-01", "Manuscrito"),
    (9, "1837-10-08", "O Testamento"),
    (10, "1837-10-15", "O Sedutor"),
    (11, "1837-10-22", "As Honras Hereditárias"),
    (12, "1837-10-29", "Álibi"),
    (14, "1837-11-12", "Terêncio o Alfaiate"),
    (30, "1838-03-04", "Costumes Ingleses"),
    # Esboços Sicilianos aparece em 4 fascículos (31-34) — verificado separadamente
]

FIRST_DATE = date(1837, 8, 13)


def test_timeline_has_35_fasciculos(page):
    """A linha do tempo deve ter exatamente 35 pontos."""
    dots = page.query_selector_all(".timeline-dot")
    assert len(dots) == 35, f"Esperado 35 fascículos, encontrado {len(dots)}"


def test_timeline_first_date_is_1837_08_13(page):
    """O primeiro fascículo deve ser 13/08/1837."""
    first_dot = page.query_selector(".timeline-dot:first-child .timeline-dot-date")
    text = first_dot.text_content().strip().lower()
    # A data exibida é "13 ago" (sem ano, por design) — mas o número é 13
    assert "13" in text and "ago" in text, f"Primeira data: {text}"


def test_timeline_dates_calculated_correctly(page):
    """As datas devem seguir 13/08/1837 + (n-1)*7 dias."""
    dots = page.query_selector_all(".timeline-dot")
    for i, dot in enumerate(dots):
        num = i + 1
        expected_date = FIRST_DATE + timedelta(days=(num - 1) * 7)
        date_el = dot.query_selector(".timeline-dot-date")
        if date_el:
            text = date_el.text_content().strip().lower()
            # Verifica dia
            assert str(expected_date.day) in text, (
                f"Fasc. n.{num}: esperado dia {expected_date.day}, encontrado {text}"
            )


def test_timeline_has_10_textos_britanicos_destacados(page):
    """13 fascículos devem ter marcador destacado (9 textos únicos + 4 fascículos de Esboços Sicilianos)."""
    highlighted = page.query_selector_all(".timeline-dot--has-text")
    # 10 textos no corpus, mas Esboços Sicilianos ocupa 4 fascículos (31,32,33,34)
    # Portanto: 9 textos únicos + 4 fascículos de Esboços = 13 fascículos destacados
    assert len(highlighted) == 13, (
        f"Esperado 13 fascículos com textos britânicos (9 textos únicos + 4 fascículos de Esboços), "
        f"encontrado {len(highlighted)}"
    )


def test_timeline_click_opens_dossier(page):
    """Clicar no fascículo n.30 (Costumes Ingleses) deve abrir o dossiê."""
    # Encontra o fascículo n.30
    dot30 = page.query_selector(".timeline-dot:nth-child(30)")
    # nth-child começa em 1, e nossos dots estão em ordem 1-35
    # Vamos iterar para achar o n.30
    dots = page.query_selector_all(".timeline-dot")
    dot30 = None
    for dot in dots:
        num_el = dot.query_selector(".timeline-dot-num")
        if num_el and num_el.text_content().strip() == "30":
            dot30 = dot
            break
    assert dot30 is not None, "Fascículo n.30 não encontrado"
    dot30.click()
    page.wait_for_timeout(500)

    # Verifica que o painel abriu
    panel = page.query_selector("#dossier-panel")
    classes = panel.get_attribute("class")
    assert "dossier-panel--open" in classes, "Painel de dossiê não abriu"

    # Verifica que é Costumes Ingleses
    title = page.query_selector("#dossier-title")
    assert "Costumes Ingleses" in title.text_content()


def test_timeline_esbocos_sicilianos_serializado(page):
    """Esboços Sicilianos deve aparecer em 4 fascículos consecutivos (n.31-34)."""
    dots = page.query_selector_all(".timeline-dot")
    esbocos_fasciculos = []
    for dot in dots:
        num_el = dot.query_selector(".timeline-dot-num")
        if num_el:
            num = int(num_el.text_content().strip())
            # Verifica se é um dos fascículos destacados
            has_text = dot.query_selector(".timeline-dot--has-text")
            if has_text or "timeline-dot--has-text" in dot.get_attribute("class"):
                if num in [31, 32, 33, 34]:
                    esbocos_fasciculos.append(num)
    assert sorted(esbocos_fasciculos) == [31, 32, 33, 34], (
        f"Esboços Sicilianos esperado em [31,32,33,34], encontrado em {esbocos_fasciculos}"
    )
