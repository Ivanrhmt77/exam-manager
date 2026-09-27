from datetime import time
from pydantic import BaseModel, ConfigDict
from uuid import UUID

from app.models.class_ import Term, ClassStatus


class ClassOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_course_id: UUID
    class_index: int
    name: str
    academic_year: int
    term: Term
    status: ClassStatus
    schedule_day: str | None = None
    schedule_start_time: time | None = None
    schedule_end_time: time | None = None
    room: str | None = None


class ClassCreate(BaseModel):
    user_course_id: UUID
    class_index: int
    academic_year: int
    term: Term
    schedule_day: str | None = None
    schedule_start_time: time | None = None
    schedule_end_time: time | None = None
    room: str | None = None


class ClassUpdate(BaseModel):
    academic_year: int | None = None
    term: Term | None = None
    status: ClassStatus | None = None
    schedule_day: str | None = None
    schedule_start_time: time | None = None
    schedule_end_time: time | None = None
    room: str | None = None
