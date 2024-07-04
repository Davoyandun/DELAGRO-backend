from sqlalchemy.orm import Session
from app.db.repositories.crop_repository import CropRepository
from app.schemas.crop import CropCreate, Crop
from app.db.models.crop import Crop as CropModel
from typing import List


class CreateCropUseCase:
    def __init__(self, crop_repo: CropRepository, get_product):
        self.crop_repo = crop_repo
        self.get_product = get_product

    def execute(self, crop_create: CropCreate, db: Session) -> Crop:
        try:
            db_crop = self._build_crop_model(crop_create, db)
            created_crop = self.crop_repo.create(db_crop)
            return created_crop
        except Exception as e:
            raise e

    def _build_crop_model(self, crop_create: CropCreate, db: Session) -> CropModel:
        db_crop = CropModel(name=crop_create.name, description=crop_create.description)

        db_crop.products = self.get_product(db, crop_create.product_ids)
        return db_crop


class ListCropsUseCase:
    def __init__(self, crop_repo: CropRepository):
        self.crop_repo = crop_repo

    def execute(
        self,
    ) -> List[Crop]:
        crops = self.crop_repo.get_all()

        return crops


class ListCropUseCase:
    def __init__(self, crop_repo: CropRepository):
        self.crop_repo = crop_repo

    def execute(self, crop_id: int) -> Crop:
        crop = self.crop_repo.get(crop_id)
        if not crop:
            return None
        return crop


class UpdateCropUseCase:
    def __init__(self, crop_repo: CropRepository):
        self.crop_repo = crop_repo

    def execute(self, crop_id: int, crop_create: CropCreate) -> Crop:
        try:

            updated_crop = self.crop_repo.update(crop_id, crop_create)
            return updated_crop
        except Exception as e:
            raise e


class DeleteCropUseCase:
    def __init__(self, crop_repo: CropRepository):
        self.crop_repo = crop_repo

    def execute(self, crop_id: int) -> Crop:
        crop = self.crop_repo.delete(crop_id)
        return crop
