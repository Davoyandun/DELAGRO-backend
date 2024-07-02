from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.pest import Pest
from app.db.repositories.pest_repository import PestRepository
from typing import List

router = APIRouter()


@router.get("/", response_model=List[Pest], status_code=status.HTTP_200_OK)
def read_pests(db: Session = Depends(get_db)) -> List[Pest]:

    try:
        pest_repo = PestRepository(db)
        pests = pest_repo.get_all()
        return pests
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving pests",
        )
