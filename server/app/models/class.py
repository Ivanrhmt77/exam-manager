import uuid
import enum
from sqlalchemy import Column, DateTime, Boolean, Enum, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base


class Semester(str, enum.Enum):
    ODD = "odd"
    EVEN = "even"
    ODD_SHORT = "odd_short"
    EVEN_SHORT = "even_short"


class Class(Base):
    __tablename__ = "classes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    semester = Column(Enum(Semester, native_enum=False, length=20), nullable=False)
    year = Column(Integer, nullable=False)
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
