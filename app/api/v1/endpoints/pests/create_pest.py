from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.pest import Pest, PestCreate
from app.db.repositories.pest_repository import PestRepository
from app.db.models.pest import Pest as PestModel
from app.services.product_service import get_product

router = APIRouter()


@router.post("/", response_model=Pest, status_code=status.HTTP_201_CREATED)
def create_pest(pest: PestCreate = Body(...), db: Session = Depends(get_db)) -> Pest:

    pest_repo = PestRepository(db)
    db_pest = PestModel(name=pest.name, description=pest.description)

    try:
        db_pest.products = get_product(db, pest.product_ids)

        created_pest = pest_repo.create(db_pest)

        return created_pest

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
