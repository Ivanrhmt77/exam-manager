from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.course import CourseOut, CourseCreate, CourseUpdate
from app.api.deps import get_db, require_role
from app.models.user import User, UserRole
from app.crud import course as course_crud, user_course as user_course_crud
from app.models.course import Course
from app.schemas.user_course import UserCourseOut, UserCourseCreate
from app.crud.user import get_user_by_id

router = APIRouter(prefix="/courses", tags=["courses"])


def _require_course(db: Session, course_id: UUID) -> Course:
    course = course_crud.get_course_by_id(db, course_id)
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
    if course_crud.get_course_by_code(db, payload.code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Course code already registered",
        )
    try:
        return course_crud.create_course(db, payload)
    except course_crud.DuplicateCodeError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Course code already registered",
        )


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


@router.patch("/{course_id}", response_model=CourseOut)
def update_course(
    course_id: UUID,
    payload: CourseUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    course = _require_course(db, course_id)
    return course_crud.update_course(db, course, payload)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    course = _require_course(db, course_id)
    return course_crud.soft_delete_course(db, course)


@router.post(
    "/{course_id}/lecturers",
    response_model=UserCourseOut,
    status_code=status.HTTP_201_CREATED,
)
def assign_lecturer(
    course_id: UUID,
    payload: UserCourseCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    _require_course(db, course_id)

    lecturer = get_user_by_id(db, payload.user_id)
    if lecturer is None or lecturer.role != UserRole.LECTURER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id must belong to an existing lecturer",
        )

    assignment = user_course_crud.get_assignment(db, course_id, payload.user_id)
    if assignment is not None:
        if not assignment.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Lecturer is already assigned to this course",
            )
        return user_course_crud.reactivate_user_course(db, assignment)

    try:
        return user_course_crud.create_user_course(db, course_id, payload.user_id)
    except user_course_crud.DuplicateAssignmentError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Lecturer is already assigned to this course",
        )


@router.get("/{course_id}/lecturers", response_model=list[UserCourseOut])
def list_course_lecturers(
    course_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    _require_course(db, course_id)
    return user_course_crud.list_lecturers_by_course(db, course_id)


@router.delete(
    "/{course_id}/lecturers/{user_id}", status_code=status.HTTP_204_NO_CONTENT
)
def unassign_lecturer(
    course_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    _require_course(db, course_id)

    assignment = user_course_crud.get_assignment(db, course_id, user_id)
    if assignment is None or assignment.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found"
        )

    return user_course_crud.soft_delete_user_course(db, assignment)
