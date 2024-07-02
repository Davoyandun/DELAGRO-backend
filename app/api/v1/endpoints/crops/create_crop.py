from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.crop import CropCreate, Crop
from app.db.repositories.crop_repository import CropRepository
from app.db.models.crop import Crop as CropModel
from app.services.product_service import get_product

router = APIRouter()


@router.post("/", response_model=Crop, status_code=status.HTTP_201_CREATED)
def create_crop(crop: CropCreate = Body(...), db: Session = Depends(get_db)) -> Crop:

    crop_repo = CropRepository(db)
    db_crop = CropModel(name=crop.name, description=crop.description)

    try:
        db_crop.products = get_product(db, crop.product_ids)

        created_crop = crop_repo.create(db_crop)

        return created_crop

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
