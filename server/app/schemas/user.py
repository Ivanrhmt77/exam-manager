from pydantic import BaseModel, ConfigDict, EmailStr, model_validator
from uuid import UUID
from app.models.user import UserRole


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    name: str
    role: UserRole
    nip: str | None = None
    nrp: str | None = None
    must_change_password: bool


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    role: UserRole
    nip: str | None = None
    nrp: str | None = None

    @model_validator(mode="after")
    def validate_identifier(self):
        if self.role == UserRole.ADMIN:
            raise ValueError(
                "Creating admin accounts via this endpoint is not supported"
            )
        if self.role == UserRole.LECTURER and not self.nip:
            raise ValueError("nip is required for lecturer role")
        if self.role == UserRole.STUDENT and not self.nrp:
            raise ValueError("nrp is required for student role")
        return self


class UserUpdate(BaseModel):
    name: str | None = None
    nip: str | None = None
    nrp: str | None = None
