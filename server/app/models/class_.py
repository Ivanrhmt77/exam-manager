import uuid
import enum
from sqlalchemy import (
    Column,
    DateTime,
    Boolean,
    Enum,
    String,
    Integer,
    ForeignKey,
    Time,
    Index,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Term(str, enum.Enum):
    ODD = "odd"
    EVEN = "even"
    ODD_SHORT = "odd_short"
    EVEN_SHORT = "even_short"


class ClassStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"


class Class(Base):
    __tablename__ = "classes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_course_id = Column(
        UUID(as_uuid=True), ForeignKey("user_courses.id"), nullable=False
    )
    class_index = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    academic_year = Column(Integer, nullable=False)
    term = Column(Enum(Term, native_enum=False, length=20), nullable=False)
    status = Column(
        Enum(ClassStatus, native_enum=False, length=20),
        nullable=False,
        default=ClassStatus.ACTIVE,
    )
    schedule_day = Column(String, nullable=True)
    schedule_start_time = Column(Time, nullable=True)
    schedule_end_time = Column(Time, nullable=True)
    room = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user_course = relationship("UserCourse")
    
    __table_args__ = (
        Index(
            "ix_classes_user_course_id_class_index_unique_active",
            "user_course_id",
            "class_index",
            unique=True,
            postgresql_where=text("is_deleted = false"),
        ),
    )
