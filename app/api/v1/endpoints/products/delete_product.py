from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import Product
from app.db.repositories.product_repository import ProductRepository
from app.use_cases.product_use_cases import DeleteProductUseCase

router = APIRouter()


@router.delete("/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
def delete_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    product_repo = ProductRepository(db)
    delete_product_use_case = DeleteProductUseCase(product_repo)

    try:
        deleted_product = delete_product_use_case.execute(product_id)
        if not deleted_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        return deleted_product
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
