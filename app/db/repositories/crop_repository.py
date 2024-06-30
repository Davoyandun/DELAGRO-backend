from sqlalchemy.orm import Session
from app.db.models.crop import Crop
from app.db.repositories.base_repository import BaseRepository


class CropRepository(BaseRepository[Crop]):

    def __init__(self, db: Session):
        super().__init__(db, Crop)
