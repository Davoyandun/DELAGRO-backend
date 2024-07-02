import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.product import ProductCreate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db


# Override the get_db dependency with a testing session
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def test_app():
    yield app

@pytest.fixture(scope="module")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()



# Create a new TestClient instance for each test
client = TestClient(app)

@pytest.fixture(scope="module")
def test_client():
    return client

# Create a new Product instance for each test
@pytest.fixture
def new_product():
    return ProductCreate(
        name="test product",
        description="test description",
        price=10,
        img_url="test image",
        pest_ids=[],
        crop_ids=[]
    )
