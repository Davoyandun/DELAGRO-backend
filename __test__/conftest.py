import os
import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.schemas.product import ProductCreate
from app.schemas.pest import PestCreate
from app.schemas.crop import CropCreate
from app.schemas.blog import BlogCreate
from app.db.models.product import Product as ProductModel
from app.db.models.pest import Pest as PestModel
from app.db.models.crop import Crop as CropModel
from app.db.repositories.product_repository import ProductRepository
from app.services.pest_service import get_pests
from app.services.crop_service import get_crops
from app.use_cases.product_use_cases import (
    CreateProductUseCase,
    ListProductsUseCase,
    UpdateProductUseCase,
    DeleteProductUseCase,
    ListProductUseCase,
)
from app.use_cases.crop_use_cases import (
    CreateCropUseCase,
    ListCropsUseCase,
    ListCropUseCase,
    UpdateCropUseCase,
    DeleteCropUseCase,
)
from app.use_cases.pest_use_cases import (
    CreatePestUseCase,
    ListPestsUseCase,
    ListPestUseCase,
    UpdatePestUseCase,
    DeletePestUseCase,
)
from app.use_cases.blog_use_cases import (
    CreateBlogUseCase,
    ListBlogsUseCase,
    ListBlogUseCase,
    UpdateBlogUseCase,
    DeleteBlogUseCase,
)

# Database setup
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

mock_get_pests = Mock(return_value=[])
mock_get_crops = Mock(return_value=[])


class MockProductRepository(ProductRepository):
    def create(self, product: ProductModel):
        product.id = 1
        return product


def override_create_product_use_case():
    product_repo = MockProductRepository(None)
    return CreateProductUseCase(product_repo, mock_get_pests, mock_get_crops)


# Fixtures
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


@pytest.fixture
def product_create():
    return ProductCreate(
        name="test product",
        description="test description",
        price=10,
        img_url="test image",
        pest_ids=[1, 2],
        crop_ids=[3, 4],
    )


@pytest.fixture
def mock_session():
    return Mock(spec=Session)


@pytest.fixture
def mock_product_repo():
    return Mock(spec=ProductRepository)


@pytest.fixture
def mock_get_pests():
    return Mock(
        return_value=[
            PestModel(id=1, name="pest1", description="desc1"),
            PestModel(id=2, name="pest2", description="desc2"),
        ]
    )


@pytest.fixture
def mock_get_product():
    return Mock(
        return_value=[
            ProductModel(id=1, name="product1", description="desc1"),
            ProductModel(id=2, name="product2", description="desc2"),
        ]
    )


@pytest.fixture
def mock_get_crops():
    return Mock(
        return_value=[
            CropModel(id=3, name="crop1", description="desc1"),
            CropModel(id=4, name="crop2", description="desc2"),
        ]
    )


@pytest.fixture
def create_product_use_case(mock_product_repo, mock_get_pests, mock_get_crops):
    return CreateProductUseCase(mock_product_repo, mock_get_pests, mock_get_crops)


@pytest.fixture
def mock_crop_repo():
    return Mock()


@pytest.fixture
def mock_blog_repo():
    return Mock()


@pytest.fixture
def mock_pest_repo():
    return Mock()


@pytest.fixture
def list_products_use_case(mock_product_repo):
    return ListProductsUseCase(mock_product_repo)


@pytest.fixture
def list_product_use_case(mock_product_repo):
    return ListProductUseCase(mock_product_repo)


@pytest.fixture
def update_product_use_case(mock_product_repo):
    return UpdateProductUseCase(mock_product_repo)


@pytest.fixture
def delete_product_use_case(mock_product_repo):
    return DeleteProductUseCase(mock_product_repo)


@pytest.fixture
def create_crop_use_case(mock_crop_repo, mock_get_product):
    return CreateCropUseCase(mock_crop_repo, mock_get_product)


@pytest.fixture
def create_pest_use_case(mock_pest_repo, mock_get_product):
    return CreatePestUseCase(mock_pest_repo, mock_get_product)


@pytest.fixture
def create_blog_use_case(mock_blog_repo):
    return CreateBlogUseCase(mock_blog_repo)


@pytest.fixture
def list_crops_use_case(mock_crop_repo):
    return ListCropsUseCase(mock_crop_repo)


@pytest.fixture
def list_pests_use_case(mock_pest_repo):
    return ListPestsUseCase(mock_pest_repo)


@pytest.fixture
def list_blogs_use_case(mock_blog_repo):
    return ListBlogsUseCase(mock_blog_repo)


@pytest.fixture
def list_pest_use_case(mock_pest_repo):
    return ListPestUseCase(mock_pest_repo)


@pytest.fixture
def list_blog_use_case(mock_blog_repo):
    return ListBlogUseCase(mock_blog_repo)


@pytest.fixture
def list_crop_use_case(mock_crop_repo):
    return ListCropUseCase(mock_crop_repo)


@pytest.fixture
def update_crop_use_case(mock_crop_repo):
    return UpdateCropUseCase(mock_crop_repo)


@pytest.fixture
def update_pest_use_case(mock_pest_repo):
    return UpdatePestUseCase(mock_pest_repo)


@pytest.fixture
def update_blog_use_case(mock_blog_repo):
    return UpdateBlogUseCase(mock_blog_repo)


@pytest.fixture
def delete_crop_use_case(mock_crop_repo):
    return DeleteCropUseCase(mock_crop_repo)


@pytest.fixture
def delete_pest_use_case(mock_pest_repo):
    return DeletePestUseCase(mock_pest_repo)


@pytest.fixture
def delete_blog_use_case(mock_blog_repo):
    return DeleteBlogUseCase(mock_blog_repo)
