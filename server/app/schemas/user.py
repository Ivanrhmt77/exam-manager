from pydantic import BaseModel, ConfigDict, EmailStr
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
