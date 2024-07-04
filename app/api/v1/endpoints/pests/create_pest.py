from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.pest import Pest, PestCreate
from app.db.repositories.pest_repository import PestRepository
from app.use_cases.pest_use_cases import CreatePestUseCase
from app.services.product_service import get_product

router = APIRouter()


@router.post("/", response_model=Pest, status_code=status.HTTP_201_CREATED)
def create_pest(pest: PestCreate = Body(...), db: Session = Depends(get_db)) -> Pest:

    pest_repo = PestRepository(db)
    create_pest_use_case = CreatePestUseCase(pest_repo, get_product)

    try:
        created_pest = create_pest_use_case.execute(pest, db)
        return created_pest

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
