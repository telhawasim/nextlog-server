from typing import List
from bson import ObjectId
from pydantic import BaseModel, Field
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
    created_at: str = (
        datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+00:00"
    )
    profiles: List[ObjectId] = []

    class Config:
        arbitrary_types_allowed = True
