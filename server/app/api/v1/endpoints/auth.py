import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import (
    TokenResponse,
    LoginRequest,
    RefreshRequest,
    ChangePasswordRequest,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    decode_token,
    hash_password,
)
from app.schemas.user import UserOut
from app.api.deps import get_db, get_current_user
from app.crud.user import get_user_by_email

router = APIRouter(prefix="/auth", tags=["auth"])


def _build_token_response(
    user: User, refresh_token: str | None = None
) -> TokenResponse:
    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=refresh_token or create_refresh_token(user.id),
        must_change_password=user.must_change_password,
        user=UserOut.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    return _build_token_response(user)


@router.post("/refresh", response_model=TokenResponse)
def register(payload: RefreshRequest, db: Session = Depends(get_db)):
    try:
        data = decode_token(payload.refresh_token)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    if data.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The provided token is not a refresh token",
        )

    user = (
        db.query(User)
        .filter(User.id == data["sub"], User.is_deleted.is_(False))
        .first()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return _build_token_response(user, payload.refresh_token)


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(payload.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    current_user.hashed_password = hash_password(payload.new_password)
    current_user.must_change_password = False
    db.commit()

    return {"detail": "Password changed successfully"}
