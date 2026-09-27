from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID

from app.models.class_ import Class
from app.models.user_course import UserCourse
from app.models.course import Course, CourseDeliveryType
from app.schemas.class_ import ClassCreate, ClassUpdate

CLASS_INDEX_LABELS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class DuplicateClassIndexError(Exception):
    """Raised when class_index is already used by an existing class for this user_course_id."""


def _build_class_name(user_course: UserCourse, class_index: int) -> str:
    label = (
        CLASS_INDEX_LABELS[class_index]
        if class_index < len(CLASS_INDEX_LABELS)
        else str(CLASS_INDEX_LABELS)
    )
    return f"{user_course.course.name} - Class {label}"


def create_class(db: Session, payload: ClassCreate, user_course: UserCourse) -> Class:
    cls = Class(
        user_course_id=payload.user_course_id,
        class_index=payload.class_index,
        name=_build_class_name(user_course, payload.class_index),
        academic_year=payload.academic_year,
        term=payload.term,
        schedule_day=payload.schedule_day,
        schedule_start_time=payload.schedule_start_time,
        schedule_end_time=payload.schedule_end_time,
        room=payload.room,
    )
    db.add(cls)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateClassIndexError(payload.class_index) from None
    db.refresh(cls)
    return cls


def list_classes(db: Session, user_course_id: UUID | None = None) -> list[Class]:
    query = db.query(Class)
    if user_course_id is not None:
        query = query.filter(Class.user_course_id == user_course_id)
    return query.order_by(Class.created_at.desc()).all()


def get_class_by_id(db: Session, class_id: UUID) -> Class | None:
    return db.query(Class).filter(Class.id == class_id).first()


def update_class(db: Session, cls: Class, payload: ClassUpdate) -> Class:
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cls, field, value)
    db.commit()
    db.refresh(cls)
    return cls


def delete_class(db: Session, cls: Class) -> None:
    db.delete(cls)
    db.commit()
