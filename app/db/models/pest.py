from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Pest(Base):
    __tablename__ = "pests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255))
    products = relationship("Product", secondary="product_pest", back_populates="pests")
