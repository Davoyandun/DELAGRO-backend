from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

product_pest_association = Table(
    "product_pest",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("pest_id", Integer, ForeignKey("pests.id")),
)

product_crop_association = Table(
    "product_crop",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("crop_id", Integer, ForeignKey("crops.id")),
)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255))
    price = Column(Integer)
    img_url = Column(String(255))
    pests = relationship(
        "Pest", secondary=product_pest_association, back_populates="products"
    )
    crops = relationship(
        "Crop", secondary=product_crop_association, back_populates="products"
    )
