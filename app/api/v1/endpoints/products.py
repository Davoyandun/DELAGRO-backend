from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.product import Product, ProductCreate
from app.db.repositories.product_repository import ProductRepository
from app.db.models.pest import Pest
from app.db.models.crop import Crop
from app.db.models.product import Product as ProductModel


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=Product)
def create_product(product: ProductCreate = Body(...), db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)

    db_product = ProductModel(
        name=product.name, description=product.description, price=product.price
    )

    if product.pest_ids:
        pests = db.query(Pest).filter(Pest.id.in_(product.pest_ids)).all()
        db_product.pests = pests

    if product.crop_ids:
        crops = db.query(Crop).filter(Crop.id.in_(product.crop_ids)).all()
        db_product.crops = crops

    return product_repo.create(db_product)


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    db_product = product_repo.get(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.get("/", response_model=list[Product])
def read_products(db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    return product_repo.get_all()


@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int, product: ProductCreate, db: Session = Depends(get_db)
):
    product_repo = ProductRepository(db)
    db_product = product_repo.get(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_repo.update(product)


@router.delete("/{product_id}", response_model=Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    db_product = product_repo.get(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_repo.delete(db_product)
