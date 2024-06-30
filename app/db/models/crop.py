from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

pest_crop_association = Table('pest_crop', Base.metadata,
    Column('pest_id', Integer, ForeignKey('pests.id')),
    Column('crop_id', Integer, ForeignKey('crops.id'))
)

class Crop(Base):
    __tablename__ = 'crops'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    pests = relationship("Pest", secondary=pest_crop_association, back_populates="crops")
    products = relationship("Product", secondary="product_crop", back_populates="crops")
