import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_product_success(new_product, test_client):
    response = test_client.post("/api/v1/products/", json=new_product.dict())
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == new_product.name
    assert response_data["description"] == new_product.description
    assert response_data["price"] == new_product.price
    assert response_data["img_url"] == new_product.img_url

def test_create_product_internal_server_error(new_product, monkeypatch, test_client):
    def mock_execute(*args, **kwargs):
        raise Exception("Test Exception")

    monkeypatch.setattr("app.use_cases.product_use_cases.CreateProductUseCase.execute", mock_execute)

    response = test_client.post("/api/v1/products/", json=new_product.dict())
    assert response.status_code == 500
    assert response.json()["detail"] == "Test Exception"


def test_get_product(test_client, new_product):
    response = test_client.post("/api/v1/products/", json=new_product.dict())
    product_id = response.json()["id"]

    response = test_client.get(f"/api/v1/products/{product_id}")

    assert response.status_code == 200
    assert response.json()["name"] == new_product.name
    assert response.json()["description"] == new_product.description
    assert response.json()["price"] == new_product.price
    assert response.json()["img_url"] == new_product.img_url


def test_get_product_invalid(test_client):
    response = test_client.get("/api/v1/products/0")

    assert response.status_code == 404


def test_get_products(test_client, new_product):
    test_client.post("/api/v1/products/", json=new_product.dict())
    test_client.post("/api/v1/products/", json=new_product.dict())

    response = test_client.get("/api/v1/products/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_product(test_client, new_product):
    response = test_client.post("/api/v1/products/", json=new_product.dict())
    product_id = response.json()["id"]
    updated_product = {
        "name": "updated product",
        "description": "updated description",
        "price": 20,
        "img_url": "updated image",
        "pest_ids": [],
        "crop_ids": [],
    }

    response = test_client.put(f"/api/v1/products/{product_id}", json=updated_product)

    assert response.status_code == 200
    assert response.json()["name"] == updated_product["name"]
    assert response.json()["description"] == updated_product["description"]
    assert response.json()["price"] == updated_product["price"]
    assert response.json()["img_url"] == updated_product["img_url"]


def test_update_product_invalid(test_client, new_product):
    response = test_client.post("/api/v1/products/", json=new_product.dict())
    product_id = response.json()["id"]
    updated_product = {
        "name": "updated product",
        "description": "updated description",
        "price": 20,
        "img_url": "updated image",
        "pest_ids": [],
        "crop_ids": [],
        "test": "invalid field",
    }

    response = test_client.put(f"/api/v1/products/{product_id}", json=updated_product)

    assert response.status_code == 422


def test_delete_product(test_client, new_product):
    response = test_client.post("/api/v1/products/", json=new_product.dict())
    product_id = response.json()["id"]

    response = test_client.delete(f"/api/v1/products/{product_id}")

    assert response.status_code == 200


def test_delete_product_invalid(test_client):
    response = test_client.delete("/api/v1/products/0")

    assert response.status_code == 404
