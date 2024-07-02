from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.pest import Pest
from app.db.repositories.pest_repository import PestRepository

router = APIRouter()


@router.get("/{pest_id}", response_model=Pest, status_code=status.HTTP_200_OK)
def read_pest(pest_id: int, db: Session = Depends(get_db)) -> Pest:

    pest_repo = PestRepository(db)
    db_pest = pest_repo.get(pest_id)
    if db_pest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pest not found"
        )

    return db_pest
