from sqlalchemy.orm import Session
from app.db.models.product import Product
from app.db.repositories.base_repository import BaseRepository
from typing import List, Optional
from sqlalchemy import asc, desc


class ProductRepository(BaseRepository[Product]):

    def __init__(self, db: Session):
        super().__init__(db, Product)

    def get_filtered(
        self,
        name: Optional[str] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        order_by: Optional[str] = None,
        order: Optional[str] = "asc",
    ) -> List[Product]:
        query = self.db.query(Product)

        if name:
            query = query.filter(Product.name.like(f"%{name}%"))
        if min_price:
            query = query.filter(Product.price >= min_price)
        if max_price:
            query = query.filter(Product.price <= max_price)

        if order_by:
            if order == "asc":
                query = query.order_by(asc(order_by))
            else:
                query = query.order_by(desc(order_by))

        return query.all()
