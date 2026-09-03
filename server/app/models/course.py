import uuid
import enum
from sqlalchemy import Boolean, Column, DateTime, String, Integer, Enum, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base


class CourseCategory(str, enum.Enum):
    MW = "MW"
    MPP = "MPP"
    MPI = "MPI"
    MPK = "MPK"
    MBKM = "MBKM"


class CourseDeliveryType(str, enum.Enum):
    THEORETICAL = "theoretical"
    PRACTICUM = "practicum"
    WORKSHOP = "workshop"


class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    credits = Column(Integer, nullable=False)
    category = Column(
        Enum(CourseCategory, native_enum=False, length=10), nullable=False
    )
    delivery_type = Column(
        Enum(CourseDeliveryType, native_enum=False, length=20), nullable=False
    )
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

    __table_args__ = (
        Index(
            "ix_courses_code_unique_active",
            "code",
            unique=True,
            postgresql_where=text("is_deleted = false"),
        ),
    )
