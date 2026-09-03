from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


class DuplicateEmailError(Exception):
    """Raised when the email is already used by an active (non-deleted) user."""


def create_user(db: Session, payload: UserCreate) -> User:
    default_password = payload.nip if payload.role == UserRole.LECTURER else payload.nrp

    user = User(
        email=payload.email,
        name=payload.name,
        role=payload.role,
        nip=payload.nip,
        nrp=payload.nrp,
        hashed_password=hash_password(default_password),
        must_change_password=True,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateEmailError(payload.email) from None
    db.refresh(user)
    return user


def list_users(db: Session, role: UserRole | None = None) -> list[User]:
    query = db.query(User).filter(User.is_deleted.is_(False))
    if role is not None:
        query = query.filter(User.role == role)
    return query.order_by(User.created_at.desc()).all()


def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    return db.query(User).filter(User.id == user_id, User.is_deleted.is_(False)).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return (
        db.query(User).filter(User.email == email, User.is_deleted.is_(False)).first()
    )


def update_user(db: Session, user: User, payload: UserUpdate) -> User:
    update_data = payload.model_dump(exclude_unset=True)
    for (
        field,
        value,
    ) in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def soft_delete_user(db: Session, user: User) -> None:
    user.is_deleted = True
    db.commit()
