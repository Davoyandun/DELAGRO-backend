from sqlalchemy.orm import Session
from app.db.models.pest import Pest
from typing import List, Optional


def get_pests(db: Session, pest_ids: Optional[List[int]]) -> List[Pest]:
    if pest_ids:
        return db.query(Pest).filter(Pest.id.in_(pest_ids)).all()
    return []
