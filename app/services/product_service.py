from sqlalchemy.orm import Session
from app.db.models.product import Product
from typing import List, Optional


def get_product(db: Session, product_ids: Optional[List[int]]) -> List[Product]:
    if product_ids:
        return db.query(Product).filter(Product.id.in_(product_ids)).all()
    return []
