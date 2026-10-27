def test_create_reservation_success(client, item):
    payload = {
        "item_id": item["id"],
        "date_debut": "2026-10-10",
        "date_fin": "2026-10-15",
    }
    response = client.post("/reservations", json=payload)
    assert response.status_code == 201
    assert response.json()["statut"] == "active"

def test_create_reservation_invalid_dates(client, item):
    payload = {
        "item_id": item["id"],
        "date_debut": "2026-10-15",
        "date_fin": "2026-10-10",
    }
    response = client.post("/reservations", json=payload)
    assert response.status_code == 422

def test_annuler_reservation(client, item):
    res = client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-10",
            "date_fin": "2026-10-15",
        },
    )
    res_id = res.json()["id"]

    cancel_res = client.post(f"/reservations/{res_id}/annuler")
    assert cancel_res.status_code == 200
    assert cancel_res.json()["statut"] == "annulee"

    cancel_again = client.post(f"/reservations/{res_id}/annuler")
    assert cancel_again.status_code == 409

def test_annuler_reservation_not_found(client):
    response = client.post("/reservations/999/annuler")
    assert response.status_code == 404