from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.crop import CropCreate, Crop
from app.db.repositories.crop_repository import CropRepository
from app.services.product_service import get_product
from app.use_cases.crop_use_cases import CreateCropUseCase

router = APIRouter()


@router.post("/", response_model=Crop, status_code=status.HTTP_201_CREATED)
def create_crop(crop: CropCreate = Body(...), db: Session = Depends(get_db)) -> Crop:

    crop_repo = CropRepository(db)
    create_crop_use_case = CreateCropUseCase(crop_repo, get_product)

    try:
        created_crop = create_crop_use_case.execute(crop, db)
        return created_crop

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
