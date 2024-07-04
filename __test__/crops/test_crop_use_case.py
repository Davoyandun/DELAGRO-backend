from unittest.mock import Mock
from app.use_cases.crop_use_cases import (
    CreateCropUseCase,
    ListCropsUseCase,
    ListCropUseCase,
    UpdateCropUseCase,
    DeleteCropUseCase,
)
from app.db.models.crop import Crop as CropModel


def test_create_crop_use_case_execute_success(
    mock_crop_repo, mock_session, new_crop, create_crop_use_case
):
    valide_attributes = {
        key: value
        for key, value in new_crop.dict().items()
        if key in CropModel.__table__.columns.keys()
    }

    mock_crop_repo.create.return_value = CropModel(id=1, **valide_attributes)

    result = create_crop_use_case.execute(new_crop, mock_session)

    assert result.id == 1
    assert result.name == new_crop.name
    assert result.description == new_crop.description


def test_create_product_use_case_execute_exception(
    mock_crop_repo, mock_session, new_crop, create_crop_use_case
):
    mock_crop_repo.create.side_effect = Exception("Error")

    try:
        create_crop_use_case.execute(new_crop, mock_session)
    except Exception as e:
        assert str(e) == "Error"
    mock_crop_repo.create.assert_called_once()


def test_list_crops_use_case_execute_success(mock_crop_repo):
    use_case = ListCropsUseCase(mock_crop_repo)
    mock_crop_repo.get_all.return_value = [
        CropModel(id=1, name="Crop1"),
        CropModel(id=2, name="Crop2"),
    ]

    result = use_case.execute()

    assert len(result) == 2
    assert result[0].name == "Crop1"
    assert result[1].name == "Crop2"
    mock_crop_repo.get_all.assert_called_once()


def test_list_crops_use_case_execute_empty(mock_crop_repo):
    use_case = ListCropsUseCase(mock_crop_repo)
    mock_crop_repo.get_all.return_value = []

    result = use_case.execute()

    assert len(result) == 0
    mock_crop_repo.get_all.assert_called_once()


def test_list_crop_use_case_execute_success(mock_crop_repo):
    use_case = ListCropUseCase(mock_crop_repo)
    mock_crop_repo.get.return_value = CropModel(id=1, name="Crop1")

    result = use_case.execute(1)

    assert result.id == 1
    assert result.name == "Crop1"
    mock_crop_repo.get.assert_called_once_with(1)


def test_list_crop_use_case_execute_exception(mock_crop_repo):
    use_case = ListCropUseCase(mock_crop_repo)
    mock_crop_repo.get.side_effect = Exception("Error")

    try:
        use_case.execute(1)
    except Exception as e:
        assert str(e) == "Error"
    mock_crop_repo.get.assert_called_once_with(1)


def test_list_crop_use_case_execute_not_found(mock_crop_repo):
    use_case = ListCropUseCase(mock_crop_repo)
    mock_crop_repo.get.return_value = None

    result = use_case.execute(1)

    assert result is None
    mock_crop_repo.get.assert_called_once_with(1)


def test_update_crop_use_case_execute_success(
    mock_crop_repo,
    new_crop,
):
    use_case = UpdateCropUseCase(mock_crop_repo)
    valide_attributes = {
        key: value
        for key, value in new_crop.dict().items()
        if key in CropModel.__table__.columns.keys()
    }
    mock_crop_repo.update.return_value = CropModel(id=1, **valide_attributes)

    result = use_case.execute(1, new_crop)

    assert result.id == 1
    assert result.name == new_crop.name
    assert result.description == new_crop.description
    mock_crop_repo.update.assert_called_once_with(1, new_crop)


def test_update_crop_use_case_execute_exception(
    mock_crop_repo,
    new_crop,
):
    use_case = UpdateCropUseCase(mock_crop_repo)
    mock_crop_repo.update.side_effect = Exception("Error")

    try:
        use_case.execute(1, new_crop)
    except Exception as e:
        assert str(e) == "Error"
    mock_crop_repo.update.assert_called_once_with(1, new_crop)


def test_delete_crop_use_case_execute_success(mock_crop_repo):
    use_case = DeleteCropUseCase(mock_crop_repo)
    mock_crop_repo.delete.return_value = CropModel(id=1, name="Crop1")

    result = use_case.execute(1)

    assert result.id == 1
    assert result.name == "Crop1"
    mock_crop_repo.delete.assert_called_once_with(1)


def test_delete_crop_use_case_execute_exception(mock_crop_repo):
    use_case = DeleteCropUseCase(mock_crop_repo)
    mock_crop_repo.delete.side_effect = Exception("Error")

    try:
        use_case.execute(1)
    except Exception as e:
        assert str(e) == "Error"
    mock_crop_repo.delete.assert_called_once_with(1)
