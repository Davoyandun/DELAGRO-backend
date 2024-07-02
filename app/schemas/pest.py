from pydantic import BaseModel
from typing import List, Optional


class PestBase(BaseModel):
    name: str
    description: str


class PestCreate(PestBase):
    product_ids: List[int] = []

    class Config:
        extra = "forbid"


class Pest(PestBase):
    id: int
    products: Optional[List[int]] = []

    class Config:
        from_attributes = True
