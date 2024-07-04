from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import Product
from app.db.repositories.product_repository import ProductRepository
from app.use_cases.product_use_cases import ListProductUseCase

router = APIRouter()


@router.get("/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
def read_product(product_id: int, db: Session = Depends(get_db)) -> Product:

    product_repo = ProductRepository(db)
    list_products_use_case = ListProductUseCase(product_repo)
    try:
        db_product = list_products_use_case.execute(product_id)

        if not db_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        return db_product
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
