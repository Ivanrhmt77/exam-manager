from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID

from app.models.user_course import UserCourse


class DuplicateAssignmentError(Exception):
    """Raised when the lecturer is already assigned (active) to this course."""


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


def list_lecturers_by_course(db: Session, course_id: UUID) -> list[UserCourse]:
    return (
        db.query(UserCourse)
        .filter(UserCourse.course_id == course_id, UserCourse.is_deleted.is_(False))
        .all()
    )


def soft_delete_user_course(db: Session, user_course: UserCourse) -> None:
    user_course.is_deleted = True
    db.commit()


def reactivate_user_course(db: Session, user_course: UserCourse) -> UserCourse:
    user_course.is_deleted = False
    db.commit()
    db.refresh(user_course)
    return user_course
