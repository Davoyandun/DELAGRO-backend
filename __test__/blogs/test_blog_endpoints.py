import pytest


def test_create_blog(new_blog, test_client):
    response = test_client.post("/api/v1/blogs/", json=new_blog.dict())

    assert response.status_code == 201
    assert response.json()["title"] == new_blog.title
    assert response.json()["content"] == new_blog.content
    assert response.json()["author"] == new_blog.author
    


def test_create_blog_invalid(test_client):
    invalid_blog = {
        "title": "test blog",
        "content": "test text",
        "author": "test author",
        "test": "invalid field",
    }

    response = test_client.post("/api/v1/blogs/", json=invalid_blog)

    assert response.status_code == 422


def test_get_blog(test_client, new_blog):
    response = test_client.post("/api/v1/blogs/", json=new_blog.dict())
    blog_id = response.json()["id"]

    response = test_client.get(f"/api/v1/blogs/{blog_id}")

    assert response.status_code == 200
    assert response.json()["title"] == new_blog.title
    assert response.json()["content"] == new_blog.content
    assert response.json()["author"] == new_blog.author


def test_get_blog_invalid(test_client):
    response = test_client.get("/api/v1/blogs/0")

    assert response.status_code == 404


def test_get_blogs(test_client, new_blog):
    test_client.post("/api/v1/blogs/", json=new_blog.dict())
    test_client.post("/api/v1/blogs/", json=new_blog.dict())

    response = test_client.get("/api/v1/blogs/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_blog(test_client, new_blog):
    response = test_client.post("/api/v1/blogs/", json=new_blog.dict())
    blog_id = response.json()["id"]

    updated_blog = {
        "title": "updated blog",
        "content": "updated text",
        "author": "updated author",
        "img_url": "updated image",
    }

    response = test_client.put(f"/api/v1/blogs/{blog_id}", json=updated_blog)

    assert response.status_code == 200
    assert response.json()["title"] == updated_blog["title"]
    assert response.json()["content"] == updated_blog["content"]
    assert response.json()["author"] == updated_blog["author"]


def test_update_blog_invalid(test_client, new_blog):
    response = test_client.post("/api/v1/blogs/", json=new_blog.dict())
    blog_id = response.json()["id"]

    invalid_blog = {
        "title": "updated blog",
        "content": "updated text",
        "author": "updated author",
        "test": "invalid field",
    }

    response = test_client.put(f"/api/v1/blogs/{blog_id}", json=invalid_blog)

    assert response.status_code == 422


def test_delete_blog(test_client, new_blog):
    response = test_client.post("/api/v1/blogs/", json=new_blog.dict())
    blog_id = response.json()["id"]

    response = test_client.delete(f"/api/v1/blogs/{blog_id}")

    assert response.status_code == 200
    assert response.json()["id"] == blog_id


def test_delete_blog_invalid(test_client):
    response = test_client.delete("/api/v1/blogs/0")

    assert response.status_code == 404
