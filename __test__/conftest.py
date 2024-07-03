import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.product import ProductCreate
from app.schemas.pest import PestCreate
from app.schemas.crop import CropCreate
from app.schemas.blog import BlogCreate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db


current_dir = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(current_dir, 'test.db')}"

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


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def test_client(db_session):
    client = TestClient(app)
    app.dependency_overrides[get_db] = lambda: db_session
    yield client
    app.dependency_overrides[get_db] = get_db


@pytest.fixture
def new_product():
    return ProductCreate(
        name="test product",
        description="test description",
        price=10,
        img_url="test image",
        pest_ids=[],
        crop_ids=[],
    )


@pytest.fixture
def new_pest():
    return PestCreate(name="test pest", description="test description")


@pytest.fixture
def new_crop():
    return CropCreate(name="test crop", description="test description", product_ids=[])


@pytest.fixture
def new_blog():
    return BlogCreate(
        author="test author",
        content="test text",
        title="test title",
        img_url="test image",
    )
