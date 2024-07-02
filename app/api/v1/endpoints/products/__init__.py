from app.api.v1.endpoints.products.create_product import router as create_product_router
from app.api.v1.endpoints.products.read_product import router as read_product_router
from app.api.v1.endpoints.products.read_products import router as read_products_router
from app.api.v1.endpoints.products.update_product import router as update_product_router
from app.api.v1.endpoints.products.delete_product import router as delete_product_router

routers = [
    create_product_router,
    read_product_router,
    read_products_router,
    update_product_router,
    delete_product_router,
]
