from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import Product, ProductCreate
from app.db.repositories.product_repository import ProductRepository
from app.use_cases.product_use_cases import CreateProductUseCase
from app.services.pest_service import get_pests
from app.services.crop_service import get_crops

router = APIRouter()


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate = Body(...), db: Session = Depends(get_db)
) -> Product:

    product_repo = ProductRepository(db)
    create_product_use_case = CreateProductUseCase(product_repo, get_pests, get_crops)

    try:
        product = create_product_use_case.execute(product, db)
        return product
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
