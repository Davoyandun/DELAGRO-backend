from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.crop import Crop
from app.db.repositories.crop_repository import CropRepository
from app.use_cases.crop_use_cases import DeleteCropUseCase

router = APIRouter()


@router.delete("/{crop_id}", response_model=Crop, status_code=status.HTTP_200_OK)
def delete_crop(crop_id: int, db: Session = Depends(get_db)) -> Crop:

    crop_repo = CropRepository(db)
    delete_crop_use_case = DeleteCropUseCase(crop_repo)

    try:
        deleted_crop = delete_crop_use_case.execute(crop_id)
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
