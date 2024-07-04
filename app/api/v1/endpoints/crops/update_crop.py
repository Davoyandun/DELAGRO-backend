from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.crop import Crop, CropCreate
from app.db.repositories.crop_repository import CropRepository
from app.use_cases.crop_use_cases import UpdateCropUseCase

router = APIRouter()


@router.put("/{crop_id}", response_model=Crop, status_code=status.HTTP_200_OK)
def update_crop(crop_id: int, crop: CropCreate, db: Session = Depends(get_db)) -> Crop:

    crop_repo = CropRepository(db)
    update_crop_use_case = UpdateCropUseCase(crop_repo)

    try:
        updated_crop = update_crop_use_case.execute(crop_id, crop)
        return updated_crop

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
