from pydantic import BaseModel
from typing import List, Optional


class BlogBase(BaseModel):
    author: str
    content: str
    title: str
    img_url: str


class BlogCreate(BlogBase):

    class Config:
        extra = "forbid"


class Blog(BlogBase):
    id: int

    class Config:
        from_attributes = True
