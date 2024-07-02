from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import Product
from app.db.repositories.product_repository import ProductRepository

router = APIRouter()


@router.get("/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
def read_product(product_id: int, db: Session = Depends(get_db)) -> Product:

    product_repo = ProductRepository(db)
    db_product = product_repo.get(product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return db_product
