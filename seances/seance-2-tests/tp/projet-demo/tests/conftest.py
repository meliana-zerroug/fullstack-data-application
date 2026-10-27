import pytest 

from fastapi.testclient import TestClient

from app.main import app
from app.routers import items, reservations


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    items.FAKE_DB.clear()
    reservations.FAKE_DB.clear()
    items._next_id = 1
    reservations._next_id = 1


@pytest.fixture
def item(client):
    response = client.post(
        "/items",
        json={"titre": "Perceuse", "tarif_jour": 15.0},
    )
    assert response.status_code == 201
    return response.json()
