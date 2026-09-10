from pydantic import BaseModel, ConfigDict
from uuid import UUID

from app.schemas.user import UserOut


class UserCourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    course_id: UUID
    user: UserOut


class UserCourseCreate(BaseModel):
    user_id: UUID
