from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.pest import Pest
from app.db.repositories.pest_repository import PestRepository

router = APIRouter()

@router.delete("/{pest_id}", response_model=Pest, status_code=status.HTTP_200_OK)
def delete_pest(pest_id: int, db: Session = Depends(get_db)) -> Pest:

    pest_repo = PestRepository(db)
    db_pest = pest_repo.get(pest_id)
    if db_pest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pest not found"
        )

    try:
        deleted_pest = pest_repo.delete(db_pest)
        return deleted_pest
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
