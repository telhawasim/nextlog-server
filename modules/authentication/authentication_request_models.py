from pydantic import BaseModel
from typing import Optional
from app.exception import CustomException


class LoginRequest(BaseModel):
    email: str
    password: Optional[str] = None
    emp_id: Optional[int] = None
    role: str

    def add_desigantion_validation(self):
        if self.role == "admin":
            if not self.password:
                raise CustomException(status_code=404, message="Password is required")
        else:
            if not self.emp_id:
                raise CustomException(
                    status_code=404, message="Employee ID is required"
                )
