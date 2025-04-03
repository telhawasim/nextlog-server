from typing import Optional
from pydantic import BaseModel
from app.exception import CustomException


class AddProfile(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None

    def add_profile_validation(self):
        if not self.id:
            raise CustomException(status_code=422, message="Employee ID is required")
        if not self.name:
            raise CustomException(status_code=422, message="Profile name is required")
