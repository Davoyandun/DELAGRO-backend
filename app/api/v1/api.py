from fastapi import APIRouter
from app.api.v1.endpoints.products import routers as product_routers
from app.api.v1.endpoints.pests import routers as pest_routers
from app.api.v1.endpoints.crops import routers as crop_routers


router = APIRouter()

for r in product_routers:
    router.include_router(r, prefix="/products", tags=["products"])

for r in pest_routers:
    router.include_router(r, prefix="/pests", tags=["pests"])

for r in crop_routers:
    router.include_router(r, prefix="/crops", tags=["crops"])
