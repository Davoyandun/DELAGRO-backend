from typing import List
from app.db.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, Product
from app.db.models.product import Product as ProductModel
from sqlalchemy.orm import Session


class CreateProductUseCase:
    def __init__(self, product_repo: ProductRepository, get_pests, get_crops):
        self.product_repo = product_repo
        self.get_pests = get_pests
        self.get_crops = get_crops

    def execute(self, product_create: ProductCreate, db: Session) -> Product:

        try:
            db_product = self._build_product_model(product_create, db)
            created_product = self.product_repo.create(db_product)

            return created_product

        except Exception as e:
            raise e

    def _build_product_model(
        self, product_create: ProductCreate, db: Session
    ) -> ProductModel:

        db_product = ProductModel(
            name=product_create.name,
            description=product_create.description,
            price=product_create.price,
            img_url=product_create.img_url,
        )

        db_product.pests = self.get_pests(db, product_create.pest_ids)
        db_product.crops = self.get_crops(db, product_create.crop_ids)

        return db_product


class ListProductsUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self) -> List[Product]:
        products = self.product_repo.get_all()
        return products


class GetProductUseCase:
    def __init__(self, product_repo: ProductRepository, get_pests, get_crops):
        self.product_repo = product_repo
        self.get_pests = get_pests
        self.get_crops = get_crops

    def execute(self, product_id: int) -> Product:

        product = self.product_repo.get(product_id)
        return product


class UpdateProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, product_id: int, product_update: ProductCreate) -> Product:
        product = self.product_repo.update(product_id, product_update)
        return product


class DeleteProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, product_id: int) -> Product:
        product = self.product_repo.delete(product_id)
        return product
