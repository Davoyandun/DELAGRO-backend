from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.blog import Blog, BlogCreate
from app.db.repositories.blog_repository import BlogRepository

router = APIRouter()


@router.put("/{blog_id}", response_model=Blog, status_code=status.HTTP_200_OK)
def update_blog(blog_id: int, blog: BlogCreate, db: Session = Depends(get_db)) -> Blog:

    blog_repo = BlogRepository(db)
    db_blog = blog_repo.get(blog_id)
    if db_blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    try:
        updated_blog = blog_repo.update(blog_id, blog)
        return updated_blog
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
