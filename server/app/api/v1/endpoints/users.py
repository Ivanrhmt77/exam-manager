from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.user import UserOut, UserCreate, UserUpdate
from app.api.deps import get_db, require_role
from app.models.user import User, UserRole
from app.crud import user as user_crud

router = APIRouter(prefix="/users", tags=["users"])


def _require_user(db: Session, user_id: UUID) -> User:
    user = user_crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    if user_crud.get_user_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    try:
        return user_crud.create_user(db, payload)
    except user_crud.DuplicateEmailError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )


@router.get("", response_model=list[UserOut])
def list_users(
    role: UserRole | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    return user_crud.list_users(db, role)


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    return _require_user(db, user_id)


@router.patch("/{user_id}", response_model=UserOut)
def update_user(
    user_id: UUID,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    user = _require_user(db, user_id)
    return user_crud.update_user(db, user, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    user = _require_user(db, user_id)
    user_crud.soft_delete_user(db, user)
