def test_purchase_sweet_decreases_quantity(client):
    # First add a sweet
    add_response = client.post(
        "/api/sweets",
        json={
            "name": "Ladoo",
            "category": "Dessert",
            "price": 10.0,
            "quantity": 5
        }
    )
    sweet_id = add_response.json()["id"]

    # Purchase the sweet
    purchase_response = client.post(f"/api/sweets/{sweet_id}/purchase")

    assert purchase_response.status_code == 200
    assert purchase_response.json()["quantity"] == 4
