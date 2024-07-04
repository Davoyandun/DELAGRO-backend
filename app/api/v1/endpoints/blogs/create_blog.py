from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.blog import Blog, BlogCreate
from app.db.repositories.blog_repository import BlogRepository
from app.use_cases.blog_use_cases import CreateBlogUseCase

router = APIRouter()


@router.post("/", response_model=Blog, status_code=status.HTTP_201_CREATED)
def create_blog(blog: BlogCreate = Body(...), db: Session = Depends(get_db)) -> Blog:

    blog_repo = BlogRepository(db)
    create_blog_use_case = CreateBlogUseCase(blog_repo)

    try:
        created_blog = create_blog_use_case.execute(blog)
        return created_blog

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
