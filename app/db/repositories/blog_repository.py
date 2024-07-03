from sqlalchemy.orm import Session
from app.db.models.blog import Blog
from app.db.repositories.base_repository import BaseRepository


class BlogRepository(BaseRepository[Blog]):

    def __init__(self, db: Session):
        super().__init__(db, Blog)
