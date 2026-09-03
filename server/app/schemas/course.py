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
