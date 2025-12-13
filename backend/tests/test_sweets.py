from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_all_sweets_empty():
    response = client.get("/api/sweets")
    assert response.status_code == 200
    assert response.json() == []

def test_add_sweet():
    response = client.post(
        "/api/sweets",
        json={
            "name": "Gulab Jamun",
            "category": "Dessert",
            "price": 20.0,
            "quantity": 50
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Gulab Jamun"
    assert data["quantity"] == 50

def test_search_sweets_by_name():
    client.post(
        "/api/sweets",
        json={
            "name": "Ladoo",
            "category": "Dessert",
            "price": 10.0,
            "quantity": 20
        }
    )

    response = client.get("/api/sweets/search?name=Ladoo")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Ladoo"
