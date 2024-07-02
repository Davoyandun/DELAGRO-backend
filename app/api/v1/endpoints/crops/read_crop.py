from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.crop import Crop
from app.db.repositories.crop_repository import CropRepository

router = APIRouter()


@router.get("/{crop_id}", response_model=Crop, status_code=status.HTTP_200_OK)
def read_crop(crop_id: int, db: Session = Depends(get_db)) -> Crop:

    crop_repo = CropRepository(db)
    db_crop = crop_repo.get(crop_id)
    if db_crop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found"
        )

    return db_crop
