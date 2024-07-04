from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.pest import Pest, PestCreate
from app.db.repositories.pest_repository import PestRepository
from app.use_cases.pest_use_cases import UpdatePestUseCase

router = APIRouter()


@router.put("/{pest_id}", response_model=Pest, status_code=status.HTTP_200_OK)
def update_pest(pest_id: int, pest: PestCreate, db: Session = Depends(get_db)) -> Pest:

    pest_repo = PestRepository(db)
    update_pest_use_case = UpdatePestUseCase(pest_repo)

    try:
        updated_pest = update_pest_use_case.execute(pest_id, pest)
        return updated_pest

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
