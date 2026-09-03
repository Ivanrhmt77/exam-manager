from pydantic import BaseModel, ConfigDict
from uuid import UUID

from app.models.course import CourseCategory, CourseDeliveryType


class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    name: str
    description: str
    credits: int
    category: CourseCategory
    delivery_type: CourseDeliveryType


class CourseCreate(BaseModel):
    code: str
    name: str
    description: str
    credits: str
    category: CourseCategory
    delivery_type: CourseDeliveryType


class CourseUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    description: str | None = None
    credits: str | None = None
    category: CourseCategory | None = None
    delivery_type: CourseDeliveryType | None = None
