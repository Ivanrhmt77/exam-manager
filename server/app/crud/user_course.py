from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID

from app.models.user_course import UserCourse


class DuplicateAssignmentError(Exception):
    """Raised when the lecturer is already assigned to this course."""


def create_user_course(db: Session, course_id: UUID, user_id: UUID):
    user_course = UserCourse(course_id=course_id, user_id=user_id)
    db.add(user_course)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateAssignmentError(user_id) from None
    db.refresh(user_course)
    return user_course


def get_assignment(db: Session, course_id: UUID, user_id: UUID) -> UserCourse | None:
    return (
        db.query(UserCourse)
        .filter(
            UserCourse.course_id == course_id,
            UserCourse.user_id == user_id,
        )
        .first()
    )


def get_user_course_by_id(db: Session, user_course_id: UUID) -> UserCourse | None:
    return db.query(UserCourse).filter(UserCourse.id == user_course_id).first()


def list_lecturers_by_course(db: Session, course_id: UUID) -> list[UserCourse]:
    return db.query(UserCourse).filter(UserCourse.course_id == course_id).all()


def delete_user_course(db: Session, user_course: UserCourse) -> None:
    db.delete(user_course)
    db.commit()
