from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.blog import Blog
from app.db.repositories.blog_repository import BlogRepository
from app.use_cases.blog_use_cases import ListBlogsUseCase
from typing import List

router = APIRouter()


@router.get("/", response_model=List[Blog], status_code=status.HTTP_200_OK)
def read_blogs(db: Session = Depends(get_db)) -> List[Blog]:
    blog_repo = BlogRepository(db)
    list_blogs_use_case = ListBlogsUseCase(blog_repo)

    try:
        blogs = list_blogs_use_case.execute()
        return blogs

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving blogs",
        )
