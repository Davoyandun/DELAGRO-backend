from sqlalchemy.orm import Session
from app.db.repositories.pest_repository import PestRepository
from app.schemas.pest import PestCreate, Pest
from app.db.models.pest import Pest as PestModel
from typing import List


class CreatePestUseCase:
    def __init__(self, pest_repo: PestRepository, get_product):
        self.pest_repo = pest_repo
        self.get_product = get_product

    def execute(self, pest_create: PestCreate, db: Session) -> Pest:
        try:
            db_pest = self._build_pest_model(pest_create, db)
            created_pest = self.pest_repo.create(db_pest)
            return created_pest
        except Exception as e:
            raise e

    def _build_pest_model(self, pest_create: PestCreate, db: Session) -> PestModel:
        db_pest = PestModel(name=pest_create.name, description=pest_create.description)

        db_pest.products = self.get_product(db, pest_create.product_ids)
        return db_pest


class ListPestsUseCase:
    def __init__(self, pest_repo: PestRepository):
        self.pest_repo = pest_repo

    def execute(
        self,
    ) -> List[Pest]:
        pests = self.pest_repo.get_all()

        return pests


class ListPestUseCase:
    def __init__(self, pest_repo: PestRepository):
        self.pest_repo = pest_repo

    def execute(self, pest_id: int) -> Pest:
        pest = self.pest_repo.get(pest_id)
        if not pest:
            return None
        return pest


class UpdatePestUseCase:
    def __init__(self, pest_repo: PestRepository):
        self.pest_repo = pest_repo

    def execute(self, pest_id: int, pest_create: PestCreate) -> Pest:
        try:

            updated_pest = self.pest_repo.update(pest_id, pest_create)
            return updated_pest
        except Exception as e:
            raise e


class DeletePestUseCase:
    def __init__(self, pest_repo: PestRepository):
        self.pest_repo = pest_repo

    def execute(self, pest_id: int) -> Pest:
        pest = self.pest_repo.delete(pest_id)
        return pest
