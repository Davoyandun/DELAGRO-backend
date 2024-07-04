from sqlalchemy.orm import Session
from app.db.repositories.blog_repository import BlogRepository
from app.schemas.blog import BlogCreate, Blog
from app.db.models.blog import Blog as BlogModel
from typing import List


class CreateBlogUseCase:
    def __init__(self, blog_repo: BlogRepository):
        self.blog_repo = blog_repo

    def execute(self, blog_create: BlogCreate) -> Blog:
        try:
            db_blog = self._build_blog_model(blog_create)
            created_blog = self.blog_repo.create(db_blog)
            return created_blog
        except Exception as e:
            raise e

    def _build_blog_model(self, blog_create: BlogCreate) -> BlogModel:
        db_blog = BlogModel(
            title=blog_create.title,
            content=blog_create.content,
            author=blog_create.author,
            img_url=blog_create.img_url,
        )
        return db_blog


class ListBlogsUseCase:
    def __init__(self, blog_repo: BlogRepository):
        self.blog_repo = blog_repo

    def execute(
        self,
    ) -> List[Blog]:
        blogs = self.blog_repo.get_all()

        return blogs


class ListBlogUseCase:
    def __init__(self, blog_repo: BlogRepository):
        self.blog_repo = blog_repo

    def execute(self, blog_id: int) -> Blog:
        blog = self.blog_repo.get(blog_id)
        if not blog:
            return None
        return blog


class UpdateBlogUseCase:
    def __init__(self, blog_repo: BlogRepository):
        self.blog_repo = blog_repo

    def execute(self, blog_id: int, blog_create: BlogCreate) -> Blog:
        try:

            updated_blog = self.blog_repo.update(blog_id, blog_create)
            return updated_blog
        except Exception as e:
            raise e


class DeleteBlogUseCase:
    def __init__(self, blog_repo: BlogRepository):
        self.blog_repo = blog_repo

    def execute(self, blog_id: int) -> Blog:
        blog = self.blog_repo.delete(blog_id)
        return blog
