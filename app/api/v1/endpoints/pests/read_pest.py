from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.pest import Pest
from app.db.repositories.pest_repository import PestRepository
from app.use_cases.pest_use_cases import ListPestUseCase

router = APIRouter()


@router.get("/{pest_id}", response_model=Pest, status_code=status.HTTP_200_OK)
def read_pest(pest_id: int, db: Session = Depends(get_db)) -> Pest:

    pest_repo = PestRepository(db)
    list_pest_use_case = ListPestUseCase(pest_repo)
    try:
        pest = list_pest_use_case.execute(pest_id)
        if not pest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pest not found"
            )
        return pest
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
