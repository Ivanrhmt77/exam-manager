from sqlalchemy.orm import Session

from app.schemas.course import CourseOut
from app.models.course import Course


def list_courses(db: Session) -> list[CourseOut]:
    return (
        db.query(Course)
        .filter(Course.is_deleted.is_(False))
        .order_by(Course.created_at.desc())
        .all()
    )
