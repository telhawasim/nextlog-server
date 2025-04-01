from datetime import datetime, timezone
from bson import ObjectId
from pydantic import BaseModel, Field


class Profile(BaseModel):
    employee_id: ObjectId
    title: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True
