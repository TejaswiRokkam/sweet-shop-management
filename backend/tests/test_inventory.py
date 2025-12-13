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

def test_restock_sweet_increases_quantity(client):
    # create sweet
    create_resp = client.post(
        "/api/sweets",
        json={
            "name": "Barfi",
            "category": "Dessert",
            "price": 15.0,
            "quantity": 5
        }
    )
    sweet_id = create_resp.json()["id"]

    # restock
    restock_resp = client.post(
        f"/api/sweets/{sweet_id}/restock",
        json={"quantity": 10}
    )

    assert restock_resp.status_code == 200
    assert restock_resp.json()["quantity"] == 15

