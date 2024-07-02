from app.api.v1.endpoints.crops.create_crop import router as create_crop_router
from app.api.v1.endpoints.crops.read_crop import router as read_crop_router
from app.api.v1.endpoints.crops.read_crops import router as read_crops_router
from app.api.v1.endpoints.crops.update_crop import router as update_crop_router
from app.api.v1.endpoints.crops.delete_crop import router as delete_crop_router

routers = [
    create_crop_router,
    read_crop_router,
    read_crops_router,
    update_crop_router,
    delete_crop_router,
]
