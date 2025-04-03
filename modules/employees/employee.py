from typing import List
from bson import ObjectId
from pydantic import BaseModel, Field, field_serializer
from datetime import datetime, timezone


class Employee(BaseModel):
    name: str
    email: str
    emp_id: int
    role: str = "employee"
    phone: str
    designation: ObjectId
    department: ObjectId
    avatar: str
    dob: str
    date_of_joining: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc))
    profiles: List[ObjectId] = []

    class Config:
        arbitrary_types_allowed = True

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")
