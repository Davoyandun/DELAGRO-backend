from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_product():
    response = client.post("/api/v1/products/", json={"name": "Product1", "description": "Description of Product1"})
    assert response.status_code == 200
    assert response.json()["name"] == "Product1"

def test_read_product():
    response = client.get("/api/v1/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Product1"

def test_read_products():
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    assert len(response.json()) > 0
