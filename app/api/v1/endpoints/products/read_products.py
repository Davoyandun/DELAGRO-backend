from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.product import Product
from app.db.repositories.product_repository import ProductRepository
from app.use_cases.product_use_cases import ListProductsUseCase

router = APIRouter()


@router.get("/", response_model=List[Product], status_code=status.HTTP_200_OK)
def read_products(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="Filter by product name"),
    min_price: Optional[int] = Query(None, description="Filter by minimum price"),
    max_price: Optional[int] = Query(None, description="Filter by maximum price"),
    order_by: Optional[str] = Query(None, description="Order by field"),
    order: Optional[str] = Query("asc", description="Order direction: 'asc' or 'desc'"),
) -> List[Product]:

    try:
        product_repo = ProductRepository(db)
        list_products_use_case = ListProductsUseCase(product_repo)
        products = list_products_use_case.execute(
            name=name,
            min_price=min_price,
            max_price=max_price,
            order_by=order_by,
            order=order,
        )
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving products: {str(e)}",
        )
