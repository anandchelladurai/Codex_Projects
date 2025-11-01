"""End-to-end test exercising FastAPI app."""
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_index_page_loads() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "UK Supermarket Price Compare" in response.text


def test_search_returns_results() -> None:
    response = client.post(
        "/search",
        data={"query": "basmati rice", "live": "false", "indian_only": "false", "sort_by": "unit"},
        headers={"HX-Request": "true"},
    )
    assert response.status_code == 200
    assert "Basmati" in response.text
    assert "Retailer" in response.text

