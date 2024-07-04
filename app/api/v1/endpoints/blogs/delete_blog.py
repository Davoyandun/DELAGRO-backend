from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.blog import Blog
from app.db.repositories.blog_repository import BlogRepository
from app.use_cases.blog_use_cases import DeleteBlogUseCase
router = APIRouter()


@router.delete("/{blog_id}", response_model=Blog, status_code=status.HTTP_200_OK)
def delete_blog(blog_id: int, db: Session = Depends(get_db)) -> Blog:

    blog_repo = BlogRepository(db)
    delete_blog_use_case = DeleteBlogUseCase(blog_repo)

    try:
        deleted_blog = delete_blog_use_case.execute(blog_id)
        if not deleted_blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
            )
        return deleted_blog
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
