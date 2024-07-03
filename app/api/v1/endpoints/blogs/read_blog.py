from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.blog import Blog
from app.db.repositories.blog_repository import BlogRepository

router = APIRouter()


@router.get("/{blog_id}", response_model=Blog, status_code=status.HTTP_200_OK)
def read_blog(blog_id: int, db: Session = Depends(get_db)) -> Blog:

    blog_repo = BlogRepository(db)
    db_blog = blog_repo.get(blog_id)
    if db_blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    return db_blog
