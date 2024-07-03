import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate
from app.use_cases.product_use_cases import CreateProductUseCase
from app.db.models.product import Product as ProductModel
from app.db.models.pest import Pest as PestModel
from app.db.models.crop import Crop as CropModel
from app.db.repositories.product_repository import ProductRepository



def test_build_product_model(create_product_use_case, product_create, mock_session):

    db_product = create_product_use_case._build_product_model(product_create, mock_session)

    assert db_product.name == product_create.name
    assert db_product.description == product_create.description
    assert db_product.price == product_create.price
    assert db_product.img_url == product_create.img_url
    assert [pest.id for pest in db_product.pests] == [1, 2]
    assert [crop.id for crop in db_product.crops] == [3, 4]

def test_execute_success(create_product_use_case, product_create, mock_session, mock_product_repo):
    valid_attributes = {key: value for key, value in product_create.dict().items() if key in ProductModel.__table__.columns.keys()}
    mock_product_repo.create.return_value = ProductModel(id=1, **valid_attributes)

    result = create_product_use_case.execute(product_create, mock_session)

    assert result.id == 1
    assert result.name == product_create.name
    assert result.description == product_create.description
    assert result.price == product_create.price
    assert result.img_url == product_create.img_url

def test_execute_exception(create_product_use_case, product_create, mock_session, monkeypatch):
    def mock_create(*args, **kwargs):
        raise Exception("Test Exception")

    monkeypatch.setattr(create_product_use_case.product_repo, "create", mock_create)

    with pytest.raises(Exception) as exc_info:
        create_product_use_case.execute(product_create, mock_session)

    assert str(exc_info.value) == "Test Exception"
