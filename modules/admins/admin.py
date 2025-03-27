from pydantic import BaseModel, Field
from datetime import datetime, timezone


class Admin(BaseModel):
    email: str
    password: str
    role: str = "admin"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
