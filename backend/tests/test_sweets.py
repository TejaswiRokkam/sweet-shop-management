from fastapi.testclient import TestClient
from app.main import app


def test_get_all_sweets_empty(client):
    response = client.get("/api/sweets")
    assert response.status_code == 200
    assert response.json() == []

def test_add_sweet(client):
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

def test_search_sweets_by_name(client):
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

def test_update_sweet(client):
    # first add a sweet
    create_response = client.post(
        "/api/sweets",
        json={
            "name": "Ladoo",
            "category": "Dessert",
            "price": 10.0,
            "quantity": 30
        }
    )
    sweet_id = create_response.json()["id"]

    # now update it
    update_response = client.put(
        f"/api/sweets/{sweet_id}",
        json={
            "name": "Motichoor Ladoo",
            "category": "Dessert",
            "price": 15.0,
            "quantity": 25
        }
    )

    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Motichoor Ladoo"

def test_delete_sweet(client):
    create_response = client.post(
        "/api/sweets",
        json={
            "name": "Jalebi",
            "category": "Dessert",
            "price": 12.0,
            "quantity": 40
        }
    )
    sweet_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/sweets/{sweet_id}")
    assert delete_response.status_code == 204
