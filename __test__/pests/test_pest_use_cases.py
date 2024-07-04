from unittest.mock import Mock
from app.use_cases.pest_use_cases import (
    CreatePestUseCase,
    ListPestUseCase,
    ListPestsUseCase,
    UpdatePestUseCase,
    DeletePestUseCase,
)
from app.db.models.pest import Pest as PestModel

def test_create_pest_use_case_execute_success(
    mock_pest_repo, mock_session, new_pest, create_pest_use_case
):
    valide_attributes = {
        key: value
        for key, value in new_pest.dict().items()
        if key in PestModel.__table__.columns.keys()
    }

    mock_pest_repo.create.return_value = PestModel(id=1, **valide_attributes)

    result = create_pest_use_case.execute(new_pest, mock_session)

    assert result.id == 1
    assert result.name == new_pest.name
    assert result.description == new_pest.description


def test_create_product_use_case_execute_exception(
    mock_pest_repo, mock_session, new_pest, create_pest_use_case
):
    mock_pest_repo.create.side_effect = Exception("Error")

    try:
        create_pest_use_case.execute(new_pest, mock_session)
    except Exception as e:
        assert str(e) == "Error"
    mock_pest_repo.create.assert_called_once()


def test_list_pests_use_case_execute_success(mock_pest_repo):
    use_case = ListPestsUseCase(mock_pest_repo)
    mock_pest_repo.get_all.return_value = [
        PestModel(id=1, name="Pest1"),
        PestModel(id=2, name="Pest2"),
    ]

    result = use_case.execute()

    assert len(result) == 2
    assert result[0].name == "Pest1"
    assert result[1].name == "Pest2"
    mock_pest_repo.get_all.assert_called_once()


def test_list_pests_use_case_execute_empty(mock_pest_repo):
    use_case = ListPestsUseCase(mock_pest_repo)
    mock_pest_repo.get_all.return_value = []

    result = use_case.execute()

    assert len(result) == 0
    mock_pest_repo.get_all.assert_called_once()


def test_list_pest_use_case_execute_success(mock_pest_repo):
    use_case = ListPestUseCase(mock_pest_repo)
    mock_pest_repo.get.return_value = PestModel(id=1, name="Pest1")

    result = use_case.execute(1)

    assert result.id == 1
    assert result.name == "Pest1"
    mock_pest_repo.get.assert_called_once_with(1)


def test_list_pest_use_case_execute_exception(mock_pest_repo):
    use_case = ListPestUseCase(mock_pest_repo)
    mock_pest_repo.get.side_effect = Exception("Error")

    try:
        use_case.execute(1)
    except Exception as e:
        assert str(e) == "Error"
    mock_pest_repo.get.assert_called_once_with(1)


def test_list_pest_use_case_execute_not_found(mock_pest_repo):
    use_case = ListPestUseCase(mock_pest_repo)
    mock_pest_repo.get.return_value = None

    result = use_case.execute(1)

    assert result is None
    mock_pest_repo.get.assert_called_once_with(1)


def test_update_pest_use_case_execute_success(
    mock_pest_repo,
    new_pest,
):
    use_case = UpdatePestUseCase(mock_pest_repo)
    valide_attributes = {
        key: value
        for key, value in new_pest.dict().items()
        if key in PestModel.__table__.columns.keys()
    }
    mock_pest_repo.update.return_value = PestModel(id=1, **valide_attributes)

    result = use_case.execute(1, new_pest)

    assert result.id == 1
    assert result.name == new_pest.name
    assert result.description == new_pest.description
    mock_pest_repo.update.assert_called_once_with(1, new_pest)


def test_update_pest_use_case_execute_exception(
    mock_pest_repo,
    new_pest,
):
    use_case = UpdatePestUseCase(mock_pest_repo)
    mock_pest_repo.update.side_effect = Exception("Error")

    try:
        use_case.execute(1, new_pest)
    except Exception as e:
        assert str(e) == "Error"
    mock_pest_repo.update.assert_called_once_with(1, new_pest)


def test_delete_pest_use_case_execute_success(mock_pest_repo):
    use_case = DeletePestUseCase(mock_pest_repo)
    mock_pest_repo.delete.return_value = PestModel(id=1, name="Pest1")

    result = use_case.execute(1)

    assert result.id == 1
    assert result.name == "Pest1"
    mock_pest_repo.delete.assert_called_once_with(1)


def test_delete_pest_use_case_execute_exception(mock_pest_repo):
    use_case = DeletePestUseCase(mock_pest_repo)
    mock_pest_repo.delete.side_effect = Exception("Error")

    try:
        use_case.execute(1)
    except Exception as e:
        assert str(e) == "Error"
    mock_pest_repo.delete.assert_called_once_with(1)
