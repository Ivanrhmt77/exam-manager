from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.course import CourseOut
from app.api.deps import get_db, require_role
from app.models.user import User, UserRole
from app.crud import course as course_crud

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[CourseOut])
def list_courses(
    db: Session = Depends(get_db), _: User = Depends(require_role(UserRole.ADMIN))
):
    return course_crud.list_courses(db)
