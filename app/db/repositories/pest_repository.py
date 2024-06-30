from sqlalchemy.orm import Session
from app.db.models.pest import Pest
from app.db.repositories.base_repository import BaseRepository


class CropRepository(BaseRepository[Pest]):

    def __init__(self, db: Session):
        super().__init__(db, Pest)
