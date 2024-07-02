import pytest

def test_create_product(new_product, test_client):
    response = test_client.post("/api/v1/products/", json=new_product.dict())
    assert response.status_code == 201
    assert response.json()["name"] == new_product.name
    assert response.json()["description"] == new_product.description
    assert response.json()["price"] == new_product.price
    assert response.json()["img_url"] == new_product.img_url

def test_create_product_invalid(test_client):
    invalid_product = {
        "name": "test product",
        "description": "test description",
        "price": 10,
        "img_url": "test image",
        "test": "invalid field",
        "pest_ids": [],
        "crop_ids": []
    }
    response = test_client.post("/api/v1/products/", json=invalid_product)
    assert response.status_code == 422 

