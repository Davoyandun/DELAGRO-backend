from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.crop import Crop
from app.db.repositories.crop_repository import CropRepository
from app.use_cases.crop_use_cases import ListCropUseCase

router = APIRouter()


@router.get("/{crop_id}", response_model=Crop, status_code=status.HTTP_200_OK)
def read_crop(crop_id: int, db: Session = Depends(get_db)) -> Crop:

    crop_repo = CropRepository(db)
    list_crop_use_case = ListCropUseCase(crop_repo)

    try:
        crop = list_crop_use_case.execute(crop_id)
        if not crop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found"
            )
        return crop

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
