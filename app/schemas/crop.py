from pydantic import BaseModel
from typing import List, Optional


class CropBase(BaseModel):
    name: str


class CropCreate(CropBase):
    product_ids: List[int] = []

    class Config:
        extra = "forbid"

class Crop(CropBase):
    id: int
    products: Optional[List[int]] = []

    class Config:
        from_attributes = True
