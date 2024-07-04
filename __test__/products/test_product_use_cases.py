import pytest
from app.db.models.product import Product as ProductModel


def test_build_product_model(create_product_use_case, product_create, mock_session):

    db_product = create_product_use_case._build_product_model(
        product_create, mock_session
    )

    assert db_product.name == product_create.name
    assert db_product.description == product_create.description
    assert db_product.price == product_create.price
    assert db_product.img_url == product_create.img_url
    assert [pest.id for pest in db_product.pests] == [1, 2]
    assert [crop.id for crop in db_product.crops] == [3, 4]


def test_create_product_use_case_execute_success(
    create_product_use_case, product_create, mock_session, mock_product_repo
):
    valid_attributes = {
        key: value
        for key, value in product_create.dict().items()
        if key in ProductModel.__table__.columns.keys()
    }
    mock_product_repo.create.return_value = ProductModel(id=1, **valid_attributes)

    result = create_product_use_case.execute(product_create, mock_session)

    assert result.id == 1
    assert result.name == product_create.name
    assert result.description == product_create.description
    assert result.price == product_create.price
    assert result.img_url == product_create.img_url


def test_create_product_use_case_execute_exception(
    create_product_use_case, product_create, mock_session, monkeypatch
):
    def mock_create(*args, **kwargs):
        raise Exception("Test Exception")
    
    monkeypatch.setattr(create_product_use_case.product_repo, "create", mock_create)

    with pytest.raises(Exception) as exc_info:
        create_product_use_case.execute(product_create, mock_session)

    assert str(exc_info.value) == "Test Exception"


def test_list_products_use_case_execute_success(
    list_products_use_case, mock_product_repo
):
    list_products_use_case.product_repo.get_filtered.return_value = [
        ProductModel(
            id=1, name="product1", description="desc1", price=10, img_url="img1"
        ),
        ProductModel(
            id=2, name="product2", description="desc2", price=20, img_url="img2"
        ),
    ]

    result = list_products_use_case.execute()

    assert len(result) == 2
    assert result[0].name == "product1"
    assert result[1].name == "product2"


def test_list_product_use_case_execute_success(
    list_product_use_case, mock_product_repo
):
    list_product_use_case.product_repo.get.return_value = ProductModel(
        id=1, name="product1", description="desc1", price=10, img_url="img1"
    )

    result = list_product_use_case.execute(1)

    assert result.id == 1
    assert result.name == "product1"
    assert result.description == "desc1"
    assert result.price == 10
    assert result.img_url == "img1"


def test_list_product_use_case_execute_not_found(
    list_product_use_case, mock_product_repo
):
    mock_product_repo.get.return_value = None

    result = list_product_use_case.execute(1)
    assert result is None


def test_update_product_use_case_execute_success(
    update_product_use_case, product_create, mock_session, mock_product_repo
):
    valid_attributes = {
        key: value
        for key, value in product_create.dict().items()
        if key in ProductModel.__table__.columns.keys()
    }
    mock_product_repo.update.return_value = ProductModel(id=1, **valid_attributes)

    result = update_product_use_case.execute(1, product_create)

    assert result.id == 1
    assert result.name == product_create.name
    assert result.description == product_create.description
    assert result.price == product_create.price
    assert result.img_url == product_create.img_url


def test_update_product_use_case_execute_exception(
    update_product_use_case, product_create, mock_session, monkeypatch
):
    def mock_update(*args, **kwargs):
        raise Exception("Test Exception")

    monkeypatch.setattr(update_product_use_case.product_repo, "update", mock_update)

    with pytest.raises(Exception) as exc_info:
        update_product_use_case.execute(1, product_create)

    assert str(exc_info.value) == "Test Exception"


def test_delete_product_use_case_execute_success(
    delete_product_use_case, mock_product_repo
):
    delete_product_use_case.execute(1)

    delete_product_use_case.product_repo.delete.assert_called_once_with(1)


def test_delete_product_use_case_execute_exception(
    delete_product_use_case, monkeypatch
):
    def mock_delete(*args, **kwargs):
        raise Exception("Test Exception")
    monkeypatch.setattr(delete_product_use_case.product_repo, "delete", mock_delete)

    with pytest.raises(Exception) as exc_info:
        delete_product_use_case.execute(1)

    assert str(exc_info.value) == "Test Exception"
