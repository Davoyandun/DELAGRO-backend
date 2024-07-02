from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.crop import Crop, CropCreate
from app.db.repositories.crop_repository import CropRepository

router = APIRouter()


@router.put("/{crop_id}", response_model=Crop, status_code=status.HTTP_200_OK)
def update_crop(crop_id: int, crop: CropCreate, db: Session = Depends(get_db)) -> Crop:

    crop_repo = CropRepository(db)
    db_crop = crop_repo.get(crop_id)
    if db_crop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found"
        )

    try:
        updated_crop = crop_repo.update(crop_id, crop)
        return updated_crop
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
