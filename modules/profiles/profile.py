from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, field_serializer


class BasicInformation(BaseModel):
    name: str
    designation: ObjectId
    email: str
    phone: str
    git_link: str
    linked_in_link: str
    summary: str

    class Config:
        arbitrary_types_allowed = True


class Profile(BaseModel):
    employee_id: ObjectId
    title: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    basic_information: Optional[BasicInformation] = None

    class Config:
        arbitrary_types_allowed = True

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")
