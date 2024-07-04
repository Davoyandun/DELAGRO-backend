from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import Product, ProductCreate
from app.db.repositories.product_repository import ProductRepository
from app.use_cases.product_use_cases import UpdateProductUseCase

router = APIRouter()


@router.put("/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
def update_product(
    product_id: int, product: ProductCreate, db: Session = Depends(get_db)
) -> Product:

    product_repo = ProductRepository(db)
    update_product_use_case = UpdateProductUseCase(product_repo)
    try:
        db_product = update_product_use_case.execute(product_id, product)
        return db_product

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
