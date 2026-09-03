from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.course import CourseOut
from app.models.course import Course


def list_courses(db: Session) -> list[CourseOut]:
    return (
        db.query(Course)
        .filter(Course.is_deleted.is_(False))
        .order_by(Course.created_at.desc())
        .all()
    )


def get_user_by_id(db: Session, course_id: UUID) -> Course | None:
    return (
        db.query(Course)
        .filter(Course.id == course_id and Course.is_deleted.is_(False))
        .first()
    )


def get_user_by_code(db: Session, code: str) -> Course | None:
    return (
        db.query(Course)
        .filter(Course.code == code and Course.is_deleted.is_(False))
        .first()
    )
