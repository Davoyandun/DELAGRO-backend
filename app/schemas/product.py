from pydantic import BaseModel
from typing import List, Optional


class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    img_url: str


class ProductCreate(ProductBase):
    pest_ids: List[int] = []
    crop_ids: List[int] = []

    class Config:
        extra = "forbid"


class Product(ProductBase):
    id: int
    pests: Optional[List[int]] = []
    crops: Optional[List[int]] = []

    class Config:
        from_attributes = True
