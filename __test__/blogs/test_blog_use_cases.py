from unittest.mock import Mock
import pytest
from app.use_cases.blog_use_cases import (
    ListBlogsUseCase,
    ListBlogUseCase,
    UpdateBlogUseCase,
    DeleteBlogUseCase,
)
from app.db.models.blog import Blog as BlogModel


@pytest.fixture
def valid_blog_attributes(new_blog):
    return {
        key: value
        for key, value in new_blog.dict().items()
        if key in BlogModel.__table__.columns.keys()
    }


def test_create_blog_use_case_execute_success(
    mock_blog_repo, new_blog, create_blog_use_case, valid_blog_attributes
):
    mock_blog_repo.create.return_value = BlogModel(id=1, **valid_blog_attributes)

    result = create_blog_use_case.execute(new_blog)

    assert result.id == 1
    assert result.author == new_blog.author
    assert result.content == new_blog.content


def test_create_product_use_case_execute_exception(
    mock_blog_repo, new_blog, create_blog_use_case
):
    mock_blog_repo.create.side_effect = Exception("Error")

    with pytest.raises(Exception, match="Error"):
        create_blog_use_case.execute(new_blog)

    mock_blog_repo.create.assert_called_once()


def test_list_blogs_use_case_execute_success(mock_blog_repo):
    use_case = ListBlogsUseCase(mock_blog_repo)
    mock_blog_repo.get_all.return_value = [
        BlogModel(id=1, author="Blog1"),
        BlogModel(id=2, author="Blog2"),
    ]

    result = use_case.execute()

    assert len(result) == 2
    assert result[0].author == "Blog1"
    assert result[1].author == "Blog2"
    mock_blog_repo.get_all.assert_called_once()


def test_list_blogs_use_case_execute_empty(mock_blog_repo):
    use_case = ListBlogsUseCase(mock_blog_repo)
    mock_blog_repo.get_all.return_value = []

    result = use_case.execute()

    assert len(result) == 0
    mock_blog_repo.get_all.assert_called_once()


def test_list_blog_use_case_execute_success(mock_blog_repo):
    use_case = ListBlogUseCase(mock_blog_repo)
    mock_blog_repo.get.return_value = BlogModel(id=1, author="Blog1")
    result = use_case.execute(1)

    assert result.id == 1
    assert result.author == "Blog1"

    mock_blog_repo.get.assert_called_once_with(1)


def test_list_blog_use_case_execute_exception(mock_blog_repo):
    use_case = ListBlogUseCase(mock_blog_repo)
    mock_blog_repo.get.side_effect = Exception("Error")

    with pytest.raises(Exception, match="Error"):
        use_case.execute(1)

    mock_blog_repo.get.assert_called_once_with(1)


def test_list_blog_use_case_execute_not_found(mock_blog_repo):
    use_case = ListBlogUseCase(mock_blog_repo)
    mock_blog_repo.get.return_value = None

    result = use_case.execute(1)

    assert result is None
    mock_blog_repo.get.assert_called_once_with(1)


def test_update_blog_use_case_execute_success(
    mock_blog_repo, new_blog, valid_blog_attributes
):
    use_case = UpdateBlogUseCase(mock_blog_repo)
    mock_blog_repo.update.return_value = BlogModel(id=1, **valid_blog_attributes)
    result = use_case.execute(1, new_blog)

    assert result.id == 1
    assert result.author == new_blog.author
    assert result.content == new_blog.content
    mock_blog_repo.update.assert_called_once_with(1, new_blog)


def test_update_blog_use_case_execute_exception(mock_blog_repo, new_blog):
    use_case = UpdateBlogUseCase(mock_blog_repo)
    mock_blog_repo.update.side_effect = Exception("Error")

    with pytest.raises(Exception, match="Error"):
        use_case.execute(1, new_blog)

    mock_blog_repo.update.assert_called_once_with(1, new_blog)


def test_delete_blog_use_case_execute_success(mock_blog_repo):
    use_case = DeleteBlogUseCase(mock_blog_repo)
    mock_blog_repo.delete.return_value = BlogModel(id=1, author="Blog1")

    result = use_case.execute(1)

    assert result.id == 1
    assert result.author == "Blog1"
    mock_blog_repo.delete.assert_called_once_with(1)


def test_delete_blog_use_case_execute_exception(mock_blog_repo):
    use_case = DeleteBlogUseCase(mock_blog_repo)
    mock_blog_repo.delete.side_effect = Exception("Error")

    with pytest.raises(Exception, match="Error"):
        use_case.execute(1)

    mock_blog_repo.delete.assert_called_once_with(1)
