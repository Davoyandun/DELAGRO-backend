from sqlalchemy.orm import Session
from app.db.models.crop import Crop
from typing import List, Optional

def get_crops(db: Session, crop_ids: Optional[List[int]]) -> List[Crop]:
    if crop_ids:
        return db.query(Crop).filter(Crop.id.in_(crop_ids)).all()
    return []