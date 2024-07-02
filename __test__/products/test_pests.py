def test_create_pest(new_pest, test_client):
    response = test_client.post("/api/v1/pests/", json=new_pest.dict())

    assert response.status_code == 201
    assert response.json()["name"] == new_pest.name
    assert response.json()["description"] == new_pest.description


def test_create_pest_invalid(test_client):
    invalid_pest = {
        "name": "test pest",
        "description": "test description",
        "test": "invalid field",
    }

    response = test_client.post("/api/v1/pests/", json=invalid_pest)

    assert response.status_code == 422


def test_get_pest(test_client, new_pest):
    response = test_client.post("/api/v1/pests/", json=new_pest.dict())
    pest_id = response.json()["id"]

    response = test_client.get(f"/api/v1/pests/{pest_id}")

    assert response.status_code == 200
    assert response.json()["name"] == new_pest.name
    assert response.json()["description"] == new_pest.description


def test_get_pest_invalid(test_client):
    response = test_client.get("/api/v1/pests/0")

    assert response.status_code == 404


def test_get_pests(test_client, new_pest):
    test_client.post("/api/v1/pests/", json=new_pest.dict())
    test_client.post("/api/v1/pests/", json=new_pest.dict())

    response = test_client.get("/api/v1/pests/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_pest(test_client, new_pest):
    response = test_client.post("/api/v1/pests/", json=new_pest.dict())
    pest_id = response.json()["id"]

    updated_pest = {
        "name": "updated pest",
        "description": "updated description",
    }

    response = test_client.put(f"/api/v1/pests/{pest_id}", json=updated_pest)

    assert response.status_code == 200
    assert response.json()["name"] == updated_pest["name"]
    assert response.json()["description"] == updated_pest["description"]


def test_update_pest_invalid(test_client, new_pest):
    response = test_client.post("/api/v1/pests/", json=new_pest.dict())
    pest_id = response.json()["id"]

    invalid_pest = {
        "name": "updated pest",
        "description": "updated description",
        "test": "invalid field",
    }

    response = test_client.put(f"/api/v1/pests/{pest_id}", json=invalid_pest)

    assert response.status_code == 422


def test_delete_pest(test_client, new_pest):
    response = test_client.post("/api/v1/pests/", json=new_pest.dict())
    pest_id = response.json()["id"]

    response = test_client.delete(f"/api/v1/pests/{pest_id}")

    assert response.status_code == 200
    assert response.json()["id"] == pest_id


def test_delete_pest_invalid(test_client):
    response = test_client.delete("/api/v1/pests/0")

    assert response.status_code == 404