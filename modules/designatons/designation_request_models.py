from pydantic import BaseModel
from typing import Optional
from app.exception import CustomException


class AddDesignationModel(BaseModel):
    name: Optional[str] = None

    def add_desigantion_validation(self):
        if not self.name:
            raise CustomException(status_code=422, message="Name is required")
