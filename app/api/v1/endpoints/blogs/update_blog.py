from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.blog import Blog, BlogCreate
from app.db.repositories.blog_repository import BlogRepository
from app.use_cases.blog_use_cases import UpdateBlogUseCase

router = APIRouter()


@router.put("/{blog_id}", response_model=Blog, status_code=status.HTTP_200_OK)
def update_blog(blog_id: int, blog: BlogCreate, db: Session = Depends(get_db)) -> Blog:

    blog_repo = BlogRepository(db)
    update_blog_use_case = UpdateBlogUseCase(blog_repo)

    try:
        updated_blog = update_blog_use_case.execute(blog_id, blog)
        return updated_blog

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
