from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic

T = TypeVar("T")


class BaseRepository(Generic[T]):

    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get(self, item_id: int) -> T:
        return self.db.query(self.model).filter(self.model.id == item_id).first()

    def create(self, item: T) -> T:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_all(self) -> list[T]:
        return self.db.query(self.model).all()

    def update(self, item_id: int, item: T) -> T:
        db_item = self.get(item_id)
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete(self, item: T) -> T:
        self.db.delete(item)
        self.db.commit()
        return item
