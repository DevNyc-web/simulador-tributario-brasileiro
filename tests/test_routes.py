import pytest

from app import create_app
from src.services import simulate_transition
from src.tax_engine import calculate
from src.tax_rules import PENDING, SUPPORTED_YEARS, load_year_rules

ROUTES = [
    "/", "/simulacao", "/simulacao/pf", "/simulacao/mei", "/simulacao/simples",
    "/simulacao/comparar", "/resultado", "/reforma", "/sobre",
]


@pytest.fixture
def client():
    return create_app().test_client()


@pytest.mark.parametrize("path", ROUTES)
def test_route_returns_200(client, path):
    assert client.get(path).status_code == 200


@pytest.mark.parametrize("path", ROUTES)
def test_disclaimer_on_every_page(client, path):
    assert "Não substitui orientação contábil ou jurídica" in client.get(path).get_data(as_text=True)


def test_result_without_simulation(client):
    assert "Nenhuma simulação disponível." in client.get("/resultado").get_data(as_text=True)


def test_pending_rules_produce_no_numeric_result():
    results = simulate_transition({})
    assert len(results) == len(SUPPORTED_YEARS)
    assert all(r["status"] == PENDING and r["resultado"] is None for r in results)


@pytest.mark.parametrize("year", SUPPORTED_YEARS)
def test_rules_files_have_no_tax_data(year):
    rules = load_year_rules(year)
    assert rules["regras"] == [] and rules["status"] == PENDING
    assert calculate(rules, {})["resultado"] is None


def test_comparison_page_has_no_verdict(client):
    html = client.get("/simulacao/comparar").get_data(as_text=True).lower()
    assert not any(w in html for w in ("mais vantajos", "pior", "a melhor opção", "melhor opção"))
