from app.api.v1.endpoints.blogs.create_blog import router as create_blog_router
from app.api.v1.endpoints.blogs.read_blog import router as read_blog_router
from app.api.v1.endpoints.blogs.read_blogs import router as read_blogs_router
from app.api.v1.endpoints.blogs.update_blog import router as update_blog_router
from app.api.v1.endpoints.blogs.delete_blog import router as delete_blog_router

routers = [
    create_blog_router,
    read_blog_router,
    read_blogs_router,
    update_blog_router,
    delete_blog_router,
]
