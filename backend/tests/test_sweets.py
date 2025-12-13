from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_all_sweets_empty():
    response = client.get("/api/sweets")
    assert response.status_code == 200
    assert response.json() == []
