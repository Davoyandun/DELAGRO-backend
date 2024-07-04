from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.crop import Crop
from app.db.repositories.crop_repository import CropRepository

router = APIRouter()


@router.delete("/{crop_id}", response_model=Crop, status_code=status.HTTP_200_OK)
def delete_crop(crop_id: int, db: Session = Depends(get_db)) -> Crop:

    crop_repo = CropRepository(db)

    try:
        deleted_crop = crop_repo.delete(crop_id)
        if not deleted_crop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found"
            )
        return deleted_crop
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
