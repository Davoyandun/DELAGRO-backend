from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import create_db_and_tables

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(api_router, prefix=settings.API_V1_STR)
