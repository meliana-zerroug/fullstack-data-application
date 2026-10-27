def test_create_item_success(client):
    response = client.post("/items", json={"titre": "Perceuse", "tarif_jour": 15.0})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1 
    assert data["titre"] == "Perceuse"
    assert data["disponible"] is True 

def test_create_item_titre_invalid(client):
    response = client.post("/items", json={"titre" : "ab", "tarif_jour": 10.0})
    assert response.status_code == 422

def test_create_item_champ_invalid(client):
    response = client.post("/items", json={"titre": "Scie", "tarif_jour": 12.0, "couleur": "rouge"})
    assert response.status_code == 422


# GET 

def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404

def test_get_item_negatif_id(client): 
    response = client.get("/items/-1")
    assert response.status_code == 422

def test_patch_delete_item(client, item):
    item_id = item["id"]
    patch_res = client.patch(f"/items/{item_id}", json={"tarif_jour": 30.0})
    assert patch_res.status_code == 200
    assert patch_res.json()["tarif_jour"] == 30.0
    assert patch_res.json()["titre"] == "Perceuse"

    del_res = client.delete(f"/items/{item_id}")
    assert del_res.status_code == 204

    get_res = client.get(f"/items/{item_id}")
    assert get_res.status_code == 404