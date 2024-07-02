from app.api.v1.endpoints.pests.create_pest import router as create_pest_router
from app.api.v1.endpoints.pests.read_pest import router as read_pest_router
from app.api.v1.endpoints.pests.read_pests import router as read_pests_router
from app.api.v1.endpoints.pests.update_pest import router as update_pest_router
from app.api.v1.endpoints.pests.delete_pest import router as delete_pest_router

routers = [
    create_pest_router,
    read_pest_router,
    read_pests_router,
    update_pest_router,
    delete_pest_router,
]
