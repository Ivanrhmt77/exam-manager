import uuid
import enum
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    LECTURER = "lecturer"
    STUDENT = "student"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    must_change_password = Column(Boolean, default=True, nullable=False)
    role = Column(Enum(UserRole, native_enum=False, length=20), nullable=False)
    name = Column(String, nullable=False)
    nip = Column(String, nullable=True)
    nrp = Column(String, nullable=True)
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
            "ix_users_email_unique_active",
            "email",
            unique=True,
            postgresql_where=text("is_deleted = false"),
        ),
    )
