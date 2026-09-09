import uuid
from sqlalchemy import Column, ForeignKey, DateTime, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class ClassStudent(Base):
    __tablename__ = "class_students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    class_ = relationship("Class")
    user = relationship("User")

    __table_args__ = (
        Index(
            "ix_class_students_class_id_user_id_unique",
            "class_id",
            "user_id",
            unique=True,
        ),
    )
