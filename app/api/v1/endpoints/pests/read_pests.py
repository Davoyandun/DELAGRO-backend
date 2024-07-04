from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.pest import Pest
from app.db.repositories.pest_repository import PestRepository
from app.use_cases.pest_use_cases import ListPestsUseCase
from typing import List

router = APIRouter()


@router.get("/", response_model=List[Pest], status_code=status.HTTP_200_OK)
def read_pests(db: Session = Depends(get_db)) -> List[Pest]:
    pest_repo = PestRepository(db)
    list_pests_use_case = ListPestsUseCase(pest_repo)

    try:
        pests = list_pests_use_case.execute()
        return pests

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving pests",
        )
