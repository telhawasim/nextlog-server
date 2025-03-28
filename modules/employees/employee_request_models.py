from pydantic import BaseModel
from typing import Optional
from app.exception import CustomException


class AddEmployeeRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    designation: Optional[str] = None

    def validate_add_employee(self):
        if not self.name:
            raise CustomException(status_code=404, message="Name is required")
        if not self.email:
            raise CustomException(status_code=404, message="Email is required")
        if not self.designation:
            raise CustomException(status_code=404, message="Designation is required")
