from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.course import CourseOut, CourseCreate
from app.api.deps import get_db, require_role
from app.models.user import User, UserRole
from app.crud import course as course_crud
from app.models.course import Course

router = APIRouter(prefix="/courses", tags=["courses"])


def _require_course(db: Session, course_id: UUID) -> Course:
    course = course_crud.get_user_by_id(db, course_id)
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
        )
    return course


@router.post("", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    if course_crud.get_user_by_code(db, payload.code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Course code already registered",
        )
    return course_crud.create_course(db, payload)


@router.get("", response_model=list[CourseOut])
def list_courses(
    db: Session = Depends(get_db), _: User = Depends(require_role(UserRole.ADMIN))
):
    return course_crud.list_courses(db)


@router.get("/{course_id}", response_model=CourseOut)
def get_course(
    course_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    return _require_course(db, course_id)
