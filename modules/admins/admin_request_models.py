from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
from app.exception import CustomException


class AddAdminRequest(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

    def add_admin_validation(self):
        if not self.email:
            raise CustomException(status_code=404, message="Email is required")
        if not self.password:
            raise CustomException(status_code=404, message="Password is required")


class DeleteAdminRequest(BaseModel):
    email: Optional[str]

    def delete_admin_validation(self):
        if not self.email:
            raise CustomException(status_code=404, message="Email is required")
