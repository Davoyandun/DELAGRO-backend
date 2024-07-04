import pytest


def test_create_crop(new_crop, test_client):
    response = test_client.post("/api/v1/crops/", json=new_crop.dict())

    assert response.status_code == 201
    assert response.json()["name"] == new_crop.name
    assert response.json()["description"] == new_crop.description


def test_create_crop_invalid(test_client):
    invalid_crop = {
        "name": "test crop",
        "description": "test description",
        "test": "invalid field",
        "product_ids": [],
    }

    response = test_client.post("/api/v1/crops/", json=invalid_crop)

    assert response.status_code == 422


def test_get_crop(test_client, new_crop):
    response = test_client.post("/api/v1/crops/", json=new_crop.dict())
    crop_id = response.json()["id"]

    response = test_client.get(f"/api/v1/crops/{crop_id}")

    assert response.status_code == 200
    assert response.json()["name"] == new_crop.name
    assert response.json()["description"] == new_crop.description


def test_get_crop_invalid(test_client):
    response = test_client.get("/api/v1/crops/0")

    assert response.status_code == 404


def test_get_crops(test_client, new_crop):
    test_client.post("/api/v1/crops/", json=new_crop.dict())
    test_client.post("/api/v1/crops/", json=new_crop.dict())

    response = test_client.get("/api/v1/crops/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_crop(test_client, new_crop):
    response = test_client.post("/api/v1/crops/", json=new_crop.dict())
    crop_id = response.json()["id"]

    updated_crop = {
        "name": "updated crop",
        "description": "updated description",
    }

    response = test_client.put(f"/api/v1/crops/{crop_id}", json=updated_crop)

    assert response.status_code == 200
    assert response.json()["name"] == updated_crop["name"]
    assert response.json()["description"] == updated_crop["description"]


def test_update_crop_invalid(test_client, new_crop):
    response = test_client.post("/api/v1/crops/", json=new_crop.dict())
    crop_id = response.json()["id"]

    invalid_crop = {
        "name": "updated crop",
        "description": "updated description",
        "img_url": "updated image",
        "test": "invalid field",
    }

    response = test_client.put(f"/api/v1/crops/{crop_id}", json=invalid_crop)

    assert response.status_code == 422


def test_delete_crop(test_client, new_crop):
    response = test_client.post("/api/v1/crops/", json=new_crop.dict())
    crop_id = response.json()["id"]

    response = test_client.delete(f"/api/v1/crops/{crop_id}")

    assert response.status_code == 200
    assert response.json()["id"] == crop_id


def test_delete_crop_invalid(test_client):
    response = test_client.delete("/api/v1/crops/0")

    assert response.status_code == 404
