from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine



def setup_function():
    # This runs before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_user_registration(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword"
        }
    )

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"


def test_user_login(client):
    # First register
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword"
        }
    )

    # Then login
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
