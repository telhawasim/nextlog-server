from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
from app.exception import CustomException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AddAdminRequest(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

    def add_admin_validation(self):
        if not self.email:
            raise CustomException(status_code=404, message="Email is required")
        if not self.password:
            raise CustomException(status_code=404, message="Password is required")

    def hash_password(self):
        self.password = pwd_context.hash(self.password)
