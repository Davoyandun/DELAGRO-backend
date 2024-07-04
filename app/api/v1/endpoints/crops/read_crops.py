from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.crop import Crop
from app.db.repositories.crop_repository import CropRepository
from app.use_cases.crop_use_cases import ListCropsUseCase
from typing import List

router = APIRouter()


@router.get("/", response_model=List[Crop], status_code=status.HTTP_200_OK)
def read_crops(db: Session = Depends(get_db)) -> List[Crop]:

    try:
        crop_repo = CropRepository(db)
        list_crops_use_case = ListCropsUseCase(crop_repo)

        crops = list_crops_use_case.execute()
        return crops
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving crops",
        )
