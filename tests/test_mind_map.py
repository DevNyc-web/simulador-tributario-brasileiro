"""Mapa mental (/mapa-mental): apresentação guiada por scroll. Só conteúdo e camadas; sem regra fiscal."""
import re
from pathlib import Path

import pytest

from app import create_app

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ["/", "/simulacao", "/simulacao/pf", "/simulacao/mei", "/simulacao/simples",
          "/simulacao/comparar", "/resultado", "/reforma", "/sobre", "/mapa-mental"]
VERDICT = ("melhor", "pior", "vantagem", "recomendado", "economiza", "ideal", "vencedor")


@pytest.fixture
def client():
    return create_app().test_client()


@pytest.fixture
def html(client):
    return client.get("/mapa-mental").get_data(as_text=True)


def plain(markup: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", markup))


@pytest.mark.parametrize("path", ROUTES)
def test_all_routes_still_return_200(client, path):
    assert client.get(path).status_code == 200


def test_mind_map_has_main_content(html):
    t = plain(html)
    for needle in ("Simulador Tributário Brasileiro 2026–2033", "2026", "Cálculo real", "432", "98%",
                   "TR-001", "TR-011", "Roadmap", "Limitações", "FUTURO", "Cenário acadêmico estimativo",
                   "R$ 5.175,24", "22,83%", "Não substitui orientação"):
        assert needle in t, needle


def test_path_has_17_ordered_stops(html):
    stops = re.findall(r'data-stop="(\d+)"', html)
    assert stops == [str(i) for i in range(17)]
    for n in range(17):
        assert f'id="c{n:02d}"' in html


def test_2027_2033_not_presented_as_calculated(html):
    t = plain(html).lower()
    assert "2027–2033" in t and "não há motor fiscal" in t
    assert not re.search(r"2027.{0,40}(calcul[ao]|motor real)", t.replace("não há motor fiscal", ""))


def test_limitations_and_undelivered_items_are_not_hidden(html):
    t = plain(html)
    for needle in ("Gráficos", "Diferença anual completa", "Atalho MEI → Simples", "Dados preservados entre telas",
                   "Sem Lucro Presumido", "Sem banco"):
        assert needle in t, needle


def test_roadmap_items_are_labelled_future(html):
    road = html.split('id="c15"')[1].split("</section>")[0]
    assert "FUTURO" in road and "Lucro Presumido" in road and "IA explicativa" in road


def test_figures_match_the_final_report(html):
    report = (ROOT / "docs/academic/relatorio-final.md").read_text(encoding="utf-8")
    must, should, could, wont = (int(x) for x in re.search(
        r"Must = (\d+) itens.*?Should = (\d+); Could = (\d+); Won't = (\d+)", report, re.S).groups())
    assert (must, should, could, wont) == (14, 5, 4, 5)
    assert f'aria-label="Distribuição MoSCoW: Must {must}, Should {should}, Could {could}, Won\'t {wont}"' in html
    for figure in ("432 testes", "98% de cobertura", "R$ 5.175,24", "22,83", "2,81", "3,65", "R$ 18.400,00", "R$ 6.540,00"):
        assert figure.replace("22,83", "22,8") in report or figure in report, figure


def test_no_verdict_words_and_no_navigation_buttons(html):
    words = set(re.findall(r"[a-zà-ú]+", plain(html).lower()))
    assert not words & set(VERDICT)
    assert "<button" not in html and "<select" not in html
    assert not re.search(r">\s*(próximo|anterior|avançar|voltar)\s*<", html, re.I)


def test_progress_indicator_is_not_interactive(html):
    bar = html.split('class="mm-progress"')[1].split("</header>")[0]
    assert "<a" not in bar and "<button" not in bar and 'aria-hidden="true"' in html


def test_has_visible_disclaimer_and_link_back(html):
    assert "Não substitui orientação contábil ou jurídica" in html
    assert 'href="/"' in html


def test_navigation_links_to_the_map(client):
    assert 'href="/mapa-mental"' in client.get("/").get_data(as_text=True)


JS = (ROOT / "static/js/mind-map.js").read_text(encoding="utf-8")
CODE = re.sub(r"//.*", "", JS)


def test_js_has_only_visual_logic():
    for word in ("aliquota", "alíquota", "irpf", "inss", "rbt12", "fator", "anexo", "dividend", "imposto", "tribut"):
        assert not re.search(r"\b" + word, CODE.lower()), word
    assert not re.search(r"(?<![\d.,])(50000|81000|4800000|3600000|2428|1621|8475|0[.,]28|0[.,]11|0[.,]10)(?![\d])", CODE)


def test_js_has_no_free_navigation():
    for forbidden in ("mousedown", "mousemove", "dragstart", "pointerdown", "pointermove", "touchmove",
                      "wheel", "preventDefault", "keydown", "onclick", '"click"'):
        assert forbidden not in CODE, forbidden
    assert "passive: true" in CODE


def test_js_handles_resize_reduced_motion_and_uses_raf():
    for needle in ('"resize"', '"orientationchange"', "prefers-reduced-motion", "requestAnimationFrame"):
        assert needle in CODE, needle
    assert "import " not in CODE and "fetch(" not in CODE and "XMLHttpRequest" not in CODE


def test_css_respects_reduced_motion_and_has_no_external_assets():
    css = (ROOT / "static/css/mind-map.css").read_text(encoding="utf-8")
    assert "prefers-reduced-motion: reduce" in css
    assert "http://" not in css and "https://" not in css and "url(" not in css
