from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import Product, ProductCreate
from app.db.repositories.product_repository import ProductRepository
from app.db.models.product import Product as ProductModel
from app.services.pest_service import get_pests
from app.services.crop_service import get_crops

router = APIRouter()


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate = Body(...), db: Session = Depends(get_db)
) -> Product:

    product_repo = ProductRepository(db)

    db_product = ProductModel(
        name=product.name,
        description=product.description,
        price=product.price,
        img_url=product.img_url,
    )

    try:
        db_product.pests = get_pests(db, product.pest_ids)
        db_product.crops = get_crops(db, product.crop_ids)

        created_product = product_repo.create(db_product)
        return created_product

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
