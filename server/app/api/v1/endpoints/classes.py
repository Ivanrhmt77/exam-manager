from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.class_ import ClassOut, ClassCreate, ClassUpdate
from app.api.deps import get_db, require_role
from app.models.user import User, UserRole
from app.models.class_ import Class
from app.crud import class_ as class_crud, user_course as user_course_crud

router = APIRouter(prefix="/classes", tags=["classes"])


def _require_class(db: Session, class_id: UUID) -> Class:
    cls = class_crud.get_class_by_id(db, class_id)
    if cls is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Class not found"
        )
    return cls


@router.post("", response_model=ClassOut, status_code=status.HTTP_201_CREATED)
def create_class(
    payload: ClassCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    user_course = user_course_crud.get_user_course_by_id(db, payload.user_course_id)
    if user_course is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_course_id must reference an existing lecturer-course assignment",
        )
    try:
        return class_crud.create_class(db, payload, user_course)
    except class_crud.DuplicateClassIndexError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="class_index already used for this user_course_id",
        )


@router.get("", response_model=list[ClassOut])
def list_classes(
    user_course_id: UUID | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    return class_crud.list_classes(db, user_course_id)


@router.get("/{class_id}", response_model=ClassOut)
def get_class(
    class_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    return _require_class(db, class_id)


@router.patch("/{class_id}", response_model=ClassOut)
def update_class(
    class_id: UUID,
    payload: ClassUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    cls = _require_class(db, class_id)
    return class_crud.update_class(db, cls, payload)


@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class(
    class_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMIN)),
):
    cls = _require_class(db, class_id)
    class_crud.delete_class(db, cls)
