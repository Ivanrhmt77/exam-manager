from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID

from app.schemas.course import CourseOut, CourseCreate, CourseUpdate
from app.models.course import Course


class DuplicateCodeError(Exception):
    """Raised when the course code is already used by an active (non-deleted) course."""


def create_course(db: Session, payload: CourseCreate) -> Course:
    course = Course(
        code=payload.code,
        name=payload.name,
        description=payload.description,
        credits=payload.credits,
        category=payload.category,
        delivery_type=payload.delivery_type,
    )
    db.add(course)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateCodeError(payload.code) from None
    db.refresh(course)
    return course


def list_courses(db: Session) -> list[CourseOut]:
    return (
        db.query(Course)
        .filter(Course.is_deleted.is_(False))
        .order_by(Course.created_at.desc())
        .all()
    )


def get_course_by_id(db: Session, course_id: UUID) -> Course | None:
    return (
        db.query(Course)
        .filter(Course.id == course_id, Course.is_deleted.is_(False))
        .first()
    )


def get_course_by_code(db: Session, code: str) -> Course | None:
    return (
        db.query(Course)
        .filter(Course.code == code, Course.is_deleted.is_(False))
        .first()
    )


def update_course(db: Session, course: Course, payload: CourseUpdate) -> Course:
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course


def soft_delete_course(db: Session, course: Course) -> None:
    course.is_deleted = True
    db.commit()
