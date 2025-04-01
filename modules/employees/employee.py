from typing import List
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class Employee(BaseModel):
    name: str
    email: str
    emp_id: int
    role: str = "employee"
    designation: ObjectId
    department: ObjectId
    avatar: str
    dob: datetime
    date_of_joining: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    profiles: List[ObjectId] = []

    class Config:
        arbitrary_types_allowed = True
