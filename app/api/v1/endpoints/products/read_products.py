from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import Product
from app.db.repositories.product_repository import ProductRepository
from typing import List

router = APIRouter()


@router.get("/", response_model=List[Product], status_code=status.HTTP_200_OK)
def read_products(db: Session = Depends(get_db)) -> List[Product]:

    try:
        product_repo = ProductRepository(db)
        products = product_repo.get_all()
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving products",
        )
