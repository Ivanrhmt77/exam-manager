import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timezone

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
from app.api.deps import get_db, get_current_user, get_user_by_id, bearer_scheme
from app.crud.user import get_user_by_email
from app.crud.token_blocklist import is_token_revoked, revoke_token

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
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
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

    if is_token_revoked(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The session has been logged out",
        )

    user = get_user_by_id(db, data["sub"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return _build_token_response(user, payload.refresh_token)


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    payload: RefreshRequest,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: User = Depends(get_current_user),
):
    access_data = decode_token(credentials.credentials)
    revoke_token(
        jti=access_data["jti"],
        expires_at=datetime.fromtimestamp(access_data["exp"], tz=timezone.utc),
    )

    try:
        refresh_data = decode_token(payload.refresh_token)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    if refresh_data.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The provided token is not a refresh token",
        )

    if refresh_data["sub"] != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The refresh token does not belong to this user",
        )

    expired_at = datetime.fromtimestamp(refresh_data["exp"], tz=timezone.utc)
    revoke_token(refresh_data["jti"], expired_at)

    return {"detail": "Logout successful"}


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


@router.get("/test-auth", status_code=status.HTTP_200_OK)
def test_auth(current_user: User = Depends(get_current_user)):
    return {"detail": "Authenticated"}
