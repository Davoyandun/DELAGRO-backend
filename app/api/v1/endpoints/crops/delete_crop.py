from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.crop import Crop
from app.db.repositories.crop_repository import CropRepository

router = APIRouter()


@router.delete("/{crop_id}", response_model=Crop, status_code=status.HTTP_200_OK)
def delete_crop(crop_id: int, db: Session = Depends(get_db)) -> Crop:

    crop_repo = CropRepository(db)
    db_crop = crop_repo.get(crop_id)
    if db_crop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found"
        )

    try:
        deleted_crop = crop_repo.delete(db_crop)
        return deleted_crop
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
