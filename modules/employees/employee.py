from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class Employee(BaseModel):
    name: str
    email: str
    role: str = "employee"
    designation: ObjectId
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True
